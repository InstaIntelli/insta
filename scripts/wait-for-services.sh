#!/bin/bash
# ============================================
# Wait for Services Script
# ============================================
# Utility script to wait for services to be ready
# Used by backend container to ensure dependencies are available

set -e

echo "Waiting for services to be ready..."

# Wait for PostgreSQL
until pg_isready -h postgres -U "${POSTGRES_USER:-postgres}" > /dev/null 2>&1; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done
echo "PostgreSQL is ready!"

# Wait for MongoDB
until mongosh --host mongodb --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
  echo "Waiting for MongoDB..."
  sleep 2
done
echo "MongoDB is ready!"

# Wait for Redis
until redis-cli -h redis ping > /dev/null 2>&1; do
  echo "Waiting for Redis..."
  sleep 2
done
echo "Redis is ready!"

# Wait for MinIO
until curl -f http://minio:9000/minio/health/live > /dev/null 2>&1; do
  echo "Waiting for MinIO..."
  sleep 2
done
echo "MinIO is ready!"

# Wait for ChromaDB
until curl -f http://chromadb:8000/api/v1/heartbeat > /dev/null 2>&1; do
  echo "Waiting for ChromaDB..."
  sleep 2
done
echo "ChromaDB is ready!"

echo "All services are ready!"








