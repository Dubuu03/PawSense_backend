#!/bin/bash

echo "🚀 Starting PawSense Backend..."

# Check if required environment variables are set
if [ -z "$HF_CAT_MODEL_URL" ]; then
    echo "⚠️ Warning: HF_CAT_MODEL_URL not set"
fi

if [ -z "$HF_DOG_MODEL_URL" ]; then
    echo "⚠️ Warning: HF_DOG_MODEL_URL not set"
fi

# Set default PORT if not provided by Railway
export PORT=${PORT:-8000}

echo "📡 Starting server on port $PORT..."

# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1