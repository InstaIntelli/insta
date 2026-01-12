"""
PostgreSQL database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create Base class for models
Base = declarative_base()

# Database engine
engine = None
SessionLocal = None


def init_db():
    """Initialize database connection"""
    global engine, SessionLocal
    
    try:
        if not settings.POSTGRES_URL:
            logger.warning("PostgreSQL URL not configured. Auth features will be disabled.")
            return
        
        engine = create_engine(
            settings.POSTGRES_URL,
            pool_pre_ping=True,
            pool_size=20,  # Increased for better concurrency
            max_overflow=40,  # Increased for peak loads
            pool_recycle=3600,  # Recycle connections after 1 hour
            echo=False  # Disable SQL logging for performance
        )
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        logger.info("PostgreSQL database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize PostgreSQL: {str(e)}")
        raise


def create_tables():
    """Create all tables in the database"""
    try:
        if engine is None:
            logger.warning("Database engine not initialized")
            return
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI endpoints to get database session
    Uses failover manager if available, otherwise falls back to original
    
    Yields:
        Database session
    """
    try:
        # Try to use failover manager first
        from app.db.postgres.failover import get_db as get_db_failover
        yield from get_db_failover()
    except (ImportError, RuntimeError):
        # Fallback to original implementation
        if SessionLocal is None:
            raise RuntimeError("Database not initialized")
        
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


# Initialize database on import
try:
    init_db()
except Exception as e:
    logger.error(f"Database initialization failed: {str(e)}")
