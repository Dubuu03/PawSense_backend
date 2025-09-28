"""
Detection service for running TensorFlow Lite inference
"""

import io
import os
import numpy as np
from typing import List, Dict, Any
from PIL import Image
from fastapi import HTTPException, UploadFile

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    # Fallback to TensorFlow Lite from full TensorFlow
    import tensorflow as tf
    tflite = tf.lite

from app.models.schemas import Detection, DetectionResponse, ModelInfo
from app.services.model_service import model_service
from app.utils.config import config


class DetectionService:
    """Service for handling image detection operations"""
    
    @staticmethod
    def validate_image(file: UploadFile) -> None:
        """
        Validate uploaded image file
        Args:
            file: Uploaded file object
        """
        print(f"🔍 Validating file: {file.filename}")
        print(f"📄 Content-Type received: '{file.content_type}'")
        print(f"📋 Allowed types from config: {config.ALLOWED_FILE_TYPES}")
        
        # Normalize MIME type
        content_type = (file.content_type or '').lower().strip()
        allowed_types = [t.lower().strip() for t in config.ALLOWED_FILE_TYPES]
        
        print(f"📄 Normalized content-type: '{content_type}'")
        print(f"📋 Normalized allowed types: {allowed_types}")
        
        # Accept common variants
        extra_types = ['image/pjpeg', 'image/x-png', 'image/x-bmp', 'image/gif', 'image/webp']
        allowed_types += extra_types
        
        # Check file type
        is_valid_type = content_type in allowed_types
        print(f"✅ Type validation result: {is_valid_type}")
        
        if not is_valid_type:
            # Fallback: check file extension
            import os
            ext = os.path.splitext(file.filename or '')[1].lower()
            allowed_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp']
            is_valid_ext = ext in allowed_exts
            
            print(f"📁 File extension: '{ext}'")
            print(f"📋 Allowed extensions: {allowed_exts}")
            print(f"✅ Extension validation result: {is_valid_ext}")
            
            if not is_valid_ext:
                print(f"❌ File validation failed for: {file.filename}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file type. Allowed types: {config.ALLOWED_FILE_TYPES}"
                )
            else:
                print(f"✅ File accepted via extension fallback")
        else:
            print(f"✅ File accepted via content-type")
            
        # Check file size
        if hasattr(file, 'size') and file.size and file.size > config.MAX_FILE_SIZE:
            max_size_mb = config.MAX_FILE_SIZE / (1024 * 1024)
            raise HTTPException(status_code=400, detail=f"File size too large. Maximum {max_size_mb}MB allowed.")
    
    @staticmethod
    def run_inference(interpreter, image: Image.Image, labels: Dict[int, str]) -> List[Detection]:
        """
        Run TensorFlow Lite inference on an image and format results
        
        Args:
            interpreter: Loaded TensorFlow Lite interpreter
            image: PIL Image object
            labels: Dictionary mapping class IDs to label names
            
        Returns:
            List of Detection objects
        """
        try:
            print(f"🔍 Starting inference for image size: {image.size}")
            
            # Get input and output details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            print(f"📋 Input details: {input_details}")
            print(f"📋 Output details: {output_details}")
            
            # Get input shape
            input_shape = input_details[0]['shape']
            height, width = input_shape[1], input_shape[2]
            
            print(f"📏 Expected input shape: {input_shape}")
            print(f"🎯 Resizing to: {width}x{height}")
            
            # Preprocess image
            image_resized = image.resize((width, height))
            image_rgb = image_resized.convert('RGB')
            input_data = np.array(image_rgb, dtype=np.float32)
            
            # Normalize to [0, 1] for most YOLO models
            input_data = input_data / 255.0
                
            # Add batch dimension
            input_data = np.expand_dims(input_data, axis=0)
            
            print(f"📊 Input data shape: {input_data.shape}")
            print(f"📊 Input data range: [{input_data.min():.3f}, {input_data.max():.3f}]")
            
            # Set input tensor
            interpreter.set_tensor(input_details[0]['index'], input_data)
            
            # Run inference
            print("🚀 Running inference...")
            interpreter.invoke()
            
            # Get all output tensors
            outputs = []
            for i, detail in enumerate(output_details):
                output = interpreter.get_tensor(detail['index'])
                outputs.append(output)
                print(f"📤 Output {i} shape: {output.shape}, dtype: {output.dtype}")
            
            # Process outputs based on the format
            detections = []
            
            # Handle different YOLO output formats
            if len(outputs) == 1:
                # Single output tensor - typical YOLO format
                output_data = outputs[0]
                print(f"📊 Single output shape: {output_data.shape}")
                
                if len(output_data.shape) == 3:
                    # Format: [batch, num_detections, 85] where 85 = [x, y, w, h, conf, class_scores...]
                    # OR: [batch, 25200, 85] for YOLOv8
                    
                    batch_size, num_detections, num_values = output_data.shape
                    print(f"📊 Detections tensor: {batch_size} batches, {num_detections} detections, {num_values} values each")
                    
                    for i in range(num_detections):
                        detection = output_data[0][i]  # Get detection from first batch
                        
                        if num_values >= 85:  # Standard YOLO format
                            x_center, y_center, w, h, obj_conf = detection[:5]
                            class_scores = detection[5:]
                            
                            # Find the class with highest score
                            class_id = np.argmax(class_scores)
                            class_score = class_scores[class_id]
                            
                            # Combined confidence
                            confidence = obj_conf * class_score
                            
                        elif num_values >= 6:  # Simplified format [x, y, w, h, conf, class]
                            x_center, y_center, w, h, confidence, class_id = detection[:6]
                            class_id = int(class_id)
                            
                        else:
                            print(f"⚠️ Unexpected detection format with {num_values} values")
                            continue
                        
                        # Skip low confidence detections
                        if confidence < 0.5:
                            continue
                        
                        print(f"🎯 Detection: class={class_id}, conf={confidence:.3f}, bbox=({x_center:.1f}, {y_center:.1f}, {w:.1f}, {h:.1f})")
                        
                        # Convert from normalized center format to pixel corner format
                        # Ultralytics YOLO outputs are typically normalized [0, 1]
                        if x_center <= 1.0 and y_center <= 1.0:  # Normalized coordinates
                            x1 = (x_center - w/2) * image.width
                            y1 = (y_center - h/2) * image.height
                            x2 = (x_center + w/2) * image.width
                            y2 = (y_center + h/2) * image.height
                        else:  # Already in pixel coordinates
                            x1 = x_center - w/2
                            y1 = y_center - h/2
                            x2 = x_center + w/2
                            y2 = y_center + h/2
                        
                        # Ensure coordinates are within image bounds
                        x1 = max(0, min(x1, image.width))
                        y1 = max(0, min(y1, image.height))
                        x2 = max(0, min(x2, image.width))
                        y2 = max(0, min(y2, image.height))
                        
                        # Skip invalid boxes
                        if x2 <= x1 or y2 <= y1:
                            continue
                        
                        # Get label name
                        class_id = int(class_id)
                        label = labels.get(class_id, f"Unknown_{class_id}")
                        
                        detection_obj = Detection(
                            class_id=class_id,
                            label=label,
                            confidence=round(float(confidence), 4),
                            bbox=[round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)]
                        )
                        
                        detections.append(detection_obj)
                        print(f"✅ Added detection: {label} ({confidence:.3f})")
                
                elif len(output_data.shape) == 2:
                    # Format: [num_detections, values]
                    print(f"📊 2D output format: {output_data.shape}")
                    # Handle 2D format if needed
                    pass
            
            else:
                # Multiple output tensors
                print(f"📊 Multiple outputs: {len(outputs)}")
                # Handle multiple output format if needed
                pass
            
            print(f"🎉 Found {len(detections)} valid detections")
            return detections
        
        except Exception as e:
            print(f"❌ Inference error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error during inference: {str(e)}")
    
    @staticmethod
    async def process_detection(model_type: str, file: UploadFile) -> DetectionResponse:
        """
        Process image detection for a specific model type
        
        Args:
            model_type: Either 'cats' or 'dogs'
            file: Uploaded image file
            
        Returns:
            DetectionResponse object
        """
        # Validate image
        DetectionService.validate_image(file)
        
        try:
            # Read and process image
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get model resources
            model = model_service.get_model(model_type)
            labels = model_service.get_labels(model_type)
            metadata = model_service.get_metadata(model_type)
            
            # Run inference
            detections = DetectionService.run_inference(model, image, labels)
            
            # Prepare response
            response = DetectionResponse(
                filename=file.filename or "unknown.jpg",
                model_info=ModelInfo(**metadata),
                detections=detections,
                total_detections=len(detections)
            )
            
            return response
        
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            else:
                raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


# Global detection service instance
detection_service = DetectionService()