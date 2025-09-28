#!/usr/bin/env python3
"""
Debug script to test the Railway deployment and identify Flutter integration issues
"""
import requests
import json
import os

# API Configuration
API_BASE_URL = "https://pawsensebackend-production.up.railway.app"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_file_upload(model_type="dogs"):
    """Test file upload similar to Flutter"""
    print(f"\n🔍 Testing File Upload for {model_type}...")
    
    # Create a dummy image file for testing
    test_image_path = "test_image.jpg"
    if not os.path.exists(test_image_path):
        # Create a small test JPEG image
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(test_image_path, 'JPEG')
        print(f"✅ Created test image: {test_image_path}")
    
    try:
        with open(test_image_path, 'rb') as f:
            files = {'file': ('scaled_43.jpg', f, 'image/jpeg')}
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'PawSense-Flutter/1.0'
            }
            
            print(f"📤 Sending request to: {API_BASE_URL}/detect/{model_type}")
            print(f"📋 Headers: {headers}")
            print(f"📂 File info: scaled_43.jpg, image/jpeg")
            
            response = requests.post(
                f"{API_BASE_URL}/detect/{model_type}",
                files=files,
                headers=headers,
                timeout=30
            )
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📥 Response Headers: {dict(response.headers)}")
            print(f"📥 Response Body: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Found {result.get('total_detections', 0)} detections")
                return True
            else:
                print(f"❌ Failed with status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print(f"🧹 Cleaned up test image")

def main():
    print("🐾 PawSense Backend Debug Script")
    print("=" * 50)
    
    # Test health
    health_ok = test_health()
    
    if health_ok:
        # Test file upload for both models
        test_file_upload("cats")
        test_file_upload("dogs")
    else:
        print("❌ Health check failed, skipping file upload tests")
    
    print("\n" + "=" * 50)
    print("🏁 Debug complete!")

if __name__ == "__main__":
    main()