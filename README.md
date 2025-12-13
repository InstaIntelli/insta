# InstaIntelli 🚀  
AI-Powered Intelligent Social Media Platform

## 📌 Overview
InstaIntelli is a smart social media web application inspired by Instagram, enhanced with Artificial Intelligence, Vector Databases, and Big Data Analytics concepts.

Users can upload posts (images + captions), search content using natural language, and get AI-powered insights using a Retrieval-Augmented Generation (RAG) pipeline.

This project demonstrates the use of multiple storage systems, scalable architecture, and modern AI integration.

---

## 🎯 Key Features
- User authentication and profiles
- Image and post uploads
- Object storage for media
- AI-generated captions
- Semantic search using vector embeddings
- RAG-based AI chat over posts
- Caching for high performance
- Modular and scalable backend

---

## 🧠 Technologies Used

### Backend
- FastAPI (Python)
- PostgreSQL (Relational DB)
- MongoDB (Document DB)
- Redis (Caching)
- MinIO / Local S3 (Object Storage)
- Vector DB (ChromaDB / FAISS)
- OpenAI API (LLM + Embeddings)

### Frontend
- React (Web UI)

### DevOps
- GitHub Organization
- Git branches per feature
- Environment-based configuration

---

## 📦 Storage Architecture

| Storage Type | Technology | Purpose |
|--------------|-----------|---------|
| Relational DB | PostgreSQL | Users, authentication |
| Document DB | MongoDB | Posts, metadata |
| Object Storage | MinIO / Local FS | Images |
| Cache | Redis | Feed & search caching |
| Vector DB | Chroma / FAISS | Semantic search |
| Columnar | Parquet | Analytics (optional) |

---

## 👥 Team & Responsibilities

| Member | Area |
|------|------|
| Hassan | Authentication & User Profiles |
| Sami | Post Upload & Storage |
| Raza | AI Embeddings & Caption Generator |
| Alisha | Search, Recommendations & Chat |

Each member works **vertically** (frontend + backend + DB + AI) on their feature.

---

## 🚀 How to Run (High Level)
1. Set up databases locally or using Docker
2. Create `.env` file from `.env.example`
3. Start backend server
4. Start frontend
5. Use the app

---

## 📌 Academic Focus
This project demonstrates:
- Polyglot persistence
- Vector databases
- RAG architecture
- Parallel processing
- Scalable system design
- Functional and non-functional requirements

---

## 📜 License
MIT License


