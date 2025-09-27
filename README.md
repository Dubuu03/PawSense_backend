# YOLO Object Detection FastAPI Backend

This FastAPI backend provides endpoints for detecting skin conditions in cats and dogs using YOLO models.

## Features

- **Two separate detection models:**
  - `/detect/cats` - Detects skin conditions in cats (Alopecia, Eosinophilic Plague, Miliary Dermatitis, ear mite, feline acne, flea, fleas, ringworm)
  - `/detect/dogs` - Detects skin conditions in dogs (dermatitis, fleas, fungal_infection, hotspot, mange, pyoderma, ringworm, ticks, unknown_abnormality)

- **Dynamic loading:** Models, labels, and metadata are loaded dynamically from configuration files
- **Error handling:** Comprehensive error handling with meaningful JSON responses
- **CORS support:** Ready for Flutter app integration
- **Image validation:** Supports JPEG, PNG, BMP, TIFF formats with size limits

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Directory Structure

Ensure your directory structure matches:
```
backend/
├── main.py
├── requirements.txt
├── README.md
└── models/
    ├── cats/
    │   ├── cat_best.tflite
    │   ├── labels.json
    │   └── metadata.yaml
    └── dogs/
        ├── dog_best.tflite
        ├── labels.json
        └── metadata.yaml
```

### 3. Run the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/health` - Check server status and loaded models

### Root
- **GET** `/` - API information and available endpoints

### Detection Endpoints
- **POST** `/detect/cats` - Detect skin conditions in cat images
- **POST** `/detect/dogs` - Detect skin conditions in dog images

## Request Format

Both detection endpoints accept `multipart/form-data` with an image file:

```
Content-Type: multipart/form-data
file: [image file]
```

## Response Format

### Success Response (200 OK)

```json
{
  "filename": "cat_image.jpg",
  "model_info": {
    "description": "Ultralytics best model trained on data.yaml",
    "author": "Ultralytics",
    "date": "2025-09-27T14:56:59.819576",
    "version": "8.3.203",
    "license": "AGPL-3.0 License (https://ultralytics.com/license)",
    "stride": 32,
    "task": "detect",
    "batch": 1,
    "imgsz": [640, 640],
    "names": {
      "0": "Alopecia",
      "1": "Eosinophilic Plague",
      ...
    }
  },
  "detections": [
    {
      "class_id": 0,
      "label": "Alopecia",
      "confidence": 0.8542,
      "bbox": [123.45, 67.89, 234.56, 178.90]
    },
    {
      "class_id": 5,
      "label": "flea",
      "confidence": 0.7321,
      "bbox": [345.67, 123.45, 456.78, 234.56]
    }
  ],
  "total_detections": 2
}
```

### Error Response (4xx/5xx)

```json
{
  "error": "Error message description",
  "model_type": "cats"
}
```

## Usage Examples

### Using curl

```bash
# Test cats detection
curl -X POST "http://localhost:8000/detect/cats" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/cat_image.jpg"

# Test dogs detection  
curl -X POST "http://localhost:8000/detect/dogs" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/dog_image.jpg"

# Health check
curl http://localhost:8000/health
```

### Using Python requests

```python
import requests

# Cats detection
with open('cat_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/detect/cats', files=files)
    result = response.json()
    print(result)

# Dogs detection
with open('dog_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/detect/dogs', files=files)
    result = response.json()
    print(result)
```

### Flutter Integration

```dart
// Example Flutter code for image upload
Future<Map<String, dynamic>> detectCatConditions(File imageFile) async {
  var request = http.MultipartRequest(
    'POST', 
    Uri.parse('http://localhost:8000/detect/cats')
  );
  
  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path)
  );
  
  var response = await request.send();
  var responseBody = await response.stream.bytesToString();
  
  if (response.statusCode == 200) {
    return json.decode(responseBody);
  } else {
    throw Exception('Detection failed: $responseBody');
  }
}
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png) 
- BMP (.bmp)
- TIFF (.tiff, .tif)

## File Size Limits

- Maximum file size: 10MB per image

## Model Information

### Cats Model
- **Classes:** Alopecia, Eosinophilic Plague, Miliary Dermatitis, ear mite, feline acne, flea, fleas, ringworm
- **Input size:** 640x640
- **Format:** TensorFlow Lite (.tflite)

### Dogs Model  
- **Classes:** dermatitis, fleas, fungal_infection, hotspot, mange, pyoderma, ringworm, ticks, unknown_abnormality
- **Input size:** 640x640
- **Format:** TensorFlow Lite (.tflite)

## Development

The code is structured with helper functions for easy maintenance:

- `load_model()` - Load YOLO models from .tflite files
- `load_labels()` - Load class labels from JSON files
- `load_metadata()` - Load model metadata from YAML files  
- `run_inference()` - Execute detection and format results
- `validate_image()` - Validate uploaded image files
- `process_detection()` - Main detection pipeline

Models are cached on first use for better performance.