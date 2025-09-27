"""
Detection controller for handling detection-related requests
"""

from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.models.schemas import DetectionResponse, ErrorResponse, ModelType
from app.services.detection_service import detection_service


class DetectionController:
    """Controller for detection endpoints"""
    
    @staticmethod
    async def detect_cats(file: UploadFile = File(...)) -> JSONResponse:
        """
        Detect skin conditions in cat images
        
        Args:
            file: Image file to analyze
            
        Returns:
            JSON response with detection results
        """
        try:
            result = await detection_service.process_detection(ModelType.CATS, file)
            return JSONResponse(content=result.model_dump())
        
        except HTTPException as e:
            error_response = ErrorResponse(
                error=e.detail,
                model_type=ModelType.CATS
            )
            return JSONResponse(
                status_code=e.status_code,
                content=error_response.model_dump()
            )
        except Exception as e:
            error_response = ErrorResponse(
                error=f"Unexpected error: {str(e)}",
                model_type=ModelType.CATS
            )
            return JSONResponse(
                status_code=500,
                content=error_response.model_dump()
            )
    
    @staticmethod
    async def detect_dogs(file: UploadFile = File(...)) -> JSONResponse:
        """
        Detect skin conditions in dog images
        
        Args:
            file: Image file to analyze
            
        Returns:
            JSON response with detection results
        """
        try:
            result = await detection_service.process_detection(ModelType.DOGS, file)
            return JSONResponse(content=result.model_dump())
        
        except HTTPException as e:
            error_response = ErrorResponse(
                error=e.detail,
                model_type=ModelType.DOGS
            )
            return JSONResponse(
                status_code=e.status_code,
                content=error_response.model_dump()
            )
        except Exception as e:
            error_response = ErrorResponse(
                error=f"Unexpected error: {str(e)}",
                model_type=ModelType.DOGS
            )
            return JSONResponse(
                status_code=500,
                content=error_response.model_dump()
            )


# Controller instance
detection_controller = DetectionController()