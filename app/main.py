"""
FastAPI Application Factory and Main Entry Point
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.main_routes import main_router
from app.routes.detection_routes import detection_router
from app.services.model_service import model_service
from app.utils.config import config


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        Configured FastAPI application instance
    """
    
    # Create FastAPI app
    app = FastAPI(
        title=config.API_TITLE,
        description=config.API_DESCRIPTION,
        version=config.API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=config.CORS_CREDENTIALS,
        allow_methods=config.CORS_METHODS,
        allow_headers=config.CORS_HEADERS,
    )
    
    # Include routers
    app.include_router(main_router)
    app.include_router(detection_router)
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        """Initialize models on startup"""
        try:
            print("🚀 Starting YOLO Detection API...")
            print("📦 Initializing models...")
            model_service.initialize_all_models()
            print("✅ All models loaded successfully!")
        except Exception as e:
            print(f"⚠️ Warning: Could not pre-load models: {e}")
            print("🔄 Models will be loaded on first request.")
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        print("🛑 Shutting down YOLO Detection API...")
    
    return app


# Create app instance
app = create_app()


def main():
    """Main entry point for running the application"""
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )


if __name__ == "__main__":
    main()