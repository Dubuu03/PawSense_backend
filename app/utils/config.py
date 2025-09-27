"""
Configuration settings for the application
"""

import os
from typing import Dict, Any


class Config:
    """Application configuration"""
    
    # API Configuration
    API_TITLE = "YOLO Object Detection API"
    API_DESCRIPTION = "FastAPI backend for cats and dogs skin condition detection"
    API_VERSION = "1.0.0"
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    
    # File Upload Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/bmp", "image/tiff"]
    
    # Model Configuration
    MODELS_DIR = "models"
    MODEL_CONFIGS = {
        "cats": {
            "model_path": os.path.join(MODELS_DIR, "cats", "cat_best.tflite"),
            "labels_path": os.path.join(MODELS_DIR, "cats", "labels.json"),
            "metadata_path": os.path.join(MODELS_DIR, "cats", "metadata.yaml")
        },
        "dogs": {
            "model_path": os.path.join(MODELS_DIR, "dogs", "dog_best.tflite"),
            "labels_path": os.path.join(MODELS_DIR, "dogs", "labels.json"),
            "metadata_path": os.path.join(MODELS_DIR, "dogs", "metadata.yaml")
        }
    }
    
    # CORS Configuration
    CORS_ORIGINS = ["*"]  # In production, replace with specific origins
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]


# Global config instance
config = Config()