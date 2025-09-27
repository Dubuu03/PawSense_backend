"""
Detection routes
"""

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from app.controllers.detection_controller import detection_controller


# Create detection router
detection_router = APIRouter(
    prefix="/detect",
    tags=["Detection"]
)


@detection_router.post(
    "/cats",
    response_class=JSONResponse,
    summary="Detect Cat Skin Conditions",
    description="Upload an image to detect skin conditions in cats. Supports JPEG, PNG, BMP, TIFF formats.",
    responses={
        200: {"description": "Detection successful"},
        400: {"description": "Invalid file type or size"},
        404: {"description": "Model files not found"},
        500: {"description": "Internal server error"}
    }
)
async def detect_cats(file: UploadFile = File(..., description="Image file to analyze")):
    """
    Detect skin conditions in cat images
    
    - **file**: Image file (JPEG, PNG, BMP, TIFF) - Max 10MB
    
    Returns detection results with bounding boxes, confidence scores, and labels.
    """
    return await detection_controller.detect_cats(file)


@detection_router.post(
    "/dogs",
    response_class=JSONResponse,
    summary="Detect Dog Skin Conditions", 
    description="Upload an image to detect skin conditions in dogs. Supports JPEG, PNG, BMP, TIFF formats.",
    responses={
        200: {"description": "Detection successful"},
        400: {"description": "Invalid file type or size"},
        404: {"description": "Model files not found"},
        500: {"description": "Internal server error"}
    }
)
async def detect_dogs(file: UploadFile = File(..., description="Image file to analyze")):
    """
    Detect skin conditions in dog images
    
    - **file**: Image file (JPEG, PNG, BMP, TIFF) - Max 10MB
    
    Returns detection results with bounding boxes, confidence scores, and labels.
    """
    return await detection_controller.detect_dogs(file)