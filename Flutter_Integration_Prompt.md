# Flutter Frontend Integration Prompt for YOLO Detection Backend

## 🎯 **Project Overview**
I need to integrate my existing Flutter app with a FastAPI YOLO detection backend for pet skin condition assessment. The backend is fully functional and provides endpoints for cats and dogs detection.

## 🏗️ **Current Flutter Structure**
```
lib/
├── pages/
│   ├── assessment_page.dart          # Pet type selection (cats/dogs)
│   ├── assessment_step_one.dart      # Pet details form
│   ├── assessment_step_two.dart      # Image upload functionality
│   └── assessment_step_three.dart    # Results display
```

## 🔌 **Backend API Details**

### **Base URL:** `http://localhost:8000` (or your server IP)

### **Endpoints:**
- `GET /health` - Health check
- `POST /detect/cats` - Cat skin condition detection
- `POST /detect/dogs` - Dog skin condition detection

### **Request Format:**
```
Content-Type: multipart/form-data
Body: file (image file)
```

### **Response Format:**
```json
{
  "filename": "pet_image.jpg",
  "model_info": {
    "description": "Ultralytics best model trained on data.yaml",
    "author": "Ultralytics",
    "version": "8.3.203",
    "task": "detect",
    "names": {
      "0": "condition_name",
      "1": "another_condition"
    }
  },
  "detections": [
    {
      "class_id": 0,
      "label": "Alopecia",
      "confidence": 0.8542,
      "bbox": [123.45, 67.89, 234.56, 178.90]
    }
  ],
  "total_detections": 2
}
```

## 📱 **Flutter Integration Requirements**

### **1. assessment_page.dart (Type Selection)**
- Modify existing file to add pet type selection
- Add radio buttons or cards for "Cats" and "Dogs" selection
- Store selected pet type and navigate to assessment_step_one.dart

### **2. assessment_step_one.dart (Pet Details)**
- Enhance existing pet details form
- Add fields needed for assessment:
```dart
String petName;
String petType; // from assessment_page.dart selection
int petAge;
String breed;
String ownerName;
```

### **3. assessment_step_two.dart (Image Upload)**
- Modify existing image upload functionality
- Add API integration to your backend:
```dart
// Image upload to backend
- Camera/Gallery selection (existing)
- API call to http://your-server:8000/detect/{petType}
- Handle multipart/form-data upload
- Show upload progress
```

### **4. assessment_step_three.dart (Results Display)**
- Enhance existing results page to show:
```dart
// Display API response
- Detection results from backend
- Confidence scores
- Bounding box data
- Pet assessment summary
```

## 🛠️ **Technical Implementation**

### **Required Packages (Add to existing pubspec.yaml):**
```yaml
dependencies:
  http: ^1.1.0  # For API calls to your backend
  # Keep your existing dependencies
```

### **HTTP Service Class (Add to your project):**
```dart
class PetDetectionService {
  static const String baseUrl = 'http://your-server-ip:8000';
  
  // Call this from assessment_step_two.dart
  static Future<Map<String, dynamic>> detectConditions({
    required File imageFile,
    required String petType, // 'cats' or 'dogs' from assessment_page
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/detect/$petType'),
    );
    
    request.files.add(
      await http.MultipartFile.fromPath('file', imageFile.path),
    );
    
    var response = await request.send();
    var responseBody = await response.stream.bytesToString();
    
    if (response.statusCode == 200) {
      return json.decode(responseBody);
    } else {
      throw Exception('Detection failed: $responseBody');
    }
  }
}
```

### **Data Models:**
```dart
class DetectionResult {
  final String filename;
  final ModelInfo modelInfo;
  final List<Detection> detections;
  final int totalDetections;
}

class Detection {
  final int classId;
  final String label;
  final double confidence;
  final List<double> bbox; // [x1, y1, x2, y2]
}

class PetAssessment {
  final String petName;
  final String petType;
  final List<File> images;
  final DetectionResult? result;
  final DateTime createdAt;
}
```

## 🎨 **UI/UX Requirements**

### **Design Specifications:**
- **Color Scheme:** Use pet-friendly colors (blue/green for trust, warm colors for comfort)
- **Navigation:** Step indicator showing progress (1/3, 2/3, 3/3)
- **Responsive:** Support different screen sizes
- **Accessibility:** Screen reader support, high contrast mode

