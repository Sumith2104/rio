# =============================================================================
# PACD-RAG: AI-Powered Smart Campus Intelligence & Student Success Platform
# Production Multi-Stage Dockerfile
# Author: Sumith U (SRN: R24EA807) | REVA University
# =============================================================================

FROM python:3.10-slim

# Prevent Python from buffering stdout and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    SECONDARY_PORT=8002

WORKDIR /app

# Install minimal OS dependencies for compilation and healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Expose primary and secondary dashboard ports
EXPOSE 8000
EXPOSE 8002

# Health check against the primary portal endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start the master unified runner
CMD ["python", "app.py"]

