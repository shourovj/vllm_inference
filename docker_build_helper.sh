#!/bin/bash

# Docker Build Helper Script
echo "🐳 vLLM Docker Build Helper"
echo "=========================="

echo "Available Dockerfile options:"
echo "1. CUDA 12.0 (recommended for modern GPUs)"
echo "2. CUDA 11.8 (compatible with older GPUs)"
echo "3. CPU-only (for testing without GPU)"

read -p "Choose option (1-3): " choice

case $choice in
    1)
        echo "Using CUDA 12.0 Dockerfile..."
        cp Dockerfile.backend Dockerfile.backend.active
        ;;
    2)
        echo "Using CUDA 11.8 Dockerfile..."
        cp Dockerfile.backend.cuda11 Dockerfile.backend.active
        ;;
    3)
        echo "Using CPU-only Dockerfile..."
        cp Dockerfile.backend.cpu Dockerfile.backend.active
        ;;
    *)
        echo "Invalid choice. Using CUDA 12.0 as default..."
        cp Dockerfile.backend Dockerfile.backend.active
        ;;
esac

echo "✅ Dockerfile selected. Now building..."

# Update docker-compose to use the active Dockerfile
sed -i 's/dockerfile: Dockerfile.backend/dockerfile: Dockerfile.backend.active/' docker-compose.yml

# Build and run
docker compose up --build -d

echo "🚀 Services started!"
echo "📱 Gradio Interface: http://localhost:7860"
echo "🔧 vLLM API: http://localhost:8801/v1"
