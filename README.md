# 🐄 PashuDrishti.ai - AI-Assisted Cattle & Buffalo Breed Recognition

> A production-ready Docker containerized AI/ML system for accurately identifying Indian cattle and buffalo breeds from images using deep learning.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Latest-red?logo=pytorch)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

**PashuDrishti.ai** leverages EfficientNet-B0 and PyTorch to recognize Indian cattle and buffalo breeds with high accuracy. The system is fully containerized with Docker for easy deployment and scaling.

- 🐳 **Docker Containerized** - Deploy anywhere with a single container
- 🚀 **Production-Ready FastAPI Web App** - Optimized for performance
- 📸 **Intelligent Image Prediction** - Upload images for instant breed classification
- 🔐 **User Authentication** - Secure sign-in and account management
- 📍 **GPS Integration** - Track livestock location with coordinates
- 💾 **Pre-trained Models** - Quantized & TorchScript export for edge deployment
- 🌐 **Scalable Deployment** - Docker Compose for multi-service orchestration

## 📋 Prerequisites

- Docker & Docker Compose installed ([Installation Guide](https://docs.docker.com/get-docker/))
- 4GB+ RAM recommended
- Model bundle: `cattle_model_low_hw.tar.gz` (pre-trained model)

## 🚀 Quick Start with Docker

### Option 1: Docker Run (Single Container)

```bash
# Clone the repository
git clone https://github.com/varshith0810/PashuDrishti.ai.git
cd PashuDrishti.ai

# Build the Docker image
docker build -t pashudrishti:latest .

# Run the container
docker run -d \
  --name pashudrishti \
  -p 8000:8000 \
  -e MODEL_BUNDLE=cattle_model_low_hw.tar.gz \
  -v $(pwd)/cattle_model_low_hw.tar.gz:/app/cattle_model_low_hw.tar.gz \
  pashudrishti:latest
```

Access the app: **http://localhost:8000**

### Option 2: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/varshith0810/PashuDrishti.ai.git
cd PashuDrishti.ai

# Start services
docker-compose up -d

# View logs
docker-compose logs -f web
```

Access the app: **http://localhost:8000**

### Option 3: Using Docker Hub (Pre-built Image)

```bash
docker run -d \
  --name pashudrishti \
  -p 8000:8000 \
  -v $(pwd)/cattle_model_low_hw.tar.gz:/app/cattle_model_low_hw.tar.gz \
  varshith0810/pashudrishti:latest
```

## 🐳 Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

# Run application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: pashudrishti-web
    ports:
      - "8000:8000"
    volumes:
      - ./cattle_model_low_hw.tar.gz:/app/cattle_model_low_hw.tar.gz
      - ./models:/app/models
      - ./data:/app/data
    environment:
      - MODEL_BUNDLE=cattle_model_low_hw.tar.gz
      - SESSION_SECRET=${SESSION_SECRET:-change-me-in-production}
      - DEBUG_BUNDLE=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s

  # Optional: PostgreSQL for future database needs
  # db:
  #   image: postgres:13
  #   environment:
  #     POSTGRES_DB: pashudrishti
  #     POSTGRES_USER: ${DB_USER:-postgres}
  #     POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
  #   volumes:
  #     - db_data:/var/lib/postgresql/data
  #   restart: unless-stopped

volumes:
  # db_data:
  pashudrishti_data:
```

## 📦 Building & Publishing Docker Image

### Build Locally

```bash
# Build image
docker build -t pashudrishti:latest .

# Tag for Docker Hub (optional)
docker tag pashudrishti:latest varshith0810/pashudrishti:latest

# Push to Docker Hub (requires login)
docker login
docker push varshith0810/pashudrishti:latest
```

### Building with Custom Tags

```bash
# Tag with version
docker build -t pashudrishti:v1.0 .

# Tag with multiple labels
docker build \
  -t varshith0810/pashudrishti:latest \
  -t varshith0810/pashudrishti:v1.0 \
  .
```

## 🌐 Deployment Options

### AWS ECS (Elastic Container Service)

```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker tag pashudrishti:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/pashudrishti:latest

docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/pashudrishti:latest
```

### Google Cloud Run

```bash
# Build and deploy
gcloud run deploy pashudrishti \
  --source . \
  --platform managed \
  --region us-central1 \
  --port 8000 \
  --memory 2Gi \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
# Push to Azure Container Registry
az acr login --name myregistry

docker tag pashudrishti:latest myregistry.azurecr.io/pashudrishti:latest

docker push myregistry.azurecr.io/pashudrishti:latest

# Deploy
az container create \
  --resource-group myResourceGroup \
  --name pashudrishti \
  --image myregistry.azurecr.io/pashudrishti:latest \
  --ports 8000 \
  --cpu 2 \
  --memory 2
```

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml pashudrishti

# Check status
docker stack services pashudrishti
```

### Kubernetes (Helm)

```bash
# Create Kubernetes deployment YAML
kubectl apply -f kubernetes/deployment.yaml

# Or use Helm (if chart available)
helm install pashudrishti ./helm-chart
```

## ⚙️ Environment Variables

| Variable | Default | Purpose | Required |
|----------|---------|---------|----------|
| `MODEL_BUNDLE` | `cattle_model_low_hw.tar.gz` | Path to model bundle | ✅ Yes |
| `SESSION_SECRET` | *(auto-generated)* | Session signing key (use strong value in production) | ✅ Yes |
| `DEBUG_BUNDLE` | `false` | Enable model inspection endpoint | ❌ No |
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) | ❌ No |
| `WORKERS` | `4` | Number of Uvicorn worker processes | ❌ No |

### Set Environment Variables

**In Docker run:**
```bash
docker run -e SESSION_SECRET=your-secret-key -e DEBUG_BUNDLE=true ...
```

**In docker-compose.yml:**
```yaml
environment:
  - SESSION_SECRET=your-secret-key
  - DEBUG_BUNDLE=true
  - LOG_LEVEL=debug
```

**With .env file:**
```bash
# Create .env file
echo "SESSION_SECRET=your-strong-secret-key" > .env
echo "DEBUG_BUNDLE=false" >> .env

# Use with docker-compose
docker-compose --env-file .env up -d
```

## 📂 Model Bundle Setup

### Download Model Bundle

1. Download `cattle_model_low_hw.tar.gz` from project releases
2. Place in repository root

### Mount Model in Docker

```bash
# Bind mount (editable)
docker run -v /path/to/cattle_model_low_hw.tar.gz:/app/cattle_model_low_hw.tar.gz ...

# Docker Compose volume
volumes:
  - ./cattle_model_low_hw.tar.gz:/app/cattle_model_low_hw.tar.gz
```

### Verify Model in Container

```bash
# Inspect model bundle
docker run -e DEBUG_BUNDLE=true pashudrishti:latest

# Access debug endpoint
curl http://localhost:8000/debug/bundle
```

## 🎯 Using the Application

### 1. Create Account
- Navigate to: `http://localhost:8000/create-account`
- Enter username and password

### 2. Sign In
- Go to: `http://localhost:8000/signin`
- Use your credentials

### 3. Upload & Predict
- Upload an animal image
- *(Optional)* Enter Animal ID
- *(Optional)* Enter GPS coordinates (format: `lat,long`)
- Submit to view:
  - Predicted breed
  - Confidence score
  - Top 5 predictions
  - Image preview
  - Location details

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check & model status |
| `/` | GET | Main prediction interface |
| `/signin` | GET/POST | User login |
| `/create-account` | GET/POST | User registration |
| `/logout` | GET | Clear session |
| `/predict` | POST | Image upload & breed prediction |
| `/debug/bundle` | GET | Inspect model bundle *(DEBUG mode only)* |

## 🔍 Container Management

### View Logs

```bash
# Docker run
docker logs pashudrishti

# Docker Compose
docker-compose logs -f web

# Real-time logs with timestamps
docker logs --timestamps pashudrishti
```

### Stop/Start Container

```bash
# Stop
docker stop pashudrishti

# Start
docker start pashudrishti

# Restart
docker restart pashudrishti
```

### Remove Container

```bash
# Stop and remove
docker rm -f pashudrishti

# Clean up all images and containers
docker system prune -a
```

### Container Statistics

```bash
# View resource usage
docker stats pashudrishti

# View container details
docker inspect pashudrishti
```

## 💾 Data Persistence

### Using Volumes

```bash
# Create named volume
docker volume create pashudrishti-data

# Use in docker run
docker run -v pashudrishti-data:/app/data ...

# Use in docker-compose
volumes:
  pashudrishti-data:
    driver: local
```

### Bind Mounts

```bash
# Mount local directory
docker run -v $(pwd)/data:/app/data ...
```

### Backup & Restore

```bash
# Backup volume
docker run --rm -v pashudrishti-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/data.tar.gz -C /data .

# Restore volume
docker run --rm -v pashudrishti-data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/data.tar.gz -C /data
```

## 🛡️ Security Best Practices

### 1. Use Strong Session Secret

```bash
# Generate strong secret
openssl rand -hex 32

# Use in production
docker run -e SESSION_SECRET=$(openssl rand -hex 32) ...
```

### 2. Run as Non-Root User

Update Dockerfile:
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 3. Read-Only Filesystem

```bash
docker run --read-only -v /tmp:/tmp pashudrishti:latest
```

### 4. Resource Limits

```bash
docker run -m 2g --cpus 2 pashudrishti:latest
```

## 🐛 Troubleshooting

### Container Fails to Start

```bash
# Check logs
docker logs pashudrishti

# Inspect container
docker inspect pashudrishti

# Run with interactive shell
docker run -it pashudrishti:latest /bin/bash
```

### Model Bundle Not Found

```bash
# Verify volume mount
docker run -v pashudrishti-data:/app/data ...

# Check inside container
docker exec pashudrishti ls -la /app/

# Ensure file exists
ls -la cattle_model_low_hw.tar.gz
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Use different port
docker run -p 8001:8000 pashudrishti:latest
```

### High Memory Usage

```bash
# Limit memory in docker-compose
services:
  web:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Database Connection Issues

```bash
# Check Docker network
docker network ls

# Connect containers to same network
docker network create pashudrishti-net

docker run --network pashudrishti-net pashudrishti:latest
```

## 📊 Production Deployment Checklist

- [ ] Use strong `SESSION_SECRET`
- [ ] Enable health checks
- [ ] Set resource limits (CPU, memory)
- [ ] Use read-only filesystem where possible
- [ ] Configure logging driver
- [ ] Setup monitoring & alerts
- [ ] Use external secrets management (Docker Secrets)
- [ ] Enable container image scanning
- [ ] Use specific image tags (not `latest`)
- [ ] Implement automated backups
- [ ] Setup CI/CD pipeline for image builds
- [ ] Document environment variables
- [ ] Test disaster recovery procedures

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: docker/build-push-action@v2
        with:
          push: true
          tags: varshith0810/pashudrishti:latest
```

## 📈 Performance Optimization

### Multi-Stage Build

```dockerfile
FROM python:3.9 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0"]
```

### Worker Configuration

```bash
docker run -e WORKERS=8 pashudrishti:latest
```

## 📝 Project Structure

```
PashuDrishti.ai/
├── src/
│   ├── app.py                 # Main FastAPI application
│   ├── config.py              # Breed list & configuration
│   ├── infer.py               # Local prediction logic
│   ├── preprocess.py          # Dataset validation
│   ├── train.py               # Training script
│   └── web_app.py             # Web app wrapper
├── backend/
│   ├── app.py                 # FastAPI compatibility wrapper
│   ├── db.py                  # SQLite database helpers
│   ├── schema.sql             # Database schema
│   └── ml/                    # ML utilities
├── scripts/
│   ├── export_low_hardware.py # Model optimization
│   └── run_pipeline.sh        # Training pipeline
├── Dockerfile                 # Container image definition
├── docker-compose.yml         # Multi-container orchestration
├── requirements.txt           # Python dependencies
├── cattle_model_low_hw.tar.gz # Pre-trained model
└── README.md                  # This file
```

## 📦 Tech Stack

- **Framework:** FastAPI
- **ML:** PyTorch + EfficientNet-B0
- **Container:** Docker & Docker Compose
- **Database:** SQLite (upgradeable to PostgreSQL)
- **Model Format:** TorchScript, Int8 Quantized
- **Deployment:** Cloud-native (AWS, GCP, Azure, Kubernetes)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙋 Support

For issues, questions, or suggestions:
1. Open a GitHub Issue
2. Check troubleshooting section above
3. Review container logs

---

**Made with ❤️ for livestock farmers and veterinarians**
