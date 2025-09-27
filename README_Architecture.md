# YOLO Object Detection FastAPI Backend - Refactored Architecture

A clean, modular FastAPI backend for detecting skin conditions in cats and dogs using YOLO models. This refactored version uses a proper MVC (Model-View-Controller) architecture with separation of concerns.

## 🏗️ Architecture Overview

```
backend/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application factory
│   ├── controllers/              # Business logic controllers
│   │   ├── __init__.py
│   │   ├── detection_controller.py
│   │   └── main_controller.py
│   ├── routes/                   # API route definitions
│   │   ├── __init__.py
│   │   ├── detection_routes.py
│   │   └── main_routes.py
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── detection_service.py
│   │   └── model_service.py
│   ├── models/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── utils/                    # Utilities and configuration
│       ├── __init__.py
│       └── config.py
├── models/                       # YOLO model files
│   ├── cats/
│   └── dogs/
├── main.py                       # Application entry point (old)
├── main_new.py                   # New application entry point
├── requirements.txt
└── README_Architecture.md        # This file
```

## 📁 Component Details

### 🎯 **Controllers** (`app/controllers/`)
Controllers handle HTTP requests and coordinate between routes and services.

- **`detection_controller.py`** - Handles detection-related requests
- **`main_controller.py`** - Handles general API endpoints

### 🛣️ **Routes** (`app/routes/`)
Routes define API endpoints and their documentation.

- **`detection_routes.py`** - `/detect/cats` and `/detect/dogs` endpoints
- **`main_routes.py`** - `/` and `/health` endpoints

### 🔧 **Services** (`app/services/`)
Services contain the core business logic.

- **`model_service.py`** - Model loading, caching, and management
- **`detection_service.py`** - Image processing and YOLO inference

### 📊 **Models** (`app/models/`)
Pydantic models for request/response validation.

- **`schemas.py`** - All API schemas and data models

### ⚙️ **Utils** (`app/utils/`)
Utilities and configuration.

- **`config.py`** - Application configuration and settings

## 🚀 Key Benefits of This Architecture

### ✅ **Separation of Concerns**
- **Routes**: Handle HTTP specifics
- **Controllers**: Orchestrate business logic  
- **Services**: Implement core functionality
- **Models**: Define data structures

### ✅ **Maintainability**
- Easy to locate and modify specific functionality
- Clear dependencies between components
- Modular design allows independent testing

### ✅ **Scalability**
- Easy to add new endpoints or models
- Services can be reused across controllers
- Configuration centralized in one place

### ✅ **Testability**
- Each component can be unit tested independently
- Dependency injection makes mocking easier
- Clear interfaces between layers

## 🔄 Migration from Old Structure

The functionality remains exactly the same, but now it's organized properly:

**Old `main.py` (monolithic)** ➡️ **New modular structure**

### What Changed:
1. **Split monolithic file** into logical components
2. **Added proper error handling** with structured responses
3. **Centralized configuration** in `config.py`
4. **Added Pydantic models** for better validation
5. **Improved documentation** with FastAPI auto-docs

### What Stayed the Same:
- ✅ Same API endpoints (`/detect/cats`, `/detect/dogs`, etc.)
- ✅ Same request/response formats
- ✅ Same YOLO model loading and inference
- ✅ Same error handling behavior
- ✅ Same Flutter app compatibility

## 📋 Usage

### Recommended Ways to Run:

```bash
# Method 1: Run app main directly (Recommended)
python -m app.main

# Method 2: Run via root main.py wrapper
python main.py

# Method 3: Run with uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Method 4: Use the interactive startup script
start_server.bat
```

## 🧪 Testing the New Structure

```bash
# Test that everything works
python test_setup.py

# Test specific endpoints
curl -X POST "http://localhost:8000/detect/cats" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_cat.jpg"
```

## 📚 API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

### Available Endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/detect/cats` | Cat skin condition detection |
| POST | `/detect/dogs` | Dog skin condition detection |

## 🔧 Configuration

All configuration is centralized in `app/utils/config.py`:

```python
class Config:
    API_TITLE = "YOLO Object Detection API"
    API_VERSION = "1.0.0"
    HOST = "0.0.0.0"
    PORT = 8000
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = ["image/jpeg", "image/png", ...]
    # ... more settings
```

## 🧩 Adding New Features

### Add New Model Type:
1. **Config**: Add model config in `config.py`
2. **Controller**: Add method in `detection_controller.py`
3. **Route**: Add endpoint in `detection_routes.py`
4. **Schema**: Add model type in `schemas.py`

### Add New Endpoint:
1. **Controller**: Add method in appropriate controller
2. **Route**: Define route with decorators
3. **Schema**: Add request/response models if needed

## 🎛️ Environment Variables

You can override config with environment variables:

```bash
export API_PORT=9000
export DEBUG=false
python main_new.py
```

## 🔍 Code Quality

The refactored code includes:

- ✅ **Type hints** throughout
- ✅ **Docstrings** for all functions
- ✅ **Error handling** with proper HTTP codes
- ✅ **Pydantic validation** for all data
- ✅ **Configuration management**
- ✅ **Modular architecture**

This architecture makes the codebase much more maintainable and professional! 🚀