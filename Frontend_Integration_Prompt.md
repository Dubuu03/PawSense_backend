# 🎯 PawSense Flutter Backend Integration - GitHub Copilot Prompt

## 📋 Project Context
I have a **FastAPI backend deployed on Railway** for a **Pet Skin Condition Detection System** called **PawSense**. The backend uses TensorFlow Lite models to detect skin conditions in cats and dogs through image analysis.

I have an **existing Flutter frontend** that needs to integrate with this backend.

**Backend URL:** `https://pawsensebackend-production.up.railway.app`

## 🏗️ Current Backend Architecture

### Available API Endpoints:
```
GET  /                    - API information
GET  /health             - Health check and model status
POST /detect/cats        - Detect cat skin conditions
POST /detect/dogs        - Detect dog skin conditions
GET  /docs               - Swagger documentation
```

### API Request/Response Structure:

#### Detection Request:
```javascript
// POST /detect/cats OR /detect/dogs
Content-Type: multipart/form-data

FormData: {
  file: File // Image file (JPEG, PNG, BMP, TIFF, max 10MB)
}

Headers: {
  'Accept': 'application/json'
  // No Authorization header needed - public endpoints
}
```

#### Required Input Parameters:
- **Endpoint Path:** Must be either `/detect/cats` or `/detect/dogs`
- **HTTP Method:** POST only
- **Content-Type:** multipart/form-data (automatically set by FormData)
- **File Field Name:** Must be exactly `"file"` (case-sensitive)
- **File Constraints:**
  - **Max Size:** 10MB (10,485,760 bytes)
  - **Allowed Types:** `image/jpeg`, `image/jpg`, `image/png`, `image/bmp`, `image/tiff`
  - **Required:** File must exist and be readable

#### Detection Response:
```javascript
{
  "filename": "cat_image.jpg",
  "model_info": {
    "description": "Cat skin condition detection model",
    "author": "PawSense Team",
    "version": "1.0.0",
    "task": "detection"
  },
  "detections": [
    {
      "class_id": 0,
      "label": "healthy_skin",
      "confidence": 0.8567,
      "bbox": [120.5, 89.3, 245.7, 198.2]
    }
  ],
  "total_detections": 1
}
```

#### Health Check Response:
```javascript
{
  "status": "healthy",
  "models_loaded": ["cats", "dogs"],
  "available_models": ["cats", "dogs"]
}
```

## 🎯 Flutter Integration Requirements

### Backend Integration Needs:
1. **HTTP Client Service** - Dio or http package integration
2. **Image Upload Handling** - MultipartFile upload to FastAPI
3. **API Response Models** - Dart classes matching backend schemas
4. **Error Handling** - Exception handling for API calls
5. **State Management** - Provider/Riverpod/Bloc for API states
6. **Image Processing** - Handle detection results and bounding boxes
7. **File Validation** - Client-side file type and size validation

### Flutter Technical Requirements:
- **HTTP Package:** `dio` for multipart file uploads
- **State Management:** Provider, Riverpod, or Bloc pattern
- **Image Handling:** `image_picker` and `image` packages
- **JSON Serialization:** `json_annotation` and `json_serializable`
- **Error Handling:** Custom exception classes
- **Loading States:** FutureBuilder or state management solutions

## 📱 Flutter Data Models

### Required Dart Classes:
```dart
// Detection Result Model
class Detection {
  final int classId;
  final String label;
  final double confidence;
  final List<double> bbox; // [x1, y1, x2, y2]
}

// API Response Model
class DetectionResponse {
  final String filename;
  final ModelInfo modelInfo;
  final List<Detection> detections;
  final int totalDetections;
}

// Health Check Model
class HealthResponse {
  final String status;
  final List<String> modelsLoaded;
  final List<String> availableModels;
}

// Error Response Model
class ApiError {
  final String error;
  final String? modelType;
  final String? details;
}
```

## 💻 Flutter Implementation Tasks

### Please help me create:

1. **API Service Class** with:
   - Dio HTTP client configuration
   - Authentication headers setup
   - Base URL configuration for Railway deployment
   - Retry logic and timeout handling

2. **Detection Service** with:
   - `Future<DetectionResponse> detectCats(File imageFile)`
   - `Future<DetectionResponse> detectDogs(File imageFile)`
   - `Future<HealthResponse> checkHealth()`
   - Multipart file upload implementation

3. **Data Models** with:
   - JSON serialization annotations
   - `fromJson()` and `toJson()` methods
   - Proper null safety handling
   - Type-safe model classes

