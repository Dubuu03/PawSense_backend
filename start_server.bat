@echo off
echo YOLO Detection FastAPI Backend Setup
echo =====================================
echo.

echo Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Running setup validation...
python test_setup.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Setup validation failed
    pause
    exit /b 1
)

echo.
echo Starting FastAPI server (Modular Architecture)...
echo Server will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo.
echo Choose startup method:
echo [1] Run via app.main (Direct)
echo [2] Run via root main.py (Wrapper)
echo [3] Run with uvicorn directly
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo Starting directly from app.main...
    python -m app.main
) else if "%choice%"=="2" (
    echo Starting via root main.py...
    python main.py
) else if "%choice%"=="3" (
    echo Starting with uvicorn...
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
) else (
    echo Invalid choice, using direct app.main...
    python -m app.main
)