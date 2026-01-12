"""
PostgreSQL Failover Manager
Supports Supabase (cloud) as primary, local PostgreSQL as fallback
"""

from typing import Optional, Dict, Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, DisconnectionError
import logging
import time
from threading import Lock

from app.core.config import settings

logger = logging.getLogger("postgres_failover")

class PostgreSQLFailover:
    """Manages PostgreSQL connections with Supabase (primary) and local (fallback)"""
    
    def __init__(self):
        self.primary_engine: Optional[Engine] = None
        self.fallback_engine: Optional[Engine] = None
        self.current_engine: Optional[Engine] = None
        self.session_factory = None
        self.lock = Lock()
        self.last_health_check = 0
        self.health_check_interval = 30  # seconds
        self.primary_healthy = True
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize both primary (Supabase) and fallback (local) engines"""
        try:
            # Primary: Supabase (cloud PostgreSQL)
            if settings.SUPABASE_DB_URL:
                self.primary_engine = create_engine(
                    settings.SUPABASE_DB_URL,
                    pool_pre_ping=True,
                    pool_size=10,
                    max_overflow=20,
                    pool_recycle=3600,
                    connect_args={
                        "connect_timeout": 5,
                        "sslmode": "require" if "supabase.co" in settings.SUPABASE_DB_URL else "prefer"
                    }
                )
                logger.info("✅ Supabase (primary) PostgreSQL engine initialized")
            else:
                logger.warning("⚠️ SUPABASE_DB_URL not configured, using local PostgreSQL only")
            
            # Fallback: Local PostgreSQL
            if settings.POSTGRES_URL:
                self.fallback_engine = create_engine(
                    settings.POSTGRES_URL,
                    pool_pre_ping=True,
                    pool_size=20,
                    max_overflow=40,
                    pool_recycle=3600
                )
                logger.info("✅ Local (fallback) PostgreSQL engine initialized")
            else:
                logger.warning("⚠️ POSTGRES_URL not configured")
            
            # Set current engine (prefer primary)
            self.current_engine = self.primary_engine or self.fallback_engine
            
            if self.current_engine:
                self.session_factory = sessionmaker(
                    bind=self.current_engine,
                    autocommit=False,
                    autoflush=False
                )
                logger.info("✅ PostgreSQL failover manager initialized")
            else:
                logger.error("❌ No PostgreSQL engines available!")
                
        except Exception as e:
            logger.error(f"❌ Error initializing PostgreSQL engines: {str(e)}")
            # Fallback to local if primary fails
            if not self.current_engine and self.fallback_engine:
                self.current_engine = self.fallback_engine
                self.session_factory = sessionmaker(
                    bind=self.current_engine,
                    autocommit=False,
                    autoflush=False
                )
    
    def _health_check(self, engine: Engine) -> bool:
        """Check if database connection is healthy"""
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as e:
            logger.debug(f"Health check failed: {str(e)}")
            return False
    
    def _check_and_switch(self):
        """Check primary health and switch to fallback if needed"""
        current_time = time.time()
        
        # Only check every N seconds
        if current_time - self.last_health_check < self.health_check_interval:
            return
        
        self.last_health_check = current_time
        
        # If using fallback, try to switch back to primary
        if self.current_engine == self.fallback_engine and self.primary_engine:
            if self._health_check(self.primary_engine):
                logger.info("🔄 Switching back to Supabase (primary)")
                self.current_engine = self.primary_engine
                self.primary_healthy = True
                self.session_factory = sessionmaker(
                    bind=self.current_engine,
                    autocommit=False,
                    autoflush=False
                )
                return
        
        # If using primary, check health
        if self.current_engine == self.primary_engine:
            if not self._health_check(self.primary_engine):
                logger.warning("⚠️ Supabase (primary) unhealthy, switching to local fallback")
                if self.fallback_engine:
                    self.current_engine = self.fallback_engine
                    self.primary_healthy = False
                    self.session_factory = sessionmaker(
                        bind=self.fallback_engine,
                        autocommit=False,
                        autoflush=False
                    )
    
    def get_session(self) -> Session:
        """Get database session with automatic failover"""
        with self.lock:
            self._check_and_switch()
            
            if not self.current_engine:
                raise RuntimeError("No PostgreSQL engine available")
            
            return self.session_factory()
    
    def get_engine(self) -> Engine:
        """Get current database engine"""
        with self.lock:
            self._check_and_switch()
            return self.current_engine
    
    def is_using_primary(self) -> bool:
        """Check if currently using primary (Supabase)"""
        return self.current_engine == self.primary_engine
    
    def get_status(self) -> Dict[str, Any]:
        """Get current failover status"""
        return {
            "using_primary": self.is_using_primary(),
            "primary_available": self.primary_engine is not None,
            "fallback_available": self.fallback_engine is not None,
            "primary_healthy": self.primary_healthy if self.primary_engine else None,
            "current_db": "Supabase" if self.is_using_primary() else "Local PostgreSQL"
        }

# Global instance
postgres_failover = PostgreSQLFailover()

def get_db():
    """Dependency for FastAPI to get database session"""
    db = postgres_failover.get_session()
    try:
        yield db
    finally:
        db.close()

def get_engine():
    """Get current database engine"""
    return postgres_failover.get_engine()

def get_db_status():
    """Get database failover status"""
    return postgres_failover.get_status()

