"""
Main controller for general API endpoints
"""

from app.models.schemas import APIInfoResponse, HealthResponse
from app.services.model_service import model_service


class MainController:
    """Controller for main API endpoints"""
    
    @staticmethod
    def get_api_info() -> APIInfoResponse:
        """Get API information"""
        return APIInfoResponse(
            message="YOLO Object Detection API",
            version="1.0.0",
            available_endpoints=[
                "/",
                "/health",
                "/detect/cats",
                "/detect/dogs"
            ]
        )
    
    @staticmethod
    def health_check() -> HealthResponse:
        """Health check endpoint"""
        return HealthResponse(
            status="healthy",
            models_loaded=model_service.get_loaded_models(),
            available_models=model_service.get_available_models()
        )


# Controller instance
main_controller = MainController()