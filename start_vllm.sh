#!/bin/bash

# vLLM Server Startup Script
echo "🚀 Starting vLLM Vision Inference Server..."
echo "=========================================="

# Check if CUDA is available
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected"
    nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader,nounits
else
    echo "⚠️  No NVIDIA GPU detected - running on CPU (slow)"
fi

# Wait a moment for any initialization
sleep 2

echo "📦 Loading Qwen2.5-VL-3B-Instruct model..."
echo "⏳ This may take a few minutes on first run..."

# Start the vLLM server
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-VL-3B-Instruct \
  --port 8801 \
  --host 0.0.0.0 \
  --max-model-len 2048 \
  --gpu-memory-utilization 0.9 \
  --trust-remote-code \
  --served-model-name Qwen/Qwen2.5-VL-3B-Instruct

echo "🛑 vLLM server stopped"
