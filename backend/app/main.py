"""
InstaIntelli - FastAPI Main Application
Main entry point for the backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="InstaIntelli API",
    description="AI-powered social media analytics platform with vector search, RAG, and multi-database architecture",
    version="0.1.0"
)


# Startup event to initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        # Initialize failover managers
        from app.db.postgres.failover import postgres_failover
        from app.db.mongodb.failover import mongo_failover
        from app.db.redis.failover import redis_failover
        
        # Create tables using current engine (will use primary or fallback)
        from app.db.postgres import create_tables
        create_tables()
        
        # Initialize Neo4j
        from app.db.neo4j import init_neo4j
        init_neo4j()
        
        # Initialize Cassandra
        from app.db.cassandra import cassandra_client
        cassandra_connected = cassandra_client.connect()
        if cassandra_connected:
            logger.info("✅ Cassandra initialized")
        else:
            logger.warning("⚠️ Cassandra connection failed (will retry on first use)")
        
        # Log database status
        logger.info("📊 Database Status:")
        logger.info(f"  PostgreSQL: {postgres_failover.get_status()}")
        logger.info(f"  MongoDB: {mongo_failover.get_status()}")
        logger.info(f"  Redis: {redis_failover.get_status()}")
        logger.info(f"  Cassandra: {'✅ Connected' if cassandra_connected else '⚠️ Not connected'}")
        
        logger.info("✅ Application startup complete")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        # Don't fail startup if database initialization fails
        logger.warning("Continuing without database initialization")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list if settings.allowed_origins_list else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers - integrated from team members
from app.api.v1.endpoints import auth, users, posts, ai, search, mfa, social, recommendations, analytics, health, profile, activity

# Register routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(mfa.router, prefix="/api/v1", tags=["Multi-Factor Authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(posts.router, prefix="/api/v1", tags=["Posts"])
app.include_router(ai.router, prefix="/api/v1", tags=["AI Processing"])
app.include_router(search.router, prefix="/api/v1", tags=["Search & RAG"])
app.include_router(social.router, prefix="/api/v1", tags=["Social Features"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(profile.router, prefix="/api/v1", tags=["Profile"])
app.include_router(activity.router, prefix="/api/v1", tags=["Activity"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])


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

