#!/usr/bin/env python3
"""
Validation script for TensorFlow Lite setup
"""

import sys

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing Python imports...")
    
    try:
        # Test basic imports
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import PIL
        print("✅ Pillow imported successfully")
        
        import numpy
        print("✅ NumPy imported successfully")
        
        import yaml
        print("✅ PyYAML imported successfully")
        
        import requests
        print("✅ Requests imported successfully")
        
        # Test TensorFlow Lite Runtime import
        import tflite_runtime.interpreter as tflite
        print("✅ TensorFlow Lite Runtime imported successfully")
        
        # Test application modules
        print("\n🔧 Testing application modules...")
        
        from app.main import create_app
        print("✅ FastAPI app creation successful")
        
        app = create_app()
        print(f"✅ App instantiated: {app.title}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Run validation"""
    print("🔍 TensorFlow Lite Detection API - Setup Validation")
    print("=" * 60)
    
    if test_imports():
        print("\n✅ All tests passed! The application should work correctly.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()