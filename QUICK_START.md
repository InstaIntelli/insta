# 🚀 InstaIntelli - Quick Start Guide

## Prerequisites Check

```powershell
# Verify Docker is installed
docker --version
docker-compose --version
```

## 3-Step Setup

### Step 1: Create Environment File

```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit .env and add your API keys:
# - OPENAI_API_KEY or GROK_API_KEY
# - SECRET_KEY (generate a random string)
```

### Step 2: Start Services

```powershell
# Build and start all services
docker-compose up -d --build
```

### Step 3: Verify

```powershell
# Check all services are running
docker-compose ps

# Test backend
curl http://localhost:8000/health
```

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001

## Common Commands

```powershell
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after dependency changes
docker-compose up -d --build
```

## Using Helper Scripts

```powershell
# PowerShell script
.\scripts\docker-commands.ps1 up
.\scripts\docker-commands.ps1 logs
.\scripts\docker-commands.ps1 health
```

## Troubleshooting

**Services won't start?**
```powershell
docker-compose logs <service-name>
```

**Port conflicts?**
- Check `.env` for port settings
- Default ports: PostgreSQL 5433, MongoDB 27018, Redis 6380, ChromaDB 8001

**Need more help?**
See `DOCKER_SETUP.md` for detailed documentation.

