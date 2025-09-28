"""
Configuration settings for the application
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # API Configuration
    API_TITLE = "YOLO Object Detection API"
    API_DESCRIPTION = "FastAPI backend for cats and dogs skin condition detection"
    API_VERSION = "1.0.0"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # File Upload Configuration
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
    ALLOWED_FILE_TYPES = os.getenv("ALLOWED_FILE_TYPES", "image/jpeg,image/jpg,image/png,image/bmp,image/tiff").split(",")
    
    # Hugging Face Configuration
    HF_TOKEN = os.getenv("HF_TOKEN")
    
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
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") != "*" else ["*"]
    CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    # Hugging Face Model URLs
    HF_URLS = {
        "cats": {
            "model": os.getenv("HF_CAT_MODEL_URL", "https://huggingface.co/crishelpc/cat-detection-yolo/resolve/main/cat_best.tflite"),
            "labels": os.getenv("HF_CAT_LABELS_URL", "https://huggingface.co/crishelpc/cat-detection-yolo/resolve/main/labels.json"),
            "metadata": os.getenv("HF_CAT_METADATA_URL", "https://huggingface.co/crishelpc/cat-detection-yolo/resolve/main/metadata.yaml")
        },
        "dogs": {
            "model": os.getenv("HF_DOG_MODEL_URL", "https://huggingface.co/crishelpc/dogs-detection-yolo/resolve/main/dog_best.tflite"),
            "labels": os.getenv("HF_DOG_LABELS_URL", "https://huggingface.co/crishelpc/dogs-detection-yolo/resolve/main/labels.json"),
            "metadata": os.getenv("HF_DOG_METADATA_URL", "https://huggingface.co/crishelpc/dogs-detection-yolo/resolve/main/metadata.yaml")
        }
    }
    
    # Detection Configuration
    DETECTION_CONFIDENCE = float(os.getenv("DETECTION_CONFIDENCE", "0.5"))
    DETECTION_IOU = float(os.getenv("DETECTION_IOU", "0.4"))
    MODEL_DOWNLOAD_TIMEOUT = int(os.getenv("MODEL_DOWNLOAD_TIMEOUT", "300"))


# Global config instance
config = Config()