"""
FastAPI application entry point for Post Upload + Storage Service.
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
        description="Post Upload + Storage Service for InstaIntelli - Handles image uploads, storage, and metadata management"
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
        logger.info("Post Upload + Storage Service starting up...")
        logger.info(f"MongoDB Database: {settings.mongodb_db_name}")
        logger.info(f"MinIO Endpoint: {settings.minio_endpoint}")
        logger.info(f"MinIO Bucket: {settings.minio_bucket_name}")
        logger.info(f"Max Upload Size: {settings.max_upload_size_mb}MB")
        logger.info("Service ready to accept requests")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown."""
        logger.info("Post Upload + Storage Service shutting down...")
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
        port=8001,
        reload=True
    )

