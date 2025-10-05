#!/bin/bash

# Docker Build and Run Script for vLLM Vision Inference

echo "🐳 vLLM Vision Inference - Docker Setup"
echo "======================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# # Check if NVIDIA Docker runtime is available
# if ! docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi &> /dev/null; then
#     echo "⚠️  NVIDIA Docker runtime not available. GPU acceleration may not work."
#     echo "   Install nvidia-docker2 for GPU support."
# fi

echo "✅ Prerequisites check passed"

# Create necessary directories
mkdir -p pres_images
touch chat_history_.txt

echo "📦 Building Docker containers..."

# Build and start services
if [ "$1" = "--detach" ] || [ "$1" = "-d" ]; then
    echo "🚀 Starting services in background..."
    docker compose up --build -d
    echo "✅ Services started in background"
    echo "📱 Gradio Interface: http://localhost:7860"
    echo "🔧 vLLM API: http://localhost:8801/v1"
    echo "📊 View logs: docker-compose logs -f"
else
    echo "🚀 Starting services..."
    docker compose up --build
fi
