"""
InstaIntelli - FastAPI Main Application
Main entry point for the backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title="InstaIntelli API",
    description="AI-powered social media analytics platform with vector search, RAG, and multi-database architecture",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list if settings.allowed_origins_list else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers - integrated from team members
from app.api.v1.endpoints import auth, users, posts, ai, search

# Register routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(posts.router, prefix="/api/v1", tags=["Posts"])
app.include_router(ai.router, prefix="/api/v1", tags=["AI Processing"])
app.include_router(search.router, prefix="/api/v1", tags=["Search & RAG"])


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "InstaIntelli API is running",
        "status": "ok",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "InstaIntelli API",
        "version": "0.1.0"
    }

