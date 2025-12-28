# Docker Setup Guide - InstaIntelli

Complete guide for setting up and running InstaIntelli using Docker.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Configuration](#environment-configuration)
- [Service Details](#service-details)
- [Development Workflow](#development-workflow)
- [Database Management](#database-management)
- [Troubleshooting](#troubleshooting)
- [Common Commands](#common-commands)

---

## Prerequisites

### Required Software

1. **Docker Desktop** (Windows/Mac) or **Docker Engine + Docker Compose** (Linux)
   - Download: https://www.docker.com/products/docker-desktop
   - For Windows: Requires WSL 2 (Windows Subsystem for Linux)
   - Minimum version: Docker 20.10+, Docker Compose 2.0+

2. **Git** (for cloning the repository)

### System Requirements

- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: At least 10GB free
- **CPU**: Multi-core processor recommended

### Windows Setup

1. Install WSL 2:
   ```powershell
   wsl --install
   ```
   Restart your computer after installation.

2. Install Docker Desktop:
   - Download from https://www.docker.com/products/docker-desktop
   - Enable WSL 2 integration in Docker Desktop settings
   - Restart Docker Desktop

3. Verify installation:
   ```powershell
   docker --version
   docker-compose --version
   ```

---

## Quick Start

### 1. Clone and Navigate to Project

```bash
cd C:\Alisha\Projects\university\big_data_project
```

### 2. Create Environment File

Copy the example environment file:

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Or manually create .env file
```

Edit `.env` and add your API keys:
- `OPENAI_API_KEY` or `GROK_API_KEY`
- `SECRET_KEY` (generate a random string)

### 3. Start All Services

```bash
# Using Docker Compose directly
docker-compose up -d --build

# Or using Make (if available)
make build
make up

# Or using PowerShell script
.\scripts\docker-commands.ps1 build
.\scripts\docker-commands.ps1 up
```

### 4. Verify Services

Check that all services are running:

```bash
docker-compose ps
```

You should see:
- ✅ `instaintelli_postgres` (healthy)
- ✅ `instaintelli_mongodb` (healthy)
- ✅ `instaintelli_redis` (healthy)
- ✅ `instaintelli_minio` (healthy)
- ✅ `instaintelli_chromadb` (healthy)
- ✅ `instaintelli_backend` (healthy)
- ✅ `instaintelli_frontend` (running)

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (minioadmin / minioadmin123)

---

## Environment Configuration

### Creating `.env` File

The `.env.example` file contains all required environment variables. Copy it to `.env`:

```bash
cp .env.example .env
```

### Required Variables

#### Application Settings
```env
SECRET_KEY=your-secret-key-here  # Generate a random string
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

#### LLM Provider (Choose One)

**Option 1: OpenAI**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**Option 2: Grok (xAI)**
```env
LLM_PROVIDER=grok
GROK_API_KEY=xai-...
```

### Port Configuration

Default ports (can be changed in `.env`):
- **PostgreSQL**: 5433 (to avoid conflict with local PostgreSQL on 5432)
- **MongoDB**: 27018 (to avoid conflict with local MongoDB on 27017)
- **Redis**: 6380 (to avoid conflict with local Redis on 6379)
- **ChromaDB**: 8001 (to avoid conflict with backend on 8000)
- **Backend API**: 8000
- **Frontend**: 3000
- **MinIO API**: 9000
- **MinIO Console**: 9001

---

## Service Details

### PostgreSQL (Hassan - Auth & Users)

- **Container**: `instaintelli_postgres`
- **Image**: `postgres:15-alpine`
- **Port**: 5433 (host) → 5432 (container)
- **Default Credentials**:
  - User: `postgres`
  - Password: `postgres123`
  - Database: `instaintelli`
- **Data Persistence**: `postgres_data` volume
- **Health Check**: Automatic via `pg_isready`

**Access from Host:**
```bash
psql -h localhost -p 5433 -U postgres -d instaintelli
```

**Access from Container:**
```bash
docker-compose exec postgres psql -U postgres -d instaintelli
```

### MongoDB (Sami - Posts)

- **Container**: `instaintelli_mongodb`
- **Image**: `mongo:7`
- **Port**: 27018 (host) → 27017 (container)
- **Default Credentials**:
  - User: `mongodb`
  - Password: `mongodb123`
  - Database: `instaintelli`
- **Data Persistence**: `mongodb_data` volume
- **Health Check**: Automatic via `mongosh ping`

**Access from Host:**
```bash
mongosh mongodb://mongodb:mongodb123@localhost:27018/instaintelli?authSource=admin
```

**Access from Container:**
```bash
docker-compose exec mongodb mongosh instaintelli
```

### Redis (Alisha - Caching)

- **Container**: `instaintelli_redis`
- **Image**: `redis:7-alpine`
- **Port**: 6380 (host) → 6379 (container)
- **Data Persistence**: `redis_data` volume (AOF enabled)
- **Health Check**: Automatic via `redis-cli ping`

**Access from Host:**
```bash
redis-cli -h localhost -p 6380
```

**Access from Container:**
```bash
docker-compose exec redis redis-cli
```

### MinIO (Sami - Object Storage)

- **Container**: `instaintelli_minio`
- **Image**: `minio/minio:latest`
- **Ports**: 
  - API: 9000
  - Console: 9001
- **Default Credentials**:
  - Access Key: `minioadmin`
  - Secret Key: `minioadmin123`
- **Data Persistence**: `minio_data` volume
- **Health Check**: Automatic via HTTP endpoint

**Access Console:**
- URL: http://localhost:9001
- Login with default credentials above

**Create Bucket:**
1. Open MinIO Console
2. Navigate to "Buckets"
3. Create bucket: `instaintelli-media`

### ChromaDB (Raza - Vector Database)

- **Container**: `instaintelli_chromadb`
- **Image**: `chromadb/chroma:latest`
- **Port**: 8001 (host) → 8000 (container)
- **Data Persistence**: `chromadb_data` volume
- **Health Check**: Automatic via API heartbeat

**Access API:**
```bash
curl http://localhost:8001/api/v1/heartbeat
```

### Backend (FastAPI)

- **Container**: `instaintelli_backend`
- **Base Image**: `python:3.11-slim`
- **Port**: 8000
- **Hot Reload**: Enabled (code changes auto-reload)
- **Health Check**: http://localhost:8000/health

**View Logs:**
```bash
docker-compose logs -f backend
```

**Run Commands:**
```bash
docker-compose exec backend /bin/bash
```

### Frontend (React + Vite)

- **Container**: `instaintelli_frontend`
- **Base Image**: `node:18-alpine`
- **Port**: 3000
- **Hot Reload**: Enabled (code changes auto-reload)

**View Logs:**
```bash
docker-compose logs -f frontend
```

---

## Development Workflow

### Starting Development

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Make code changes:**
   - Backend: Edit files in `backend/` - changes auto-reload
   - Frontend: Edit files in `frontend/` - changes auto-reload

### Running Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest tests/test_search.py

# Run with coverage
docker-compose exec backend pytest --cov=app
```

### Database Migrations

```bash
# Create a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback last migration
docker-compose exec backend alembic downgrade -1
```

### Rebuilding After Dependency Changes

If you update `requirements.txt` or `package.json`:

```bash
# Rebuild and restart
docker-compose up -d --build

# Or rebuild specific service
docker-compose build backend
docker-compose up -d backend
```

### Stopping Services

```bash
# Stop all services (keeps containers)
docker-compose stop

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove everything including volumes
docker-compose down -v
```

---

## Database Management

### Initializing Databases

Databases are automatically initialized on first start. To manually initialize:

```bash
# PostgreSQL (runs Alembic migrations)
docker-compose exec postgres bash /app/scripts/init_postgres.sh

# MongoDB (creates collections and indexes)
docker-compose exec mongodb bash /app/scripts/init_mongodb.sh
```

### Accessing Databases

**PostgreSQL:**
```bash
docker-compose exec postgres psql -U postgres -d instaintelli
```

**MongoDB:**
```bash
docker-compose exec mongodb mongosh instaintelli
```

**Redis:**
```bash
docker-compose exec redis redis-cli
```

### Backup and Restore

**PostgreSQL Backup:**
```bash
docker-compose exec postgres pg_dump -U postgres instaintelli > backup.sql
```

**PostgreSQL Restore:**
```bash
docker-compose exec -T postgres psql -U postgres instaintelli < backup.sql
```

**MongoDB Backup:**
```bash
docker-compose exec mongodb mongodump --out /data/backup
```

**MongoDB Restore:**
```bash
docker-compose exec mongodb mongorestore /data/backup
```

---

## Troubleshooting

### Services Won't Start

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Check port conflicts:**
   ```bash
   # Windows PowerShell
   netstat -ano | findstr :8000
   netstat -ano | findstr :3000
   ```

3. **View service logs:**
   ```bash
   docker-compose logs <service-name>
   # Example: docker-compose logs backend
   ```

4. **Check service health:**
   ```bash
   docker-compose ps
   ```

### Backend Won't Connect to Databases

1. **Verify services are healthy:**
   ```bash
   docker-compose ps
   ```
   All services should show "healthy" status.

2. **Check environment variables:**
   ```bash
   docker-compose exec backend env | grep POSTGRES
   docker-compose exec backend env | grep MONGODB
   ```

3. **Test database connections:**
   ```bash
   docker-compose exec backend python -c "from app.db.postgres import engine; print('PostgreSQL OK')"
   ```

### Frontend Can't Connect to Backend

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Verify CORS settings in `.env`:**
   ```env
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
   ```

3. **Check frontend environment:**
   ```bash
   docker-compose exec frontend env | grep VITE_API_URL
   ```

### Out of Disk Space

Docker volumes can grow large. Clean up:

```bash
# Remove unused volumes
docker volume prune

# Remove everything (careful!)
docker system prune -a --volumes
```

### Slow Performance

1. **Increase Docker resources:**
   - Docker Desktop → Settings → Resources
   - Increase CPU and Memory allocation

2. **Check container resource usage:**
   ```bash
   docker stats
   ```

### ChromaDB Issues

If ChromaDB fails to start:

1. **Check logs:**
   ```bash
   docker-compose logs chromadb
   ```

2. **Restart ChromaDB:**
   ```bash
   docker-compose restart chromadb
   ```

3. **If persistent issues, remove volume and restart:**
   ```bash
   docker-compose down
   docker volume rm big_data_project_chromadb_data
   docker-compose up -d chromadb
   ```

---

## Common Commands

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up -d --build

# Execute command in container
docker-compose exec <service> <command>
```

### Using Makefile (Linux/Mac/WSL)

```bash
make build      # Build images
make up         # Start services
make down       # Stop services
make logs       # View logs
make test       # Run tests
make migrate    # Run migrations
make health     # Check health
```

### Using PowerShell Script (Windows)

```powershell
.\scripts\docker-commands.ps1 build
.\scripts\docker-commands.ps1 up
.\scripts\docker-commands.ps1 down
.\scripts\docker-commands.ps1 logs
.\scripts\docker-commands.ps1 health
```

### Quick Health Check

```bash
# Check all services
docker-compose ps

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000

# Test ChromaDB
curl http://localhost:8001/api/v1/heartbeat
```

---

## Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/

---

## Support

For issues or questions:
1. Check service logs: `docker-compose logs <service>`
2. Verify environment variables in `.env`
3. Check this troubleshooting section
4. Review Docker Desktop resource allocation

---

**Last Updated**: 2024
**Project**: InstaIntelli - AI-powered Social Media Platform

