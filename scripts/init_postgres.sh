#!/bin/bash
# ============================================
# PostgreSQL Initialization Script
# ============================================
# This script initializes the PostgreSQL database
# Run this inside the postgres container or via docker-compose exec

set -e

echo "Initializing PostgreSQL database..."

# Wait for PostgreSQL to be ready
until pg_isready -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-instaintelli}"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

echo "PostgreSQL is ready!"

# Run Alembic migrations if they exist
if [ -f "/app/backend/alembic.ini" ]; then
  echo "Running database migrations..."
  cd /app/backend
  alembic upgrade head
fi

echo "PostgreSQL initialization complete!"








