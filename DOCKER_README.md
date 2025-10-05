# vLLM Vision Inference - Docker Setup

Complete Docker containerization for the vLLM Vision Inference project with separate backend and frontend containers.

## 🏗️ Architecture

- **Backend Container**: Runs vLLM server with Qwen2.5-VL-3B-Instruct model
- **Frontend Container**: Runs Gradio web interface
- **Docker Compose**: Orchestrates both containers with proper networking

## 📁 Files Structure

```
vllm_inference/
├── Dockerfile.backend          # vLLM server container
├── Dockerfile.frontend         # Gradio interface container
├── docker-compose.yml          # Container orchestration
├── start_vllm.sh              # vLLM server startup script
├── requirements.docker.txt    # Docker-specific dependencies
├── gradio_app.py              # Gradio application
├── pres_images/               # Sample images directory
└── chat_history_.txt          # Chat history storage
```

## 🚀 Quick Start

### Prerequisites

1. **Docker & Docker Compose** installed
2. **NVIDIA Docker Runtime** (for GPU support)
3. **NVIDIA GPU** with CUDA support

### Build and Run

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Configuration

### Environment Variables

**Backend Container:**
- `CUDA_VISIBLE_DEVICES=0` - GPU device selection
- `NVIDIA_VISIBLE_DEVICES=0` - NVIDIA GPU visibility

**Frontend Container:**
- `BACKEND_URL=http://backend:8801` - Backend service URL
- `GRADIO_SERVER_NAME=0.0.0.0` - Gradio server binding
- `GRADIO_SERVER_PORT=7860` - Gradio server port

### Ports

- **Backend**: `8801` - vLLM API server
- **Frontend**: `7860` - Gradio web interface

### Volumes

- `./pres_images:/app/pres_images:ro` - Read-only image directory
- `./chat_history_.txt:/app/chat_history_.txt` - Chat history persistence

## 🐳 Container Details

### Backend Container (vLLM Server)

**Base Image**: `nvidia/cuda:12.1-devel-ubuntu22.04`
**Features**:
- CUDA 12.1 support
- vLLM server with Qwen2.5-VL-3B-Instruct
- GPU memory optimization
- Health checks
- Auto-restart on failure

**Startup Command**:
```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-VL-3B-Instruct \
  --port 8801 \
  --host 0.0.0.0 \
  --max-model-len 2048 \
  --gpu-memory-utilization 0.9 \
  --trust-remote-code
```

### Frontend Container (Gradio Interface)

**Base Image**: `python:3.11-slim`
**Features**:
- Lightweight Python environment
- Gradio web interface
- Backend health checking
- Auto-restart on failure

**Startup Process**:
1. Wait for backend to be ready
2. Start Gradio interface
3. Connect to backend via internal network

## 🔍 Monitoring

### Health Checks

Both containers include health checks:

**Backend Health Check**:
```bash
curl -f http://localhost:8801/v1/models
```

**Frontend Health Check**:
```bash
curl -f http://localhost:7860
```

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

## 🛠️ Development

### Building Individual Containers

```bash
# Build backend only
docker build -f Dockerfile.backend -t vllm-backend .

# Build frontend only
docker build -f Dockerfile.frontend -t vllm-frontend .
```

### Running Individual Containers

```bash
# Run backend
docker run --gpus all -p 8801:8801 vllm-backend

# Run frontend (after backend is running)
docker run -p 7860:7860 -e BACKEND_URL=http://host.docker.internal:8801 vllm-frontend
```

## 🔧 Troubleshooting

### Common Issues

1. **GPU Not Detected**:
   ```bash
   # Check NVIDIA Docker runtime
   docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi
   ```

2. **Backend Not Ready**:
   ```bash
   # Check backend logs
   docker-compose logs backend
   
   # Check if model is downloading
   docker-compose exec backend nvidia-smi
   ```

3. **Frontend Can't Connect**:
   ```bash
   # Check network connectivity
   docker-compose exec frontend curl http://backend:8801/v1/models
   ```

4. **Port Conflicts**:
   ```bash
   # Check port usage
   netstat -tulpn | grep :8801
   netstat -tulpn | grep :7860
   ```

### Performance Optimization

1. **GPU Memory**:
   - Adjust `--gpu-memory-utilization` in startup script
   - Monitor with `nvidia-smi`

2. **Model Loading**:
   - First run downloads model (~6GB)
   - Subsequent runs are faster

3. **Container Resources**:
   - Adjust memory limits in docker-compose.yml
   - Use resource constraints for production

## 🌐 Access

Once running, access the services:

- **Gradio Interface**: http://localhost:7860
- **vLLM API**: http://localhost:8801/v1
- **API Documentation**: http://localhost:8801/docs

## 📝 Notes

- **First Run**: Model download takes 5-10 minutes
- **GPU Memory**: Requires ~8GB VRAM minimum
- **Storage**: Model cache stored in container
- **Networking**: Containers communicate via Docker network
- **Persistence**: Chat history saved to host filesystem

## 🔄 Updates

To update the application:

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```
