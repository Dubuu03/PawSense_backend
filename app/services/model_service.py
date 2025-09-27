"""
Model loading and management service
"""

import json
import yaml
import os
import tempfile
import requests
from typing import Dict, Any
from fastapi import HTTPException
from ultralytics import YOLO
from pathlib import Path

from app.utils.config import config


class ModelService:
    """Service for managing YOLO models and their metadata"""
    
    def __init__(self):
        self.models_cache = {}
        self.labels_cache = {}
        self.metadata_cache = {}
        
        # Hugging Face URLs from config
        self.hf_urls = config.HF_URLS
        
        # Download timeout from config
        self.download_timeout = config.MODEL_DOWNLOAD_TIMEOUT
    
    def download_file(self, url: str) -> str:
        """
        Download file from URL to temporary location
        
        Args:
            url: URL to download from
            
        Returns:
            Path to downloaded file
        """
        try:
            response = requests.get(url, timeout=self.download_timeout)
            response.raise_for_status()
            
            # Create temporary file with appropriate extension
            suffix = Path(url).suffix or '.tmp'
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            temp_file.write(response.content)
            temp_file.close()
            
            return temp_file.name
        
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error downloading file from {url}: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving downloaded file: {str(e)}")
    
    def load_labels(self, model_type: str) -> Dict[int, str]:
        """
        Load class labels from Hugging Face JSON file
        
        Args:
            model_type: Either 'cats' or 'dogs'
            
        Returns:
            Dictionary mapping class IDs to label names
        """
        try:
            # Check cache first
            if model_type in self.labels_cache:
                return self.labels_cache[model_type]
            
            # Download and load labels
            labels_url = self.hf_urls[model_type]['labels']
            temp_path = self.download_file(labels_url)
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                labels_dict = json.load(f)
            
            # Convert string keys to integers and cache
            labels = {int(k): v for k, v in labels_dict.items()}
            self.labels_cache[model_type] = labels
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return labels
        
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Model type '{model_type}' not found")
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Invalid JSON in labels file: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading labels: {str(e)}")
    
    def load_metadata(self, model_type: str) -> Dict[str, Any]:
        """
        Load model metadata from Hugging Face YAML file
        
        Args:
            model_type: Either 'cats' or 'dogs'
            
        Returns:
            Dictionary containing model metadata
        """
        try:
            # Check cache first
            if model_type in self.metadata_cache:
                return self.metadata_cache[model_type]
            
            # Download and load metadata
            metadata_url = self.hf_urls[model_type]['metadata']
            temp_path = self.download_file(metadata_url)
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                metadata = yaml.safe_load(f)
            
            # Cache the metadata
            self.metadata_cache[model_type] = metadata
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return metadata
        
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Model type '{model_type}' not found")
        except yaml.YAMLError as e:
            raise HTTPException(status_code=500, detail=f"Invalid YAML in metadata file: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading metadata: {str(e)}")
    
    def load_model(self, model_type: str) -> YOLO:
        """
        Load YOLO model from Hugging Face .tflite file
        
        Args:
            model_type: Either 'cats' or 'dogs'
            
        Returns:
            Loaded YOLO model
        """
        try:
            # Check cache first
            if model_type in self.models_cache:
                return self.models_cache[model_type]
            
            # Download and load model
            model_url = self.hf_urls[model_type]['model']
            temp_path = self.download_file(model_url)
            
            model = YOLO(temp_path, task="detect")
            
            # Cache the model (keep temp file for model to use)
            self.models_cache[model_type] = model
            
            return model
        
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Model type '{model_type}' not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")
    
    def initialize_model_resources(self, model_type: str) -> None:
        """
        Initialize and cache model resources (model, labels, metadata) from Hugging Face
        
        Args:
            model_type: Either 'cats' or 'dogs'
        """
        if model_type not in self.hf_urls:
            raise HTTPException(status_code=400, detail=f"Invalid model type: {model_type}")
        
        # Load and cache resources if not already loaded
        if model_type not in self.models_cache:
            self.models_cache[model_type] = self.load_model(model_type)
        
        if model_type not in self.labels_cache:
            self.labels_cache[model_type] = self.load_labels(model_type)
        
        if model_type not in self.metadata_cache:
            self.metadata_cache[model_type] = self.load_metadata(model_type)
    
    def get_model(self, model_type: str) -> YOLO:
        """Get cached model"""
        if model_type not in self.models_cache:
            self.initialize_model_resources(model_type)
        return self.models_cache[model_type]
    
    def get_labels(self, model_type: str) -> Dict[int, str]:
        """Get cached labels"""
        if model_type not in self.labels_cache:
            self.initialize_model_resources(model_type)
        return self.labels_cache[model_type]
    
    def get_metadata(self, model_type: str) -> Dict[str, Any]:
        """Get cached metadata"""
        if model_type not in self.metadata_cache:
            self.initialize_model_resources(model_type)
        return self.metadata_cache[model_type]
    
    def get_loaded_models(self) -> list:
        """Get list of loaded models"""
        return list(self.models_cache.keys())
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        return list(self.hf_urls.keys())
    
    def initialize_all_models(self) -> None:
        """Initialize all available models"""
        for model_type in self.hf_urls.keys():
            try:
                self.initialize_model_resources(model_type)
            except Exception as e:
                print(f"Warning: Could not initialize {model_type} model: {e}")


# Global model service instance
model_service = ModelService()