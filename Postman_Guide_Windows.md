# 📮 Postman Setup Guide for YOLO Detection API (Windows)

## 🚀 Quick Start

### 1. **Start Your Server**
```powershell
# In your backend directory
cd "D:\BSCS\CS - 4A\Thesis\backend"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. **Download Postman**
- Visit: https://www.postman.com/downloads/
- Download Postman for Windows
- Install and create a free account

## 📋 Postman Collection Setup

### **Request 1: Health Check**
```
Method: GET
URL: http://localhost:8000/health
Headers: (none needed)
Body: (none needed)
```

### **Request 2: Detect Cat Conditions**
```
Method: POST
URL: http://localhost:8000/detect/cats
Headers: 
  - Content-Type: multipart/form-data (auto-set)
Body: 
  - Type: form-data
  - Key: file
  - Type: File
  - Value: [Select your cat image]
```

### **Request 3: Detect Dog Conditions**
```
Method: POST
URL: http://localhost:8000/detect/dogs
Headers: 
  - Content-Type: multipart/form-data (auto-set)
Body: 
  - Type: form-data
  - Key: file
  - Type: File
  - Value: [Select your dog image]
```

## 📁 Step-by-Step Instructions

### **Step 1: Create New Collection**
1. Open Postman
2. Click "New" → "Collection"
3. Name it: "YOLO Detection API"
4. Save

### **Step 2: Add Health Check Request**
1. Right-click collection → "Add request"
2. Name: "Health Check"
3. Set method to `GET`
4. URL: `http://localhost:8000/health`
5. Click "Send"
6. Should return:
```json
{
  "status": "healthy",
  "models_loaded": ["cats", "dogs"],
  "available_models": ["cats", "dogs"]
}
```

### **Step 3: Add Cat Detection Request**
1. Right-click collection → "Add request"
2. Name: "Detect Cat Conditions"
3. Set method to `POST`
4. URL: `http://localhost:8000/detect/cats`
5. Go to "Body" tab
6. Select "form-data"
7. Add key: `file` (set type to "File")
8. Click "Select Files" and choose your cat image
9. Click "Send"

### **Step 4: Add Dog Detection Request**
1. Right-click collection → "Add request"
2. Name: "Detect Dog Conditions"
3. Set method to `POST`
4. URL: `http://localhost:8000/detect/dogs`
5. Go to "Body" tab
6. Select "form-data"
7. Add key: `file` (set type to "File")
8. Click "Select Files" and choose your dog image
9. Click "Send"

## 📊 Expected Response Format

### **Success Response (200 OK)**
```json
{
  "filename": "your_image.jpg",
  "model_info": {
    "description": "Ultralytics best model trained on data.yaml",
    "author": "Ultralytics",
    "version": "8.3.203",
    "task": "detect",
    "names": {
      "0": "Alopecia",
      "1": "Eosinophilic Plague",
      "2": "Miliary Dermatitis",
      "3": "ear mite",
      "4": "feline acne",
      "5": "flea",
      "6": "fleas", 
      "7": "ringworm"
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

### **Error Response (400/500)**
```json
{
  "error": "Invalid file type. Allowed types: image/jpeg, image/jpg, image/png, image/bmp, image/tiff",
  "model_type": "cats"
}
```

## 🎯 Troubleshooting

### **Common Issues & Solutions**

#### ❌ "Connection Error"
```
Solution: Make sure server is running
Command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### ❌ "405 Method Not Allowed"
```
Solution: Check HTTP method
- Health check: GET
- Detection endpoints: POST
```

#### ❌ "422 Validation Error"
```
Solution: Check file upload
- Body type: form-data
- Key name: file
- Key type: File (not Text)
```

#### ❌ "Invalid file type"
```
Solution: Use supported formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp) 
- TIFF (.tiff)
```

## 📂 Sample Windows File Paths

When selecting files in Postman, navigate to:
```
C:\Users\YourName\Pictures\your_image.jpg
D:\Images\cat_photo.png
C:\Desktop\dog_picture.jpeg
```

## 🔧 Advanced Postman Features

### **Environment Variables**
1. Create environment: "YOLO API"
2. Add variable: 
   - Name: `base_url`
   - Value: `http://localhost:8000`
3. Use in requests: `{{base_url}}/detect/cats`

### **Tests (Auto-validation)**
Add to "Tests" tab:
```javascript
// Test status code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test response structure
pm.test("Response has required fields", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('filename');
    pm.expect(jsonData).to.have.property('detections');
    pm.expect(jsonData).to.have.property('total_detections');
});

// Test detection format
pm.test("Detections have correct format", function () {
    const jsonData = pm.response.json();
    if (jsonData.detections.length > 0) {
        const detection = jsonData.detections[0];
        pm.expect(detection).to.have.property('class_id');
        pm.expect(detection).to.have.property('label');
        pm.expect(detection).to.have.property('confidence');
        pm.expect(detection).to.have.property('bbox');
    }
});
```

## 📱 Testing Different Images

### **Recommended Test Images**
1. **Clear cat/dog photos** - Should detect conditions if present
2. **Multiple animals** - Test multiple detections
3. **Poor quality images** - Test robustness
4. **Non-animal images** - Should return 0 detections
5. **Large images** - Test file size limits

### **Windows Image Sources**
- Sample Pictures: `C:\Users\Public\Pictures\Sample Pictures`
- Your Photos: `C:\Users\%USERNAME%\Pictures`
- Downloads: `C:\Users\%USERNAME%\Downloads`

## 🎉 Quick Test Checklist

- [ ] Server is running on port 8000
- [ ] Postman is installed and open
- [ ] Created collection "YOLO Detection API"
- [ ] Health check returns status "healthy"
- [ ] Can upload cat image to `/detect/cats`
- [ ] Can upload dog image to `/detect/dogs`
- [ ] Response includes detections array
- [ ] Confidence scores are between 0-1
- [ ] Bounding boxes are [x1,y1,x2,y2] format

**Happy Testing!** 🚀