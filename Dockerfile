# ==============================================================================
# PashuDrishti.ai - Production Multi-Stage Dockerfile for AWS App Runner / ECS
# Optimized for CPU Inference (sub-second latency, lightweight image size)
# ==============================================================================

FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed for compiling or image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install lightweight CPU-only PyTorch to avoid massive CUDA binaries (~4GB -> ~250MB)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn boto3

# ==============================================================================
# Runner Stage
# ==============================================================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Install runtime libraries (libgomp for PyTorch OpenMP execution, curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for cloud security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

# Copy python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and model bundle
COPY --chown=appuser:appuser backend/ /app/backend/
COPY --chown=appuser:appuser cattle_model_low_hw.tar.gz /app/cattle_model_low_hw.tar.gz

USER appuser

# Environment configurations
ENV PORT=8000 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    MODEL_BUNDLE=/app/cattle_model_low_hw.tar.gz \
    DB_PATH=/app/data/app.db \
    WEB_CONCURRENCY=2

EXPOSE 8000

# Docker healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production server: Gunicorn managing 2 Uvicorn async worker processes
CMD ["sh", "-c", "gunicorn -w ${WEB_CONCURRENCY:-2} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT:-8000} backend.app:app"]
