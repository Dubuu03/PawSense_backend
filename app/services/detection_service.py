"""
Detection service for running TensorFlow Lite inference
"""

import io
import numpy as np
from typing import List, Dict, Any
from PIL import Image
from fastapi import HTTPException, UploadFile
import tflite_runtime.interpreter as tflite

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
        # Check file type
        if file.content_type not in config.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(config.ALLOWED_FILE_TYPES)}"
            )
        
        # Check file size
        if hasattr(file, 'size') and file.size and file.size > config.MAX_FILE_SIZE:
            max_size_mb = config.MAX_FILE_SIZE / (1024 * 1024)
            raise HTTPException(status_code=400, detail=f"File size too large. Maximum {max_size_mb}MB allowed.")
    
    @staticmethod
    def run_inference(interpreter: tflite.Interpreter, image: Image.Image, labels: Dict[int, str]) -> List[Detection]:
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
            # Get input and output details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            # Get input shape
            input_shape = input_details[0]['shape']
            height, width = input_shape[1], input_shape[2]
            
            # Preprocess image
            image_resized = image.resize((width, height))
            image_rgb = image_resized.convert('RGB')
            input_data = np.array(image_rgb, dtype=np.float32)
            
            # Normalize to [0, 1] if needed
            if input_details[0]['dtype'] == np.float32:
                input_data = input_data / 255.0
                
            # Add batch dimension
            input_data = np.expand_dims(input_data, axis=0)
            
            # Set input tensor
            interpreter.set_tensor(input_details[0]['index'], input_data)
            
            # Run inference
            interpreter.invoke()
            
            # Get output tensors
            # Assuming YOLO output format: [batch, detections, 6] where 6 = [x, y, w, h, conf, class]
            output_data = interpreter.get_tensor(output_details[0]['index'])
            
            detections = []
            
            # Process detections
            for detection in output_data[0]:  # Remove batch dimension
                if len(detection) >= 6:
                    x_center, y_center, w, h, confidence, class_id = detection[:6]
                    
                    # Skip low confidence detections
                    if confidence < 0.5:
                        continue
                    
                    # Convert from center format to corner format
                    x1 = (x_center - w/2) * image.width
                    y1 = (y_center - h/2) * image.height
                    x2 = (x_center + w/2) * image.width
                    y2 = (y_center + h/2) * image.height
                    
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
            
            return detections
        
        except Exception as e:
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