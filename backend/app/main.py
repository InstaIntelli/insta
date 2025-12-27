"""
InstaIntelli - FastAPI Main Application
Main entry point for the backend API
To be implemented by team
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Placeholder - configuration to be loaded from app.core.config
# from app.core.config import settings

app = FastAPI(
    title="InstaIntelli API",
    description="AI-powered social media analytics platform",
    version="0.1.0"
)

# CORS middleware - to be configured
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# API routers - to be added by respective team members
# from app.api.v1.endpoints import auth, users, posts, ai, search
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])
# app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
# app.include_router(search.router, prefix="/api/v1/search", tags=["search"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "InstaIntelli API is running", "status": "ok"}

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "InstaIntelli API"
    }