4. **Exception Handling** with:
   - Custom API exception classes
   - Network error handling
   - HTTP status code mapping
   - User-friendly error messages

5. **State Management** with:
   - Loading states for API calls
   - Error state management
   - Success state with results
   - Image upload progress tracking

6. **File Handling** with:
   - Image picker integration
   - File validation (size, type)
   - MultipartFile conversion
   - Proper filename handling

## 🔧 Flutter Code Examples Needed:

### API Service Implementation:
```dart
// Example of what I need help with:
class PawSenseApiService {
  static const String baseUrl = 'https://pawsensebackend-production.up.railway.app';
  
  Future<DetectionResponse> detectConditions(File imageFile, String modelType) async {
    // CRITICAL: Must validate inputs before API call
    // - imageFile: Must exist and be readable
    // - modelType: Must be exactly "cats" or "dogs"
    // - File size: Must be ≤ 10MB
    // - File type: Must be JPEG, PNG, BMP, or TIFF
    
    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(
        imageFile.path,
        filename: imageFile.path.split('/').last,
      ),
    });
    
    final response = await dio.post(
      '/detect/$modelType',  // modelType = "cats" or "dogs"
      data: formData,
      options: Options(
        headers: {'Accept': 'application/json'},
        contentType: 'multipart/form-data',
      ),
    );
    
    // Parse response and handle all possible status codes
  }
}
```

### State Management:
```dart
// Help needed for state management pattern:
class DetectionProvider extends ChangeNotifier {
  DetectionResponse? _result;
  bool _isLoading = false;
  String? _error;
  
  // Implementation needed for state updates
}
```

### Error Handling:
```dart
// Comprehensive error handling for all scenarios:
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  
  // Custom exception handling implementation needed
}
```

## 🚀 Flutter Dependencies Needed:
```yaml
dependencies:
  dio: ^5.3.2                    # HTTP client for API calls
  image_picker: ^1.0.4          # Image selection from gallery/camera
  json_annotation: ^4.8.1       # JSON serialization
  provider: ^6.0.5              # State management (or riverpod/bloc)
  
dev_dependencies:
  json_serializable: ^6.7.1     # Code generation for JSON
  build_runner: ^2.4.6          # Code generation runner
```

## 📱 Integration Architecture:
```
Flutter App
    ├── services/
    │   ├── api_service.dart          # HTTP client & endpoints
    │   ├── detection_service.dart    # Detection API calls
    │   └── image_service.dart        # Image handling
    ├── models/
    │   ├── detection_response.dart   # API response models
    │   ├── health_response.dart      # Health check model
    │   └── api_error.dart           # Error handling models
    ├── providers/
    │   └── detection_provider.dart   # State management
    └── utils/
        ├── constants.dart            # API URLs & config
        └── exceptions.dart           # Custom exceptions
```

## 📋 Critical Input Requirements & Validation

### File Upload Validation Checklist:
```dart
bool validateImageFile(File imageFile) {
  // 1. File exists and readable
  if (!imageFile.existsSync()) return false;
  
  // 2. File size ≤ 10MB
  if (imageFile.lengthSync() > 10 * 1024 * 1024) return false;
  
  // 3. File extension validation
  final allowedExtensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'];
  final extension = imageFile.path.toLowerCase().split('.').last;
  if (!allowedExtensions.contains('.$extension')) return false;
  
  return true;
}
```

### Model Type Validation:
```dart
enum ModelType {
  cats('cats'),
  dogs('dogs');
  
  const ModelType(this.value);
  final String value;
}

// Usage: ModelType.cats.value or ModelType.dogs.value
```

### API Response Status Codes:
- **200:** Success - Detection completed
- **400:** Bad Request - Invalid file (size/type) or missing file parameter
- **404:** Not Found - Model files not found on server
- **500:** Internal Server Error - Processing failed

### Expected Response Time:
- **Health Check:** < 1 second
- **Detection:** 2-10 seconds (depends on image size and model complexity)

## 🎯 Immediate Next Steps:
1. Set up Dio HTTP client with Railway URL
2. Create data models with JSON serialization
3. Implement input validation functions
4. Implement API service methods with proper error handling
5. Add state management for detection flow
6. Integrate image picker and file upload
7. Handle all possible API responses and errors

---

**Goal:** Integrate my existing Flutter frontend with the Railway-deployed FastAPI backend for PawSense pet skin condition detection. I need clean, efficient Dart code for API communication, data models, state management, and error handling.

Please help me implement the backend integration step by step, starting with the API service setup and data models!