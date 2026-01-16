# InstaIntelli 🚀✨

> **AI-Powered Social Media Platform with Advanced Big Data Analytics**

InstaIntelli is a modern, Instagram-like social media platform powered by cutting-edge AI and big data technologies. Share photos, get AI-generated captions, search semantically, and chat with your memories using RAG (Retrieval Augmented Generation).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.2.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-green.svg)](https://fastapi.tiangolo.com/)

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🎯 What Makes InstaIntelli Special](#-what-makes-instaintelli-special)
- [🏗️ Architecture](#️-architecture)
- [📦 Prerequisites](#-prerequisites)
- [🚀 Quick Start (5 Minutes)](#-quick-start-5-minutes)
- [⚙️ Detailed Setup Guide](#️-detailed-setup-guide)
- [🎨 Using the Application](#-using-the-application)
- [📖 API Documentation](#-api-documentation)
- [🛠️ Development Guide](#️-development-guide)
- [🐛 Troubleshooting](#-troubleshooting)
- [🔧 Configuration Reference](#-configuration-reference)
- [📊 Database Schema](#-database-schema)
- [🔐 Security Features](#-security-features)
- [📈 Performance & Scalability](#-performance--scalability)
- [🤝 Contributing](#-contributing)
- [👥 Team](#-team)
- [📄 License](#-license)

---

## ✨ Features

### 🎨 User-Facing Features

| Feature | Description |
|---------|-------------|
| 📸 **Photo Sharing** | Upload and share beautiful photos with your network |
| 🤖 **AI Captions** | Automatic caption generation using GPT-4 |
| 🔍 **Semantic Search** | Find posts by meaning, not just keywords |
| 💬 **RAG Chat** | Chat with your posts using AI (ask questions about your memories) |
| 👤 **User Profiles** | Manage your profile and view others' posts |
| 🎨 **Beautiful UI** | Modern Instagram-like interface with dark mode |
| 🔐 **Multi-Factor Auth** | Secure your account with Google Authenticator |
| 📱 **Responsive Design** | Works perfectly on mobile, tablet, and desktop |

### 🏗️ Technical Features (Big Data Analytics)

| Feature | Technology |
|---------|------------|
| **Polyglot Persistence** | 5 specialized databases for optimal performance |
| **Vector Embeddings** | OpenAI embeddings + ChromaDB for semantic search |
| **Distributed Caching** | Redis for lightning-fast performance |
| **Object Storage** | MinIO (S3-compatible) for scalable image storage |
| **Microservices** | Modular, containerized architecture |
| **Real-time Processing** | Background AI processing with async tasks |
| **RAG System** | LangChain + OpenAI for intelligent chat |
| **Image Processing** | Automatic thumbnail generation with Pillow |

---

## 🎯 What Makes InstaIntelli Special?

InstaIntelli demonstrates **advanced big data concepts** in a real-world application:

1. **Polyglot Persistence**: Uses 5 different databases, each optimized for its specific use case
   - PostgreSQL for relational user data
   - MongoDB for flexible post metadata
   - Redis for high-speed caching
   - ChromaDB for vector embeddings
   - MinIO for object storage

2. **AI-Powered Features**: 
   - Automatic caption generation
   - Semantic search (find "sunset photos" even if you wrote "evening beach")
   - RAG chat (ask "What was I doing in March?" and get AI-powered answers)

3. **Production-Ready Architecture**:
   - Containerized with Docker
   - Scalable microservices design
   - Comprehensive error handling
   - Security best practices (JWT, MFA, bcrypt)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    InstaIntelli Platform                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌───────────────────────────┐    │
│  │   Frontend   │────────▶│    Backend (FastAPI)      │    │
│  │   (React)    │         │    Port: 8000             │    │
│  │ Port: 3000   │         └───────────┬───────────────┘    │
│  └──────────────┘                     │                      │
│                                       │                      │
│                   ┌───────────────────┼──────────────┐      │
│                   │                   │              │      │
│           ┌───────▼────┐      ┌──────▼──────┐  ┌───▼────┐ │
│           │ PostgreSQL │      │   MongoDB   │  │ Redis  │ │
│           │  (Users)   │      │   (Posts)   │  │(Cache) │ │
│           └────────────┘      └─────────────┘  └────────┘ │
│                                                              │
│           ┌───────────┐       ┌──────────────┐             │
│           │  ChromaDB │       │    MinIO     │             │
│           │ (Vectors) │       │  (Images)    │             │
│           └───────────┘       └──────────────┘             │
│                                                              │
│           ┌──────────────────────────────────┐             │
│           │      OpenAI API (External)       │             │
│           │  - GPT-4 (Captions)              │             │
│           │  - text-embedding-3-small        │             │
│           └──────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- React 18.2.0 with Vite
- React Router 6.20.0 for navigation
- Axios for API calls
- Modern CSS with theme support (light/dark mode)

**Backend:**
- FastAPI 0.104.1 (Python 3.14)
- SQLAlchemy 2.0.23 (ORM)
- Pydantic for validation
- JWT + MFA authentication
- Uvicorn ASGI server

**Databases:**
- PostgreSQL 15 - User authentication and profiles
- MongoDB 7 - Post metadata storage
- Redis 7 - Caching layer
- ChromaDB - Vector database for embeddings
- MinIO - S3-compatible object storage

**AI/ML:**
- OpenAI GPT-4o-mini for caption generation
- OpenAI text-embedding-3-small for embeddings
- LangChain for RAG implementation
- PyOTP for MFA/TOTP

**DevOps:**
- Docker & Docker Compose
- Containerized services
- Environment-based configuration

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

| Software | Version | Download Link | Purpose |
|----------|---------|---------------|---------|
| **Docker Desktop** | 20.10+ | [Download Docker](https://www.docker.com/products/docker-desktop) | Run all services |
| **Docker Compose** | 2.0+ | Included with Docker Desktop | Orchestrate containers |
| **Git** | 2.0+ | [Download Git](https://git-scm.com/downloads) | Clone repository |

### Required API Keys

| Service | Required | How to Get |
|---------|----------|------------|
| **OpenAI API Key** | ✅ Yes | [Get API Key](https://platform.openai.com/api-keys) |
| **Grok API Key** | ❌ Optional | Alternative to OpenAI |

### System Requirements

- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **Internet**: Required for AI features

---

## 🚀 Quick Start (5 Minutes)

Follow these steps to get InstaIntelli running on your machine:

### Step 1: Clone the Repository

```bash
git clone https://github.com/InstaIntelli/insta.git
cd insta
```

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env
```

**Edit the `.env` file and add your OpenAI API key:**

```bash
# Open .env in your favorite editor (VS Code, Notepad++, etc.)
# Find this line:
OPENAI_API_KEY=your-openai-api-key-here

# Replace with your actual key:
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

**Generate a SECRET_KEY (required for JWT tokens):**

**On Windows (PowerShell):**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**On macOS/Linux:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and add it to your `.env` file:
```bash
SECRET_KEY=your-generated-secret-key-here
```

### Step 3: Start All Services

```bash
# Build and start all containers (first time takes 5-10 minutes)
docker-compose up -d --build
```

**What's happening?**
- Docker is building images for all services
- Starting 7 containers (frontend, backend, postgres, mongodb, redis, chromadb, minio)
- Setting up databases and connections

**Wait for services to be ready (30-60 seconds):**
```bash
# Check if all services are running
docker-compose ps
```

You should see all services with status "Up":
```
NAME                    STATUS
backend                 Up
frontend                Up
postgres                Up
mongodb                 Up
redis                   Up
chromadb                Up
minio                   Up
```

### Step 4: Access the Application

**Open your browser and visit:**

| Service | URL | Purpose |
|---------|-----|---------|
| 🎨 **Frontend** | http://localhost:3000 | Main application |
| 🔧 **Backend API** | http://localhost:8000 | API endpoints |
| 📚 **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| 💾 **MinIO Console** | http://localhost:9001 | Object storage (login: minioadmin/minioadmin123) |

### Step 5: Create Your Account

1. Visit http://localhost:3000
2. Click **"Sign Up"** on the landing page
3. Fill in your details:
   - Username (e.g., johndoe)
   - Email (e.g., john@example.com)
   - Password (minimum 6 characters)
4. Click **"Sign Up"**
5. You'll be automatically logged in!

### Step 6: Upload Your First Post

1. Click the **"➕ Create"** button in the sidebar
2. Select an image from your computer
3. (Optional) Add a caption
4. Click **"Upload"**
5. Wait for AI to generate a caption (5-10 seconds)
6. View your post in the feed!

🎉 **Congratulations!** You're now using InstaIntelli!

---

## ⚙️ Detailed Setup Guide

### Installing Docker Desktop

#### Windows

1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Follow the setup wizard
4. Restart your computer
5. Open Docker Desktop
6. Wait for Docker to start (icon turns green)

#### macOS

1. Download Docker Desktop for Mac
2. Drag Docker.app to Applications folder
3. Open Docker from Applications
4. Grant necessary permissions
5. Wait for Docker to start

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
# Logout and login again
```

### Getting OpenAI API Key

1. Visit https://platform.openai.com/
2. Sign up or log in
3. Go to https://platform.openai.com/api-keys
4. Click **"Create new secret key"**
5. Name it "InstaIntelli"
6. Copy the key (starts with `sk-proj-...`)
7. **Save it immediately** (you can't see it again!)
8. Add it to your `.env` file

### Environment Configuration

Here's what each important variable does:

```bash
# Application Settings
APP_NAME=InstaIntelli           # Your app name
APP_ENV=development             # Environment (development/production)
DEBUG=true                      # Enable debug mode
SECRET_KEY=your-secret-key      # JWT token secret (CHANGE THIS!)
ALLOWED_ORIGINS=http://localhost:3000  # Frontend URL

# OpenAI Configuration
OPENAI_API_KEY=your-key-here    # OpenAI API key (REQUIRED)
OPENAI_MODEL=gpt-4o-mini        # Model for captions
OPENAI_EMBEDDING_MODEL=text-embedding-3-small  # Model for search

# Database Ports (only change if you have conflicts)
POSTGRES_PORT=5433              # PostgreSQL port
MONGODB_PORT=27018              # MongoDB port
REDIS_PORT=6380                 # Redis port
MINIO_PORT=9000                 # MinIO port
CHROMA_PORT=8001                # ChromaDB port
```

---

## 🎨 Using the Application

### Landing Page

When you first visit http://localhost:3000, you'll see:
- Animated gradient background
- Phone mockup with rotating screenshots
- Feature showcase
- **"Log In"** and **"Sign Up"** buttons

### Creating an Account

1. Click **"Sign Up"**
2. Enter your details:
   - **Username**: Choose a unique username (letters, numbers, underscore)
   - **Email**: Your email address
   - **Password**: At least 6 characters
   - **Confirm Password**: Must match
3. Click **"Sign Up"**
4. You're in! Welcome to InstaIntelli 🎉

### Uploading a Post

1. Click **"➕ Create"** in the sidebar (or bottom nav on mobile)
2. **Select Image**: Click to browse or drag & drop
3. **Add Caption** (optional): Write something about your photo
4. Click **"Upload Post"**
5. **AI Processing**: 
   - AI analyzes your image
   - Generates a creative caption
   - Creates embeddings for semantic search
   - Stores in multiple databases
6. **Done!** Your post appears in the feed

### Semantic Search

**Traditional Search**: Find posts that contain exact words
**Semantic Search**: Find posts by meaning!

**Example:**
- Search: "sunset beach photos"
- Results: Posts with "evening ocean", "dusk seaside", "twilight shore", etc.

**How to use:**
1. Click **"🔍 Search"** in sidebar
2. Enter your search query
3. Select number of results (1-20)
4. Click **"Search"**
5. View semantically similar posts!

### RAG Chat (Chat with Your Posts)

**What is RAG?**
RAG (Retrieval Augmented Generation) lets you ask questions about your posts, and AI answers based on your actual content.

**Examples:**
- "What was I doing in summer?"
- "Show me my beach photos"
- "Tell me about my travel posts"

**How to use:**
1. Click **"💬 Chat"** in sidebar
2. Type your question
3. Click **"Send"**
4. AI retrieves relevant posts
5. Generates intelligent answer
6. Shows source posts used

### Dark Mode Toggle

1. Look for the **🌙** or **☀️** button in sidebar
2. Click to toggle between light and dark mode
3. Preference is saved automatically
4. Works across all pages

### Multi-Factor Authentication (MFA)

**Secure your account with Google Authenticator!**

1. Go to your profile
2. Click **"Enable MFA"**
3. Scan QR code with Google Authenticator app
4. Enter 6-digit code to verify
5. Save recovery codes (important!)
6. MFA is now active

**Next login:**
- Enter email & password
- Enter 6-digit code from Google Authenticator
- Access granted!

---

## 📖 API Documentation

### Interactive API Docs

Visit http://localhost:8000/docs for interactive Swagger UI where you can:
- See all available endpoints
- Try API calls directly
- View request/response schemas
- Test authentication

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "john@example.com",
  "username": "johndoe",
  "password": "SecurePass123"
}

Response:
{
  "user": {
    "user_id": "user_abc123",
    "email": "john@example.com",
    "username": "johndoe",
    "mfa_enabled": false
  },
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response (No MFA):
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": { ... }
}

Response (MFA Required):
{
  "mfa_required": true,
  "user_id": "user_abc123"
}
```

### Post Endpoints

#### Upload Post
```http
POST /api/v1/posts/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <image_file>
user_id: "user_abc123"
text: "Check out this amazing sunset!"

Response:
{
  "post_id": "post_xyz789",
  "status": "uploaded",
  "image_url": "http://localhost:9000/instaintelli/originals/post_xyz789.jpg",
  "thumbnail_url": "http://localhost:9000/instaintelli/thumbnails/post_xyz789.jpg"
}
```

#### Get Feed
```http
GET /api/v1/posts/feed?limit=50&skip=0
Authorization: Bearer <token>

Response:
{
  "posts": [
    {
      "post_id": "post_xyz789",
      "user_id": "user_abc123",
      "username": "johndoe",
      "text": "Amazing sunset!",
      "caption": "A breathtaking view of nature's beauty 🌅",
      "image_url": "...",
      "thumbnail_url": "...",
      "created_at": "2025-12-29T10:00:00Z"
    }
  ],
  "count": 1
}
```

### AI Endpoints

#### Process Post
```http
POST /api/v1/ai/process_post
Authorization: Bearer <token>
Content-Type: application/json

{
  "post_id": "post_xyz789",
  "user_id": "user_abc123",
  "text": "Beautiful sunset at the beach"
}

Response:
{
  "status": "processing_started",
  "post_id": "post_xyz789"
}
```

### Search Endpoints

#### Semantic Search
```http
POST /api/v1/search/semantic
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "sunset beach photos",
  "n_results": 10
}

Response:
{
  "query": "sunset beach photos",
  "results": [
    {
      "post_id": "post_xyz789",
      "text": "Beautiful evening at the shore",
      "similarity": 0.89,
      "image_url": "...",
      "user_id": "user_abc123"
    }
  ],
  "count": 1,
  "cached": false
}
```

#### RAG Chat
```http
POST /api/v1/search/chat
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "Tell me about my beach photos",
  "n_results": 5
}

Response:
{
  "query": "Tell me about my beach photos",
  "answer": "You have several beautiful beach photos from your summer vacation. The sunset shots from Malibu beach are particularly stunning...",
  "sources": [
    {
      "post_id": "post_xyz789",
      "text": "Sunset at Malibu",
      "similarity": 0.92
    }
  ]
}
```

---

## 🛠️ Development Guide

### Running Without Docker (Local Development)

#### Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make sure databases are running (via Docker or locally)
# Then start the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

#### Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at http://localhost:3000

### Useful Docker Commands

```bash
# View all services
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Stop and remove all data (CAUTION: Deletes databases!)
docker-compose down -v

# Rebuild a specific service
docker-compose up -d --build backend

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# View resource usage
docker stats
```

### Database Access

#### PostgreSQL
```bash
# Access PostgreSQL shell
docker-compose exec postgres psql -U postgres -d instaintelli

# Common queries
\dt                          # List tables
SELECT * FROM users;         # View users
\d users                     # Describe users table
\q                          # Quit
```

#### MongoDB
```bash
# Access MongoDB shell
docker-compose exec mongodb mongosh instaintelli -u mongodb -p mongodb123

# Common commands
show collections             # List collections
db.posts.find()             # View all posts
db.posts.findOne()          # View one post
db.posts.countDocuments()   # Count posts
exit                        # Quit
```

#### Redis
```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# Common commands
KEYS *                      # List all keys
GET search:query_hash       # Get cached value
FLUSHALL                    # Clear all cache (CAUTION!)
exit                        # Quit
```

---

## 🐛 Troubleshooting

### Issue: Services Won't Start

**Symptom**: `docker-compose up` fails or services crash

**Solutions**:

1. **Check Docker is running**:
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Check port conflicts**:
   ```bash
   # On Windows:
   netstat -ano | findstr :8000
   netstat -ano | findstr :3000
   
   # On macOS/Linux:
   lsof -i :8000
   lsof -i :3000
   ```
   
   If ports are in use, change them in `.env`:
   ```bash
   BACKEND_PORT=8001
   FRONTEND_PORT=3001
   ```

3. **Check logs**:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

4. **Restart Docker Desktop**:
   - Close Docker Desktop
   - Restart your computer
   - Start Docker Desktop
   - Try again

5. **Clean restart**:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

### Issue: Frontend Can't Connect to Backend

**Symptom**: API calls fail with "Network Error" or CORS errors

**Solutions**:

1. **Check backend is running**:
   ```bash
   docker-compose ps
   curl http://localhost:8000/docs
   ```

2. **Check CORS configuration** in `.env`:
   ```bash
   ALLOWED_ORIGINS=http://localhost:3000
   ```

3. **Check frontend API URL** in `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000'
   ```

4. **Restart both services**:
   ```bash
   docker-compose restart backend frontend
   ```

### Issue: OpenAI API Errors

**Symptom**: "OpenAI API Error" or "Invalid API Key"

**Solutions**:

1. **Verify API key**:
   - Check `.env` file
   - Key should start with `sk-proj-` or `sk-`
   - No extra spaces or quotes

2. **Test API key**:
   ```bash
   # On Windows (PowerShell):
   $headers = @{ "Authorization" = "Bearer YOUR_API_KEY" }
   Invoke-RestMethod -Uri "https://api.openai.com/v1/models" -Headers $headers
   
   # On macOS/Linux:
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

3. **Check API credits**:
   - Visit https://platform.openai.com/account/usage
   - Ensure you have credits available

4. **Use alternative model** (in `.env`):
   ```bash
   OPENAI_MODEL=gpt-3.5-turbo  # Cheaper alternative
   ```

### Issue: Database Connection Errors

**Symptom**: "Can't connect to PostgreSQL" or "MongoDB connection refused"

**Solutions**:

1. **Check database containers are running**:
   ```bash
   docker-compose ps postgres mongodb redis
   ```

2. **Wait for databases to initialize** (first startup takes 30-60 seconds):
   ```bash
   docker-compose logs -f postgres
   # Wait for: "database system is ready to accept connections"
   ```

3. **Restart database services**:
   ```bash
   docker-compose restart postgres mongodb redis
   ```

4. **Check database credentials** in `.env`:
   ```bash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres123
   ```

### Issue: Image Upload Fails

**Symptom**: "Upload failed" or "MinIO error"

**Solutions**:

1. **Check MinIO is running**:
   ```bash
   docker-compose ps minio
   curl http://localhost:9000/minio/health/live
   ```

2. **Check MinIO bucket exists**:
   - Visit http://localhost:9001
   - Login: minioadmin / minioadmin123
   - Verify "instaintelli" bucket exists

3. **Check image size**:
   - Maximum upload size: 10MB
   - Supported formats: JPG, PNG, GIF, WEBP

4. **Check disk space**:
   ```bash
   docker system df
   ```

### Issue: Semantic Search Returns No Results

**Symptom**: Search works but returns empty results

**Solutions**:

1. **Wait for AI processing**:
   - After uploading, wait 10-15 seconds
   - AI needs time to generate embeddings

2. **Check ChromaDB**:
   ```bash
   docker-compose logs chromadb
   docker-compose restart chromadb
   ```

3. **Re-process posts**:
   - Use API to trigger re-processing
   - Or delete and re-upload posts

### Issue: Docker Desktop Performance Issues

**Symptom**: Slow startup, high CPU/memory usage

**Solutions**:

1. **Increase Docker resources**:
   - Open Docker Desktop
   - Settings → Resources
   - Increase CPU: 4 cores
   - Increase Memory: 8GB
   - Apply & Restart

2. **Clean Docker**:
   ```bash
   docker system prune -a
   docker volume prune
   ```

3. **Limit service resources** in `docker-compose.yml`:
   ```yaml
   backend:
     mem_limit: 512m
     cpus: 1
   ```

### Still Having Issues?

1. **Check full logs**:
   ```bash
   docker-compose logs > logs.txt
   ```

2. **Check our documentation**: See `PROJECT_MANUAL.md` for detailed technical guide

3. **Common error messages**:

| Error | Solution |
|-------|----------|
| "Port already in use" | Change port in `.env` or stop conflicting service |
| "Cannot connect to Docker daemon" | Start Docker Desktop |
| "No space left on device" | Clean Docker: `docker system prune -a` |
| "Build failed" | Check internet connection, try `docker-compose build --no-cache` |
| "Container exited with code 1" | Check logs: `docker-compose logs <service>` |

---

## 🔧 Configuration Reference

### Complete `.env` File Example

```bash
# ============================================
# APPLICATION CONFIGURATION
# ============================================
APP_NAME=InstaIntelli
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-change-this-in-production
ALLOWED_ORIGINS=http://localhost:3000

# ============================================
# POSTGRESQL CONFIGURATION (User Database)
# ============================================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_DB=instaintelli
POSTGRES_HOST=postgres
POSTGRES_PORT=5433
POSTGRES_URL=postgresql://postgres:postgres123@postgres:5432/instaintelli

# ============================================
# MONGODB CONFIGURATION (Post Database)
# ============================================
MONGODB_USER=mongodb
MONGODB_PASSWORD=mongodb123
MONGODB_DB=instaintelli
MONGODB_HOST=mongodb
MONGODB_PORT=27018
MONGODB_URL=mongodb://mongodb:mongodb123@mongodb:27017/instaintelli?authSource=admin

# ============================================
# REDIS CONFIGURATION (Cache)
# ============================================
REDIS_HOST=redis
REDIS_PORT=6380
REDIS_URL=redis://redis:6379/0

# ============================================
# MINIO CONFIGURATION (Object Storage)
# ============================================
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_BUCKET_NAME=instaintelli
MINIO_SECURE=false

# ============================================
# CHROMADB CONFIGURATION (Vector Database)
# ============================================
CHROMA_HOST=chromadb
CHROMA_PORT=8001
CHROMA_COLLECTION_NAME=post_embeddings

# ============================================
# OPENAI CONFIGURATION (AI Features)
# ============================================
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_MAX_TOKENS=150
OPENAI_TEMPERATURE=0.7

# ============================================
# GROK CONFIGURATION (Alternative AI)
# ============================================
GROK_API_KEY=your-grok-api-key-optional
GROK_MODEL=grok-beta

# ============================================
# APPLICATION SETTINGS
# ============================================
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp
THUMBNAIL_SIZE=300
JWT_EXPIRATION_HOURS=24
CACHE_TTL_SECONDS=3600
```

### Port Configuration

| Service | Default Port | Purpose |
|---------|-------------|---------|
| Frontend | 3000 | React application |
| Backend | 8000 | FastAPI server |
| PostgreSQL | 5433 | User database |
| MongoDB | 27018 | Post database |
| Redis | 6380 | Cache |
| MinIO | 9000 | Object storage API |
| MinIO Console | 9001 | Web interface |
| ChromaDB | 8001 | Vector database |

### Changing Default Ports

If you have port conflicts, edit `.env`:

```bash
# Example: Change all ports
FRONTEND_PORT=3001
BACKEND_PORT=8001
POSTGRES_PORT=5434
MONGODB_PORT=27019
REDIS_PORT=6381
MINIO_PORT=9002
MINIO_CONSOLE_PORT=9003
CHROMA_PORT=8002
```

Then restart:
```bash
docker-compose down
docker-compose up -d --build
```

---

## 📊 Database Schema

### PostgreSQL - Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    bio TEXT,
    profile_image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(255),
    mfa_recovery_codes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### MongoDB - Posts Collection

```javascript
{
  "_id": ObjectId("..."),
  "post_id": "post_abc123",
  "user_id": "user_xyz789",
  "username": "johndoe",
  "text": "Original post text",
  "caption": "AI-generated caption",
  "image_url": "http://minio:9000/instaintelli/originals/post_abc123.jpg",
  "thumbnail_url": "http://minio:9000/instaintelli/thumbnails/post_abc123.jpg",
  "topics": ["travel", "nature", "sunset"],
  "created_at": ISODate("2025-12-29T10:00:00Z"),
  "updated_at": ISODate("2025-12-29T10:00:00Z"),
  "likes_count": 0,
  "comments_count": 0
}
```

### ChromaDB - Embeddings Collection

```python
{
    "ids": ["post_abc123"],
    "embeddings": [[0.123, -0.456, ...]],  # 1536 dimensions
    "metadatas": [{
        "post_id": "post_abc123",
        "user_id": "user_xyz789",
        "created_at": "2025-12-29T10:00:00Z"
    }],
    "documents": ["Combined text for embedding"]
}
```

### Redis - Cache Structure

```
# Key patterns
search:{query_hash}:{user_id}:{n_results} = JSON
chat:{query_hash}:{user_id} = JSON
user:{user_id} = JSON

# TTL: 3600 seconds (1 hour)
```

---

## 🔐 Security Features

### Authentication
- **JWT Tokens**: Secure token-based authentication
- **Password Hashing**: bcrypt with salt
- **MFA/TOTP**: Google Authenticator support
- **Recovery Codes**: 10 one-time recovery codes

### Data Protection
- **Input Validation**: Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM
- **CORS**: Configured allowed origins
- **File Upload Validation**: Type and size checks

### Best Practices
- Environment variables for secrets
- No hardcoded credentials
- Secure password requirements (min 6 chars)
- Session management
- HTTPS ready (for production)

---

## 📈 Performance & Scalability

### Caching Strategy
- Redis for search results (1 hour TTL)
- Reduces OpenAI API calls
- Faster response times

### Database Optimization
- Indexed fields (email, username, user_id)
- Connection pooling
- Lazy loading
- Pagination support

### Image Optimization
- Automatic thumbnail generation (300x300)
- Optimized JPEG quality (85%)
- Lazy image loading in frontend

### Scalability Features
- Microservices architecture
- Stateless backend (horizontal scaling)
- Distributed caching (Redis)
- Object storage (MinIO/S3)
- Background job processing

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Getting Started

1. **Fork the repository**
   ```bash
   # Click "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/insta.git
   cd insta
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

4. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests if applicable

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/AmazingFeature
   ```

7. **Open a Pull Request**
   - Go to original repository
   - Click "New Pull Request"
   - Describe your changes
   - Submit!

### Commit Message Convention

Use conventional commits:

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Format code
refactor: Refactor code
test: Add tests
chore: Update dependencies
```

---

## 👥 Team

**Project Lead & Architecture:**
- **Alisha Shahid** - Search & RAG System, Redis Caching, MFA Implementation, Frontend Design

**Core Contributors:**
- **Hassan** - Authentication & User Management
- **Sami** - Post Upload Service & MinIO Storage
- **Raza** - AI Processing & Vector Embeddings

**Course:** Big Data Analytics  
**Institution:** [Your University]  
**Year:** 2025

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 InstaIntelli Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 and embeddings API
- **FastAPI** framework and community
- **React** and Vite teams
- **ChromaDB** for vector search
- **Docker** for containerization
- All open-source contributors

---

## 📚 Additional Resources

- **Detailed Technical Manual**: See `PROJECT_MANUAL.md`
- **API Documentation**: http://localhost:8000/docs (when running)
- **GitHub Repository**: https://github.com/InstaIntelli/insta
- **OpenAI Documentation**: https://platform.openai.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **React Documentation**: https://react.dev

---

## 🎯 Project Highlights

InstaIntelli demonstrates:

✅ **Polyglot Persistence** with 5 databases  
✅ **Vector Search** with OpenAI embeddings  
✅ **RAG System** with LangChain  
✅ **Microservices Architecture** with Docker  
✅ **Modern Frontend** with React 18  
✅ **AI Integration** with GPT-4  
✅ **Production-Ready** security and scalability  
✅ **Comprehensive Documentation**  

---

<div align="center">

**Built with ❤️ for Big Data Analytics Course**

⭐ **Star this repository if you found it helpful!** ⭐

[Report Bug](https://github.com/InstaIntelli/insta/issues) · [Request Feature](https://github.com/InstaIntelli/insta/issues)

</div>
