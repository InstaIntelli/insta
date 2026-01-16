"""
FastAPI application entry point for AI Processing Service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api import router
from .utils import logger


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="AI Processing Service for InstaIntelli - Handles caption generation, embedding creation, and vector storage"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(router)
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup."""
        logger.info("AI Processing Service starting up...")
        logger.info(f"OpenAI Model: {settings.openai_model}")
        logger.info(f"Embedding Model: {settings.openai_embedding_model}")
        logger.info(f"ChromaDB Path: {settings.chroma_persist_path}")
        logger.info("Service ready to accept requests")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown."""
        logger.info("AI Processing Service shutting down...")
        from .mongodb_client import mongodb_client
        mongodb_client.close()
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )

