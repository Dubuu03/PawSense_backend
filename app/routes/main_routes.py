"""
Main application routes
"""

from fastapi import APIRouter

from app.controllers.main_controller import main_controller
from app.models.schemas import APIInfoResponse, HealthResponse


# Create main router
main_router = APIRouter(tags=["Main"])


@main_router.get(
    "/",
    response_model=APIInfoResponse,
    summary="API Information",
    description="Get basic information about the API and available endpoints"
)
async def root():
    """
    Root endpoint with API information
    
    Returns basic information about the YOLO Object Detection API including
    version and available endpoints.
    """
    return main_controller.get_api_info()


@main_router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check server status and loaded models"
)
async def health_check():
    """
    Health check endpoint
    
    Returns the current status of the server and information about
    loaded models and available models.
    """
    return main_controller.health_check()