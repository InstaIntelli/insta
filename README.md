# InstaIntelli 🚀

AI-powered intelligent social media platform with vector search, RAG (Retrieval Augmented Generation), multi-database architecture, and scalable microservices design.

## 🌟 Features

### Core Features
- **User Authentication** - Secure JWT-based authentication with PostgreSQL
- **Post Upload & Management** - Image uploads with automatic thumbnail generation
- **AI-Powered Captions** - Automatic caption generation using LLM
- **Semantic Search** - Vector-based search for finding similar posts
- **RAG Chat** - Chat with your posts using retrieval augmented generation
- **Real-time Feed** - Browse posts from all users
- **User Profiles** - Manage user profiles and view user posts

### Technical Features
- **Polyglot Persistence** - Multiple specialized databases
- **Vector Embeddings** - Semantic search with ChromaDB
- **Caching Layer** - Redis for performance optimization
- **Object Storage** - MinIO for scalable image storage
- **Microservices Architecture** - Modular and scalable design
- **Docker Containerization** - Easy deployment and development

## 🏗️ Architecture

### Technology Stack

**Frontend:**
- React 18 with Vite
- React Router for navigation
- Axios for API calls
- Modern UI with dark/light theme

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- Pydantic for validation
- JWT authentication

**Databases:**
- **PostgreSQL** - User authentication and profiles
- **MongoDB** - Post metadata storage
- **Redis** - Caching layer
- **ChromaDB** - Vector database for embeddings
- **MinIO** - S3-compatible object storage

**AI/ML:**
- OpenAI GPT-4 for caption generation
- OpenAI Embeddings for semantic search
- LangChain for RAG implementation

### Project Structure

```
instaintelli/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # API endpoints
│   │   │   ├── auth/             # Authentication
│   │   │   ├── users/            # User profiles
│   │   │   ├── posts/            # Post management
│   │   │   ├── ai/               # AI processing
│   │   │   └── search/           # Search & RAG
│   │   ├── core/                 # Core configuration
│   │   ├── db/                   # Database connections
│   │   ├── models/               # Database models
│   │   └── services/             # Business logic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable components
│   │   ├── pages/                # Page components
│   │   ├── services/             # API services
│   │   └── contexts/             # React contexts
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml            # Docker orchestration
├── .env.example                  # Environment template
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API key (for AI features)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd big_data_project
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Minimum required: OPENAI_API_KEY, SECRET_KEY
```

### 3. Start Services

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001

## 📖 API Documentation

### Authentication Endpoints

```
POST /api/v1/auth/register  - Register new user
POST /api/v1/auth/login     - Login user
POST /api/v1/auth/logout    - Logout user
GET  /api/v1/auth/me        - Get current user
```

### Post Endpoints

```
POST /api/v1/posts/upload         - Upload post with image
GET  /api/v1/posts/{post_id}      - Get post by ID
GET  /api/v1/posts/user/{user_id} - Get user's posts
GET  /api/v1/posts/feed           - Get feed
DELETE /api/v1/posts/{post_id}    - Delete post
```

### AI Endpoints

```
POST /api/v1/ai/process_post  - Process post with AI
```

### Search Endpoints

```
POST /api/v1/search/semantic           - Semantic search
POST /api/v1/search/chat               - RAG chat
GET  /api/v1/search/similar/{post_id}  - Find similar posts
```

### User Endpoints

```
GET  /api/v1/users/{user_id}           - Get user profile
GET  /api/v1/users/username/{username} - Get user by username
PUT  /api/v1/users/{user_id}           - Update user profile
```

## 🔧 Development

### Running Locally (Without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Database Migrations

```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Run migrations
docker-compose exec backend alembic upgrade head
```

## 🧪 Testing

```bash
# Run backend tests
docker-compose exec backend pytest

# Run frontend tests
cd frontend && npm test
```

## 📊 Database Schema

### PostgreSQL (Users)
- `users` - User accounts and profiles

### MongoDB (Posts)
- `posts` - Post metadata, captions, image URLs

### ChromaDB (Vectors)
- `post_embeddings` - Vector embeddings for semantic search

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM

## 📈 Performance Optimization

- Redis caching for search results
- Database indexing
- Connection pooling
- Lazy loading
- Image optimization with thumbnails

## 🐛 Troubleshooting

### Services won't start
```bash
# Check service logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>
```

### Port conflicts
Edit `.env` file and change port numbers:
- `POSTGRES_PORT=5433`
- `MONGODB_PORT=27018`
- `REDIS_PORT=6380`

### Database connection errors
```bash
# Verify services are healthy
docker-compose ps

# Restart databases
docker-compose restart postgres mongodb redis
```

## 📝 Environment Variables

See `.env.example` for all configuration options.

**Required:**
- `OPENAI_API_KEY` - OpenAI API key for AI features
- `SECRET_KEY` - Secret key for JWT tokens

**Optional:**
- Database credentials (defaults provided)
- Service ports (defaults provided)
- LLM provider configuration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

- **Alisha** - Search & RAG, Caching
- **Hassan** - Authentication & Users
- **Sami** - Post Upload & Storage
- **Raza** - AI Processing & Embeddings

## 🙏 Acknowledgments

- OpenAI for GPT and embeddings
- FastAPI framework
- React community
- ChromaDB for vector search

---

**Built with ❤️ for Big Data Analytics Course**
