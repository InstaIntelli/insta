# InstaIntelli - Comprehensive Project Documentation

> **AI-Powered Social Media Analytics Platform**  
> A full-stack application with advanced AI features, multi-database architecture, and modern React UI

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Project Structure](#4-project-structure)
5. [Features](#5-features)
6. [Database Schema](#6-database-schema)
7. [API Documentation](#7-api-documentation)
8. [Frontend Components](#8-frontend-components)
9. [AI/ML Modules](#9-aiml-modules)
10. [Setup & Installation](#10-setup--installation)
11. [Environment Configuration](#11-environment-configuration)
12. [Deployment Guide](#12-deployment-guide)
13. [Security Features](#13-security-features)
14. [Testing](#14-testing)
15. [Contributing](#15-contributing)

---

## 1. Project Overview

**InstaIntelli** is an AI-powered social media platform that combines the core functionality of Instagram with intelligent features like:

- **Semantic Search**: Find posts using natural language queries
- **RAG-based Chat**: Ask questions about your content using AI
- **Smart Recommendations**: AI-driven user and content recommendations
- **Advanced Analytics**: Real-time engagement tracking and insights
- **Multi-Factor Authentication**: Enhanced security with TOTP

### Key Differentiators

| Feature | Description |
|---------|-------------|
| **Vector Search** | Semantic search using FAISS/ChromaDB embeddings |
| **RAG Chatbot** | Chat with AI about your posts using LangChain |
| **Graph Social Network** | Neo4j-powered follower/following relationships |
| **Real-time Analytics** | Redis-cached engagement metrics |
| **Multi-DB Architecture** | PostgreSQL, MongoDB, Redis, Neo4j, Cassandra |

---

## 2. Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  Feed   │ │ Profile │ │ Search  │ │  Chat   │ │Analytics│   │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │
│       └───────────┴───────────┴───────────┴───────────┘         │
│                              │                                   │
│                       Axios API Client                           │
└──────────────────────────────┼───────────────────────────────────┘
                               │ HTTP/REST
┌──────────────────────────────┼───────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    API Layer (v1)                        │    │
│  │  auth │ posts │ search │ social │ ai │ analytics │ mfa  │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                              │                                   │
│  ┌──────────────────────────┴──────────────────────────────┐    │
│  │                   Service Layer                          │    │
│  │  AuthService │ PostService │ AIService │ SocialService   │    │
│  └──────────────────────────┬──────────────────────────────┘    │
│                              │                                   │
│  ┌──────────────────────────┴──────────────────────────────┐    │
│  │                   Database Layer                         │    │
│  │  PostgreSQL │ MongoDB │ Redis │ Neo4j │ Cassandra        │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────┼───────────────────────────────────┐
│                       AI/ML LAYER                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐    │
│  │  Embeddings │ │ Vector DB   │ │   RAG (LangChain)       │    │
│  │  (OpenAI)   │ │ (FAISS)     │ │   Question Answering    │    │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Authentication** → Supabase Auth → JWT Token → Protected Routes
2. **Post Upload** → Image Processing → MongoDB Storage → Vector Embedding
3. **Search Query** → Embedding Generation → FAISS Similarity → Results
4. **Social Actions** → Neo4j Graph Updates → Real-time UI Updates

---

## 3. Technology Stack

### Backend

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Primary language | 3.11+ |
| **FastAPI** | Web framework | 0.100+ |
| **Pydantic** | Data validation | 2.0+ |
| **SQLAlchemy** | PostgreSQL ORM | 2.0+ |
| **PyMongo** | MongoDB driver | 4.0+ |
| **Neo4j** | Graph database driver | 5.0+ |
| **Redis** | Caching | 4.0+ |
| **LangChain** | RAG framework | 0.1+ |
| **FAISS** | Vector similarity search | 1.7+ |
| **OpenAI** | Embeddings & LLM | 1.0+ |

### Frontend

| Technology | Purpose | Version |
|------------|---------|---------|
| **React** | UI framework | 18+ |
| **Vite** | Build tool | 5+ |
| **React Router** | Routing | 6+ |
| **Axios** | HTTP client | 1.6+ |
| **CSS3** | Styling (Glassmorphism) | - |

### Databases

| Database | Use Case |
|----------|----------|
| **PostgreSQL** | User accounts, authentication |
| **MongoDB** | Posts, comments, messages |
| **Redis** | Caching, sessions, real-time data |
| **Neo4j** | Social graph (followers, following) |
| **Cassandra** | Activity logs, time-series data |
| **FAISS/ChromaDB** | Vector embeddings for search |

### DevOps

| Tool | Purpose |
|------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **MinIO** | Object storage (images) |

---

## 4. Project Structure

```
big_data_project/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/endpoints/   # API route handlers
│   │   │   ├── auth.py         # Authentication routes
│   │   │   ├── posts.py        # Post CRUD operations
│   │   │   ├── search.py       # Semantic search & RAG
│   │   │   ├── social.py       # Follow, like, comment
│   │   │   ├── ai.py           # AI processing endpoints
│   │   │   ├── analytics.py    # Dashboard analytics
│   │   │   ├── mfa.py          # Multi-factor auth
│   │   │   ├── profile.py      # User profiles
│   │   │   └── recommendations.py
│   │   ├── services/           # Business logic
│   │   │   ├── auth/           # Authentication service
│   │   │   ├── posts/          # Post management
│   │   │   ├── ai/             # AI/ML services
│   │   │   ├── search/         # Search functionality
│   │   │   ├── social/         # Social features
│   │   │   └── analytics/      # Analytics processing
│   │   ├── db/                 # Database connections
│   │   │   ├── postgres/       # PostgreSQL client
│   │   │   ├── mongodb/        # MongoDB client
│   │   │   ├── redis/          # Redis client
│   │   │   ├── neo4j/          # Neo4j client
│   │   │   └── cassandra/      # Cassandra client
│   │   ├── core/               # Configuration
│   │   │   └── config.py       # Settings management
│   │   └── main.py             # FastAPI entry point
│   ├── ai_service/             # Standalone AI module
│   └── post_service/           # Post processing module
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Layout.jsx      # Main layout wrapper
│   │   │   ├── PostCard.jsx    # Post display component
│   │   │   ├── CommentSection.jsx
│   │   │   ├── RightSidebar.jsx
│   │   │   ├── Stories.jsx
│   │   │   └── MessagesPill.jsx
│   │   ├── pages/              # Route pages
│   │   │   ├── FeedPage.jsx    # Home feed
│   │   │   ├── ProfilePage.jsx # User profile
│   │   │   ├── SearchPage.jsx  # Semantic search
│   │   │   ├── AssistantPage.jsx # AI chat
│   │   │   ├── MessagesPage.jsx  # Direct messages
│   │   │   ├── AnalyticsDashboard.jsx
│   │   │   └── RecommendationsPage.jsx
│   │   ├── services/           # API clients
│   │   │   ├── api.js          # Axios instance
│   │   │   ├── authService.js
│   │   │   ├── postService.js
│   │   │   ├── socialService.js
│   │   │   └── searchService.js
│   │   ├── contexts/           # React contexts
│   │   │   └── ThemeContext.jsx
│   │   └── utils/              # Utility functions
│   │       └── auth.js
│   └── vite.config.js
│
├── ai/                         # AI/ML Modules
│   ├── embeddings/             # Embedding generation
│   ├── rag/                    # RAG implementation
│   └── vector_db/              # Vector store management
│
├── scripts/                    # Utility scripts
├── docs/                       # Documentation
├── docker-compose.yml          # Container orchestration
├── .env.example                # Environment template
└── README.md                   # Quick start guide
```

---

## 5. Features

### 5.1 Authentication & Security

| Feature | Description |
|---------|-------------|
| **Email/Password Auth** | Traditional registration with Supabase |
| **Google OAuth** | Social login integration |
| **Multi-Factor Auth** | TOTP-based 2FA with QR codes |
| **JWT Tokens** | Secure API authentication |
| **Protected Routes** | Frontend route guards |

### 5.2 Social Features

| Feature | Description |
|---------|-------------|
| **Follow/Unfollow** | Neo4j-powered social graph |
| **Like Posts** | Double-tap to like with animation |
| **Comments** | Nested threaded comments |
| **Direct Messages** | User-to-user messaging |
| **Follower/Following Lists** | Modal views with actions |

### 5.3 Content Management

| Feature | Description |
|---------|-------------|
| **Post Upload** | Image upload with captions |
| **Feed** | Personalized content feed |
| **My Posts** | User's own post gallery |
| **Stories** | Story-style content display |

### 5.4 AI-Powered Features

| Feature | Description |
|---------|-------------|
| **Semantic Search** | Natural language post search |
| **RAG Chat** | Ask questions about your content |
| **Smart Recommendations** | AI-driven user suggestions |
| **Content Analysis** | Automatic tag generation |

### 5.5 Analytics

| Feature | Description |
|---------|-------------|
| **Engagement Metrics** | Likes, comments, shares |
| **Growth Tracking** | Follower trends over time |
| **Post Performance** | Individual post analytics |
| **Dashboard** | Visual data representation |

---

## 6. Database Schema

### 6.1 PostgreSQL (Users & Auth)

```sql
-- Users Table
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    full_name VARCHAR(100),
    bio TEXT,
    profile_picture VARCHAR(500),
    is_verified BOOLEAN DEFAULT FALSE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6.2 MongoDB (Posts & Content)

```javascript
// Posts Collection
{
    _id: ObjectId,
    post_id: UUID,
    user_id: UUID,
    caption: String,
    image_url: String,
    tags: [String],
    likes_count: Number,
    comments_count: Number,
    created_at: Date,
    updated_at: Date,
    embedding: [Number]  // Vector for semantic search
}

// Comments Collection
{
    _id: ObjectId,
    comment_id: UUID,
    post_id: UUID,
    user_id: UUID,
    parent_comment_id: UUID,  // For nested replies
    text: String,
    created_at: Date
}

// Messages Collection
{
    _id: ObjectId,
    message_id: UUID,
    sender_id: UUID,
    recipient_id: UUID,
    content: String,
    read: Boolean,
    created_at: Date
}
```

### 6.3 Neo4j (Social Graph)

```cypher
// Nodes
(:User {user_id: UUID, username: String})
(:Post {post_id: UUID})

// Relationships
(:User)-[:FOLLOWS]->(:User)
(:User)-[:LIKES]->(:Post)
(:User)-[:CREATED]->(:Post)
```

### 6.4 Redis (Caching)

```
# Session tokens
session:{user_id} -> {token_data}

# Analytics cache
analytics:{user_id}:daily -> {metrics}

# Rate limiting
ratelimit:{ip}:{endpoint} -> {count}
```

---

## 7. API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login user |
| POST | `/auth/refresh` | Refresh token |
| POST | `/auth/google` | Google OAuth |
| GET | `/auth/me` | Get current user |

### MFA Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mfa/setup` | Initialize MFA setup |
| POST | `/mfa/verify` | Verify OTP code |
| POST | `/mfa/disable` | Disable MFA |

### Post Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts` | Get feed posts |
| POST | `/posts` | Create new post |
| GET | `/posts/{post_id}` | Get single post |
| DELETE | `/posts/{post_id}` | Delete post |
| GET | `/posts/user/{user_id}` | Get user's posts |

### Social Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/social/follow/{user_id}` | Follow user |
| DELETE | `/social/unfollow/{user_id}` | Unfollow user |
| POST | `/social/like/{post_id}` | Like post |
| DELETE | `/social/unlike/{post_id}` | Unlike post |
| POST | `/social/comment` | Add comment |
| GET | `/social/comments/{post_id}` | Get comments |
| GET | `/social/followers/{user_id}` | Get followers |
| GET | `/social/following/{user_id}` | Get following |

### Search & AI Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search/semantic` | Semantic search |
| POST | `/search/chat` | RAG chat query |
| GET | `/search/suggestions` | Search suggestions |

### Analytics Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/dashboard` | Get dashboard data |
| GET | `/analytics/posts` | Post analytics |
| GET | `/analytics/engagement` | Engagement metrics |

### Recommendations Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommendations/users` | Suggested users |
| GET | `/recommendations/posts` | Recommended posts |

---

## 8. Frontend Components

### 8.1 Core Components

| Component | File | Purpose |
|-----------|------|---------|
| **Layout** | `Layout.jsx` | Main app layout with sidebar |
| **PostCard** | `PostCard.jsx` | Individual post display |
| **CommentSection** | `CommentSection.jsx` | Threaded comments |
| **RightSidebar** | `RightSidebar.jsx` | Suggestions panel |
| **Stories** | `Stories.jsx` | Stories carousel |
| **MessagesPill** | `MessagesPill.jsx` | Floating messages button |

### 8.2 Pages

| Page | Route | Purpose |
|------|-------|---------|
| **FeedPage** | `/feed` | Home feed |
| **ProfilePage** | `/profile/:userId` | User profile |
| **SearchPage** | `/search` | Semantic search |
| **AssistantPage** | `/chat` | AI chat interface |
| **MessagesPage** | `/messages` | Direct messages |
| **AnalyticsDashboard** | `/analytics` | Analytics |
| **RecommendationsPage** | `/recommendations` | Discover users |
| **UploadPage** | `/upload` | Create post |
| **MyPostsPage** | `/my-posts` | User's posts |

### 8.3 Design System

- **Theme**: Dark/Light mode support
- **Style**: Glassmorphism with vibrant gradients
- **Animations**: Smooth entrance and micro-interactions
- **Responsive**: Mobile-first design

---

## 9. AI/ML Modules

### 9.1 Embedding Generation

```python
# Using OpenAI embeddings
from openai import OpenAI

def generate_embedding(text: str) -> List[float]:
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding
```

### 9.2 Vector Store (FAISS)

```python
import faiss
import numpy as np

# Create index
dimension = 1536  # OpenAI embedding dimension
index = faiss.IndexFlatL2(dimension)

# Add vectors
vectors = np.array(embeddings).astype('float32')
index.add(vectors)

# Search
k = 10  # Top 10 results
distances, indices = index.search(query_vector, k)
```

### 9.3 RAG Implementation

```python
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS

# Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Query
response = qa_chain.run("What posts do I have about travel?")
```

---

## 10. Setup & Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- MongoDB 6+
- Redis 7+

### Quick Start

```bash
# 1. Clone repository
git clone <repository-url>
cd big_data_project

# 2. Setup environment
cp .env.example .env
# Edit .env with your credentials

# 3. Start with Docker
docker-compose up -d

# 4. Run backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# 5. Run frontend
cd frontend
npm install
npm run dev
```

### Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MinIO Console | http://localhost:9001 |

---

## 11. Environment Configuration

### Required Variables

```bash
# Database
POSTGRES_URL=postgresql://user:pass@localhost:5432/insta
MONGODB_URL=mongodb://localhost:27017/insta
REDIS_URL=redis://localhost:6379
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Authentication
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
JWT_SECRET=your-secret-key

# AI/ML
OPENAI_API_KEY=sk-your-openai-key

# Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Frontend
VITE_API_URL=http://localhost:8000
```

---

## 12. Deployment Guide

### Docker Deployment

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use production database credentials
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure proper CORS origins
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure log aggregation
- [ ] Set up backup strategies
- [ ] Enable rate limiting

---

## 13. Security Features

| Feature | Implementation |
|---------|----------------|
| **Password Hashing** | Argon2 via Supabase |
| **JWT Authentication** | Short-lived access tokens |
| **MFA** | TOTP with pyotp |
| **CORS** | Configured allowed origins |
| **Input Validation** | Pydantic models |
| **SQL Injection Prevention** | SQLAlchemy ORM |
| **XSS Prevention** | React's built-in escaping |
| **Rate Limiting** | Redis-based throttling |

---

## 14. Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### API Testing

Access Swagger UI at `http://localhost:8000/docs` for interactive API testing.

---

## 15. Contributing

### Development Workflow

1. Create feature branch from `main`
2. Implement changes with tests
3. Submit pull request
4. Code review and merge

### Code Style

- **Python**: Follow PEP 8, use Black formatter
- **JavaScript**: ESLint with Prettier
- **Commits**: Conventional commit messages

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Authors

**InstaIntelli Team**  
Big Data Project - 2026

---

*Documentation generated on: January 16, 2026*
