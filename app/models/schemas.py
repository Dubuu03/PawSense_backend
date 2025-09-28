"""
Pydantic models for request/response schemas
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Bounding box coordinates [x1, y1, x2, y2]"""
    x1: float = Field(..., description="Left coordinate")
    y1: float = Field(..., description="Top coordinate")  
    x2: float = Field(..., description="Right coordinate")
    y2: float = Field(..., description="Bottom coordinate")


class Detection(BaseModel):
    """Single detection result"""
    class_id: int = Field(..., description="Class ID from the model")
    label: str = Field(..., description="Human-readable label")
    confidence: float = Field(..., ge=0, le=1, description="Detection confidence score")
    bbox: List[float] = Field(..., min_items=4, max_items=4, description="Bounding box [x1, y1, x2, y2]")


class ModelInfo(BaseModel):
    """Model metadata information"""
    description: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    version: Optional[str] = None
    license: Optional[str] = None
    docs: Optional[str] = None
    stride: Optional[int] = None
    task: Optional[str] = None
    batch: Optional[int] = None
    imgsz: Optional[List[int]] = None
    names: Optional[Dict[int, str]] = None
    args: Optional[Dict[str, Any]] = None
    channels: Optional[int] = None


class DetectionResponse(BaseModel):
    """Complete detection API response"""
    filename: str = Field(..., description="Original filename")
    model_info: ModelInfo = Field(..., description="Model metadata")
    detections: List[Detection] = Field(..., description="List of detections")
    total_detections: int = Field(..., description="Total number of detections")


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    model_type: Optional[str] = Field(None, description="Model type that caused the error")
    details: Optional[str] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Server status")
    models_loaded: List[str] = Field(..., description="List of loaded models")
    available_models: List[str] = Field(..., description="List of available models")


class APIInfoResponse(BaseModel):
    """API information response"""
    message: str = Field(..., description="API description")
    version: str = Field(..., description="API version")
    available_endpoints: List[str] = Field(..., description="List of available endpoints")


# Model type enumeration
class ModelType:
    CATS = "cats"
    DOGS = "dogs"
    
    @classmethod
    def get_all(cls) -> List[str]:
        return [cls.CATS, cls.DOGS]