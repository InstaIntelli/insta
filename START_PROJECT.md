# 🚀 How to Start InstaIntelli

## Prerequisites

1. **Docker Desktop** - Must be running
   - Download: https://www.docker.com/products/docker-desktop
   - Make sure Docker Desktop is **started** before proceeding

2. **Git** (if cloning from repository)

3. **OpenAI API Key** (for AI features)

---

## Step 1: Start Docker Desktop

**Windows:**
- Open Docker Desktop from Start Menu
- Wait until it shows "Docker Desktop is running" in the system tray

**Verify Docker is running:**
```bash
docker ps
```
Should show running containers (or empty list, not an error).

---

## Step 2: Configure Environment Variables

1. **Copy `.env.example` to `.env`** (if it exists) or create `.env` file in project root

2. **Set your OpenAI API Key:**
   ```bash
   OPENAI_API_KEY=your-actual-openai-api-key-here
   ```

3. **Verify key settings in `.env`:**
   - `POSTGRES_HOST=postgres` (not `localhost` - Docker service name)
   - `MONGODB_HOST=mongodb` (not `localhost`)
   - `REDIS_HOST=redis` (not `localhost`)
   - `MINIO_ENDPOINT=minio:9000` (not `localhost`)
   - `CHROMA_HOST=chromadb` (not `localhost`)
   - `NEO4J_URI=bolt://neo4j:7687`

   **Important:** When running in Docker, use Docker service names, not `localhost`!

---

## Step 3: Pull Neo4j Image (if needed)

If you encounter Neo4j pull errors, manually pull it first:
```bash
docker pull neo4j:latest
```

---

## Step 4: Start All Services

**From project root directory:**
```bash
docker-compose up -d
```

This will:
- Pull required images (if not already downloaded)
- Create Docker network
- Start all services:
  - PostgreSQL (port 5433)
  - MongoDB (port 27018)
  - Redis (port 6379)
  - MinIO (ports 9000-9001)
  - ChromaDB (port 8001)
  - Neo4j (ports 7474, 7687)
  - Backend API (port 8000)
  - Frontend (port 3000)

**First time startup takes 2-5 minutes** (downloading images, initializing databases).

---

## Step 5: Verify Services Are Running

**Check all containers:**
```bash
docker-compose ps
```

**Expected output:**
- All services should show `Up` status
- Health checks may show `(health: starting)` initially - wait 1-2 minutes

**Check backend logs:**
```bash
docker-compose logs backend --tail 50
```

Look for:
- ✅ `Application startup complete`
- ✅ `Uvicorn running on http://0.0.0.0:8000`
- ❌ No `ModuleNotFoundError` or connection errors

**Check frontend logs:**
```bash
docker-compose logs frontend --tail 50
```

---

## Step 6: Access the Application

### Frontend (React)
- **URL:** http://localhost:3000
- Open in browser

### Backend API
- **URL:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Health Check:** http://localhost:8000/health

### Database Access

**PostgreSQL:**
```bash
docker-compose exec postgres psql -U postgres -d instaintelli
```

**MongoDB:**
```bash
docker-compose exec mongodb mongosh -u mongodb -p mongodb123
```

**Redis:**
```bash
docker-compose exec redis redis-cli
```

**Neo4j Browser:**
- **URL:** http://localhost:7474
- **Username:** `neo4j`
- **Password:** `neo4j123` (or your `.env` value)

**MinIO Console:**
- **URL:** http://localhost:9001
- **Username:** `minioadmin`
- **Password:** `minioadmin`

---

## Step 7: Test the Application

1. **Create an account:**
   - Go to http://localhost:3000
   - Sign up with email/password

2. **Upload a post:**
   - Upload an image with caption
   - Wait a few seconds for AI processing

3. **Test search:**
   - Use semantic search to find posts
   - Try the chatbot feature

4. **Test social features:**
   - Follow users
   - Like posts
   - Add comments

---

## Troubleshooting

### ❌ "Docker daemon not running"
**Fix:** Start Docker Desktop

### ❌ "Neo4j pull failed" / "no such host"
**Fix:**
```bash
docker pull neo4j:latest
# Then retry: docker-compose up -d
```

### ❌ Backend shows "ModuleNotFoundError: No module named 'neo4j'"
**Fix:**
```bash
docker-compose build backend
docker-compose up -d backend
```

### ❌ "Connection refused" errors
**Fix:**
1. Check `.env` uses Docker service names (not `localhost`)
2. Wait 1-2 minutes for services to fully start
3. Check health: `docker-compose ps`

### ❌ Frontend can't connect to backend
**Fix:**
- Verify `REACT_APP_API_URL=http://localhost:8000` in `.env`
- Check backend is running: `docker-compose logs backend`

### ❌ Images not loading
**Fix:**
- Check MinIO is healthy: `docker-compose ps minio`
- Verify backend image proxy endpoint works: http://localhost:8000/api/v1/posts/images/{object_path}

---

## Common Commands

**Stop all services:**
```bash
docker-compose down
```

**Stop and remove volumes (⚠️ deletes data):**
```bash
docker-compose down -v
```

**Restart a specific service:**
```bash
docker-compose restart backend
```

**View logs:**
```bash
docker-compose logs -f backend    # Follow logs
docker-compose logs backend --tail 100  # Last 100 lines
```

**Rebuild after code changes:**
```bash
docker-compose build backend
docker-compose up -d backend
```

**Check database health:**
```bash
curl http://localhost:8000/api/v1/health/databases
```

---

## Quick Start Summary

```bash
# 1. Start Docker Desktop

# 2. Navigate to project
cd C:\Alisha\Projects\university\big_data_project

# 3. Ensure .env is configured (especially OPENAI_API_KEY)

# 4. Start everything
docker-compose up -d

# 5. Wait 2-3 minutes, then check
docker-compose ps

# 6. Open browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

---

## Next Steps

- Read `ENV_SETUP_GUIDE.md` for cloud database setup
- Read `TESTING_GUIDE.md` for testing instructions
- Read `CLOUD_DB_SETUP_GUIDE.md` for production-ready cloud databases

---

**Need help?** Check logs: `docker-compose logs [service-name]`

