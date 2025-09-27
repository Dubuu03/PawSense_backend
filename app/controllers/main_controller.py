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
        try:
            # Quick health check without model loading
            models_loaded = list(model_service.models_cache.keys()) if hasattr(model_service, 'models_cache') else []
            available_models = list(model_service.hf_urls.keys()) if hasattr(model_service, 'hf_urls') else ["cats", "dogs"]
            
            return HealthResponse(
                status="healthy",
                models_loaded=models_loaded,
                available_models=available_models
            )
        except Exception as e:
            return HealthResponse(
                status="unhealthy",
                models_loaded=[],
                available_models=["cats", "dogs"]
            )


# Controller instance
main_controller = MainController()