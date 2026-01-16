# ============================================
# INSTAINTELLI - Backend Dockerfile
# ============================================
# FastAPI Backend Container
# Uses Python 3.11 for compatibility with all dependencies

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# - gcc: Required for building some Python packages
# - postgresql-client: For database operations
# - curl: For health checks
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt from project root
# Note: docker-compose.yml sets context to root (.), so this path is correct
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ ./backend/

# Set working directory to backend for proper imports
WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application with hot-reload for development
# --reload enables auto-reload on code changes
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

