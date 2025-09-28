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
        Run TensorFlow Lite inference on YOLO v8 model
        
        Args:
            interpreter: Loaded TensorFlow Lite interpreter
            image: PIL Image object
            labels: Dictionary mapping class IDs to label names
            
        Returns:
            List of Detection objects
        """
        try:
            print(f"🔍 Starting YOLO v8 inference for image size: {image.size}")
            
            # Get input and output details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            # Get input shape [batch, height, width, channels]
            input_shape = input_details[0]['shape']
            height, width = input_shape[1], input_shape[2]
            
            print(f"📏 Model input shape: {input_shape}")
            
            # Preprocess image
            image_resized = image.resize((width, height))
            image_rgb = image_resized.convert('RGB')
            input_data = np.array(image_rgb, dtype=np.float32)
            
            # Normalize to [0, 1]
            input_data = input_data / 255.0
            
            # Add batch dimension: [1, height, width, 3]
            input_data = np.expand_dims(input_data, axis=0)
            
            print(f"📊 Preprocessed input shape: {input_data.shape}")
            
            # Set input tensor and run inference
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            
            # Get output tensor - YOLO v8 format: [1, 4+num_classes, 8400]
            output_data = interpreter.get_tensor(output_details[0]['index'])
            print(f"📤 Raw output shape: {output_data.shape}")
            
            detections = []
            
            # Handle YOLO v8 output format: [1, 13, 8400] where 13 = 4 bbox + 9 classes
            if len(output_data.shape) == 3:
                batch_size, num_channels, num_predictions = output_data.shape
                num_classes = num_channels - 4  # First 4 channels are bbox coordinates
                
                print(f"📊 YOLO v8 format detected: {num_classes} classes, {num_predictions} predictions")
                
                # Process first batch only
                predictions = output_data[0]  # Shape: [13, 8400]
                
                # Transpose to [8400, 13] for easier processing
                predictions = predictions.transpose(1, 0)  # Now [8400, 13]
                
                print(f"📊 Transposed predictions shape: {predictions.shape}")
                
                # Process each prediction
                valid_detections = 0
                for i in range(num_predictions):
                    pred = predictions[i]  # Shape: [13]
                    
                    # Extract bbox coordinates (center format, normalized)
                    x_center, y_center, box_width, box_height = pred[:4]
                    
                    # Extract class scores
                    class_scores = pred[4:]  # [9] class probabilities
                    
                    # Find best class and confidence
                    class_id = int(np.argmax(class_scores))
                    confidence = float(class_scores[class_id])
                    
                    # Skip low confidence detections
                    if confidence < 0.25:  # Lowered threshold for testing
                        continue
                    
                    # Convert normalized coordinates to pixel coordinates
                    img_width, img_height = image.size
                    x1 = (x_center - box_width / 2) * img_width
                    y1 = (y_center - box_height / 2) * img_height
                    x2 = (x_center + box_width / 2) * img_width
                    y2 = (y_center + box_height / 2) * img_height
                    
                    # Clamp coordinates to image bounds
                    x1 = max(0, min(x1, img_width))
                    y1 = max(0, min(y1, img_height))
                    x2 = max(0, min(x2, img_width))
                    y2 = max(0, min(y2, img_height))
                    
                    # Skip invalid boxes
                    if x2 <= x1 or y2 <= y1:
                        continue
                    
                    # Get label name
                    label = labels.get(class_id, f"Unknown_{class_id}")
                    
                    print(f"🎯 Detection #{valid_detections + 1}: {label} (class={class_id}), conf={confidence:.3f}, bbox=[{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]")
                    
                    detection_obj = Detection(
                        class_id=class_id,
                        label=label,
                        confidence=round(confidence, 4),
                        bbox=[round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)]
                    )
                    
                    detections.append(detection_obj)
                    valid_detections += 1
            
            else:
                print(f"⚠️ Unexpected output shape: {output_data.shape}")
                raise HTTPException(status_code=500, detail=f"Unexpected model output shape: {output_data.shape}")
            
            print(f"✅ Found {len(detections)} valid detections above confidence threshold")
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
            
            print(f"📷 Processing {model_type} detection for image: {image.size}")
            
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
            
            print(f"🎉 Detection complete: {len(detections)} detections found")
            return response
        
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            else:
                print(f"❌ Processing error: {str(e)}")
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


# Global detection service instance
detection_service = DetectionService()