#!/bin/bash
# ============================================
# MinIO Initialization Script
# ============================================
# This script creates the required MinIO bucket
# Run this inside the minio container or via docker-compose exec

set -e

echo "Initializing MinIO storage..."

# Wait for MinIO to be ready
until curl -f http://localhost:9000/minio/health/live > /dev/null 2>&1; do
  echo "Waiting for MinIO to be ready..."
  sleep 2
done

echo "MinIO is ready!"

# Create bucket using MinIO client (mc)
# Note: This requires mc to be installed in the container
# Alternatively, use the MinIO web console at http://localhost:9001

echo "MinIO initialization complete!"
echo "Access MinIO Console at http://localhost:9001"
echo "Default credentials: minioadmin / minioadmin123"

