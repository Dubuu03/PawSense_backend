FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Set Python environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Test basic imports
RUN python -c "import fastapi, numpy, PIL, tflite_runtime; print('✅ Core dependencies OK')"

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
