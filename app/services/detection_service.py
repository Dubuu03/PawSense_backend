"""
Detection service for running YOLO inference
"""

import io
from typing import List, Dict, Any
from PIL import Image
from fastapi import HTTPException, UploadFile
from ultralytics import YOLO

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
    def run_inference(model: YOLO, image: Image.Image, labels: Dict[int, str]) -> List[Detection]:
        """
        Run YOLO inference on an image and format results
        
        Args:
            model: Loaded YOLO model
            image: PIL Image object
            labels: Dictionary mapping class IDs to label names
            
        Returns:
            List of Detection objects
        """
        try:
            # Run inference
            results = model(image)
            
            detections = []
            
            # Process each detection
            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes
                    
                    for i in range(len(boxes)):
                        # Get detection data
                        bbox = boxes.xyxy[i].cpu().numpy().tolist()  # [x1, y1, x2, y2]
                        confidence = float(boxes.conf[i].cpu().numpy())
                        class_id = int(boxes.cls[i].cpu().numpy())
                        
                        # Get label name
                        label = labels.get(class_id, f"Unknown_{class_id}")
                        
                        detection = Detection(
                            class_id=class_id,
                            label=label,
                            confidence=round(confidence, 4),
                            bbox=[round(coord, 2) for coord in bbox]
                        )
                        
                        detections.append(detection)
            
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