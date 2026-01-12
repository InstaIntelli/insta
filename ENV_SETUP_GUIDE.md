# Environment Variables Setup Guide

## Quick Fix for Your Current .env

Your `.env` file has some inconsistencies. Here's what needs to be fixed:

### **Key Issues:**

1. **Docker Service Names vs Localhost**: When running in Docker, you must use Docker service names (e.g., `postgres`, `mongodb`, `redis`) instead of `localhost`.

2. **Missing Variables**: Some variables used by the code are missing.

3. **Inconsistent URLs**: Some URLs use service names while hosts use localhost.

## ✅ Corrected .env File

Replace your current `.env` with this corrected version:

```bash
# ============================================
# APPLICATION
# ============================================
APP_NAME=InstaIntelli
APP_ENV=development
DEBUG=True
SECRET_KEY=zxaKKgc-wqceske9nCgw5DIKxYLe01AgmMSRKWOHlzo
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# ============================================
# POSTGRESQL
# ============================================
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_DB=instaintelli
POSTGRES_URL=postgresql://postgres:postgres123@postgres:5432/instaintelli

# ============================================
# MONGODB
# ============================================
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_USER=mongodb
MONGODB_PASSWORD=mongodb123
MONGODB_DB=instaintelli
MONGODB_URL=mongodb://mongodb:mongodb123@mongodb:27017/instaintelli?authSource=admin
MONGODB_DATABASE=instaintelli
MONGODB_POSTS_COLLECTION=posts

# ============================================
# REDIS
# ============================================
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_URL=redis://redis:6379/0

# ============================================
# MINIO
# ============================================
MINIO_ENDPOINT=minio
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_BUCKET_NAME=instaintelli-media
MINIO_USE_SSL=False

# ============================================
# CHROMADB
# ============================================
VECTOR_DB_TYPE=chroma
CHROMA_HOST=chromadb
CHROMA_PORT=8000
CHROMA_COLLECTION_NAME=instaintelli_embeddings
CHROMA_PERSIST_PATH=./chroma_db

# ============================================
# NEO4J
# ============================================
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j123
NEO4J_PORT=7474
NEO4J_BOLT_PORT=7687

# ============================================
# OPENAI
# ============================================
OPENAI_API_KEY=your-actual-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_BASE_URL=https://api.openai.com/v1
LLM_PROVIDER=openai

# ============================================
# RAG CONFIGURATION
# ============================================
RAG_TOP_K_RESULTS=5
RAG_SIMILARITY_THRESHOLD=0.7
RAG_CHUNK_SIZE=512
RAG_CHUNK_OVERLAP=50

# ============================================
# FRONTEND
# ============================================
VITE_API_URL=http://localhost:8000
REACT_APP_API_URL=http://localhost:8000
```

## 🔧 Changes Made

### 1. **Fixed Service Names** (for Docker)
- Changed `POSTGRES_HOST=localhost` → `POSTGRES_HOST=postgres`
- Changed `MONGODB_HOST=localhost` → `MONGODB_HOST=mongodb`
- Changed `REDIS_HOST=localhost` → `REDIS_HOST=redis`
- Changed `MINIO_ENDPOINT=localhost` → `MINIO_ENDPOINT=minio`
- Changed `CHROMA_HOST=localhost` → `CHROMA_HOST=chromadb`

### 2. **Fixed URLs**
- `POSTGRES_URL`: Uses `postgres:5432` (Docker service name)
- `MONGODB_URL`: Uses `mongodb:27017` (Docker service name)
- `REDIS_URL`: Uses `redis:6379` (Docker service name)
- `MINIO_ENDPOINT`: Uses `minio:9000` (Docker service name)

### 3. **Added Missing Variables**
- `MONGODB_DATABASE=instaintelli`
- `MONGODB_POSTS_COLLECTION=posts`
- `CHROMA_PERSIST_PATH=./chroma_db`
- `LLM_PROVIDER=openai`
- `VITE_API_URL=http://localhost:8000` (for Vite frontend)

### 4. **Fixed MINIO_SECRET_KEY**
- Changed from `minioadmin` to `minioadmin123` (matches docker-compose.yml)

## 📝 Important Notes

### **Docker vs Local Development**

**When running with Docker Compose:**
- Use Docker service names: `postgres`, `mongodb`, `redis`, `minio`, `chromadb`, `neo4j`
- The `docker-compose.yml` will override some values anyway, but having correct defaults helps

**When running locally (without Docker):**
- Use `localhost` for all hosts
- Make sure services are running on your local machine

### **Environment-Specific Files**

You can create separate files:
- `.env.docker` - For Docker deployment
- `.env.local` - For local development

Then use:
```bash
# For Docker
cp .env.docker .env

# For local
cp .env.local .env
```

## ✅ Verification

After updating your `.env`, verify it works:

```bash
# Check if backend can read config
docker-compose exec backend python -c "from app.core.config import settings; print('✅ Config loaded:', settings.APP_NAME)"

# Check database connections
docker-compose logs backend | grep -i "connected\|error"
```

## 🚀 Next Steps

1. **Update your `.env` file** with the corrected values above
2. **Add your OpenAI API key** (replace `your-actual-api-key-here`)
3. **Restart services**: `docker-compose restart backend`
4. **Test the application**: Visit http://localhost:3000

## 🔒 Security Reminder

- **Never commit `.env` to Git**
- **Generate a new SECRET_KEY** for production
- **Use strong passwords** in production
- **Rotate API keys** regularly