### **assessment_step_one.dart modifications:**
```dart
// Add/modify existing form fields:
- Pet name (text input)
- Pet age (number input)  
- Breed (text input or dropdown)
- Pass petType from assessment_page.dart
```

### **assessment_step_two.dart modifications:**
```dart
// Enhance existing image upload:
- Keep existing camera/gallery functionality
- Add API call after image selection:
  
  Future<void> uploadAndAnalyze(File imageFile, String petType) async {
    try {
      final result = await PetDetectionService.detectConditions(
        imageFile: imageFile,
        petType: petType,
      );
      // Navigate to assessment_step_three with results
    } catch (e) {
      // Show error message
    }
  }
```

### **assessment_step_three.dart modifications:**
```dart
// Enhance existing results display:
- Show detection results from API response
- Display confidence percentages
- List detected conditions
- Show assessment summary
```

## 🔄 **Data Flow Between Your Existing Files**

```dart
// assessment_page.dart → assessment_step_one.dart
String selectedPetType; // Pass to next step

// assessment_step_one.dart → assessment_step_two.dart  
Map<String, dynamic> petDetails = {
  'name': petName,
  'age': petAge, 
  'breed': breed,
  'type': selectedPetType,
};

// assessment_step_two.dart → assessment_step_three.dart
Map<String, dynamic> detectionResults; // From API response
```

## 🛡️ **Error Handling**

### **Network Errors:**
```dart
// Handle these scenarios:
- Server unreachable
- Timeout errors
- Invalid image format
- File size too large
- Server internal errors
- No internet connection

// User-friendly error messages:
- "Unable to connect to server"
- "Image file too large (max 10MB)"
- "Invalid image format"
- "Detection service unavailable"
```

## 📊 **Integration Tasks for Your Existing Files**

### **assessment_page.dart:**
- [ ] Add pet type selection (cats/dogs)
- [ ] Store selected type for next step

### **assessment_step_one.dart:**
- [ ] Receive pet type from previous step
- [ ] Validate and store pet details

### **assessment_step_two.dart:**
- [ ] Add API integration after image upload
- [ ] Call backend detection endpoint
- [ ] Handle loading states and errors

### **assessment_step_three.dart:**
- [ ] Display API detection results
- [ ] Show confidence scores and conditions
- [ ] Format results for user display

## 🧪 **Testing Requirements**

### **Test Scenarios:**
```dart
// Unit tests:
- HTTP service methods
- Data model serialization
- Form validation logic

// Widget tests:
- Step navigation flow
- Image upload functionality
- Results display accuracy

// Integration tests:
- End-to-end assessment flow
- Backend API integration
- Error handling scenarios
```

## 🔧 **Configuration**

### **Environment Setup:**
```dart
// config.dart
class AppConfig {
  static const String apiBaseUrl = 'http://192.168.1.100:8000'; // Your IP
  static const int maxImagesPerAssessment = 5;
  static const int maxImageSizeBytes = 10 * 1024 * 1024; // 10MB
  static const List<String> supportedImageTypes = ['jpg', 'jpeg', 'png'];
}
```

## 🎯 **Success Criteria**

### **Functional Requirements:**
- [x] Successful API communication with backend
- [ ] Smooth step-by-step navigation
- [ ] Accurate detection results display
- [ ] Proper error handling and user feedback
- [ ] Image upload with progress indication
- [ ] Results visualization with bounding boxes

### **Performance Requirements:**
- Image upload < 10 seconds for 5MB file
- Results display < 2 seconds after API response
- Smooth 60fps navigation between steps
- Memory efficient image handling

## 📝 **Implementation Steps**

### **Step 1: assessment_page.dart**
1. Add pet type selection UI
2. Store selection in state/variable
3. Navigate to step one with selected type

### **Step 2: assessment_step_one.dart** 
1. Receive pet type from previous page
2. Add/modify pet details form
3. Pass all data to step two

### **Step 3: assessment_step_two.dart**
1. Keep existing image upload functionality  
2. Add API call to your backend after image selection
3. Handle API response and navigate to results

### **Step 4: assessment_step_three.dart**
1. Receive detection results from step two
2. Display results in user-friendly format
3. Show detected conditions and confidence scores

---

**Modify your existing Flutter files (assessment_page.dart, assessment_step_one.dart, assessment_step_two.dart, assessment_step_three.dart) to integrate with your FastAPI backend. Focus on adding the API integration to your current flow without changing the overall structure.**