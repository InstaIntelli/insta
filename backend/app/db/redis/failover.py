"""
Redis Failover Manager
Supports Upstash (cloud) as primary, local Redis as fallback
"""

from typing import Optional, Dict, Any
import redis
from redis.exceptions import ConnectionError, TimeoutError
import logging
import time
from threading import Lock

from app.core.config import settings

logger = logging.getLogger("redis_failover")

class RedisFailover:
    """Manages Redis connections with Upstash (primary) and local (fallback)"""
    
    def __init__(self):
        self.primary_client: Optional[redis.Redis] = None
        self.fallback_client: Optional[redis.Redis] = None
        self.current_client: Optional[redis.Redis] = None
        self.lock = Lock()
        self.last_health_check = 0
        self.health_check_interval = 30
        self.primary_healthy = True
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize both primary (Upstash) and fallback (local) clients"""
        try:
            # Primary: Upstash (cloud Redis)
            if settings.UPSTASH_REDIS_URL:
                # Parse Upstash URL: redis://default:password@host:port
                self.primary_client = redis.from_url(
                    settings.UPSTASH_REDIS_URL,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    decode_responses=True
                )
                logger.info("✅ Upstash (primary) Redis client initialized")
            else:
                logger.warning("⚠️ UPSTASH_REDIS_URL not configured, using local Redis only")
            
            # Fallback: Local Redis
            if settings.REDIS_URL:
                self.fallback_client = redis.from_url(
                    settings.REDIS_URL,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    decode_responses=True
                )
                logger.info("✅ Local (fallback) Redis client initialized")
            elif settings.REDIS_HOST:
                self.fallback_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                    db=settings.REDIS_DB,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    decode_responses=True
                )
                logger.info("✅ Local (fallback) Redis client initialized")
            else:
                logger.warning("⚠️ Redis not configured")
            
            # Set current client (prefer primary)
            self.current_client = self.primary_client or self.fallback_client
            
            if self.current_client:
                logger.info("✅ Redis failover manager initialized")
            else:
                logger.error("❌ No Redis clients available!")
                
        except Exception as e:
            logger.error(f"❌ Error initializing Redis clients: {str(e)}")
            if not self.current_client and self.fallback_client:
                self.current_client = self.fallback_client
    
    def _health_check(self, client: redis.Redis) -> bool:
        """Check if Redis connection is healthy"""
        try:
            client.ping()
            return True
        except Exception as e:
            logger.debug(f"Redis health check failed: {str(e)}")
            return False
    
    def _check_and_switch(self):
        """Check primary health and switch to fallback if needed"""
        current_time = time.time()
        
        if current_time - self.last_health_check < self.health_check_interval:
            return
        
        self.last_health_check = current_time
        
        # If using fallback, try to switch back to primary
        if self.current_client == self.fallback_client and self.primary_client:
            if self._health_check(self.primary_client):
                logger.info("🔄 Switching back to Upstash (primary)")
                self.current_client = self.primary_client
                self.primary_healthy = True
                return
        
        # If using primary, check health
        if self.current_client == self.primary_client:
            if not self._health_check(self.primary_client):
                logger.warning("⚠️ Upstash (primary) unhealthy, switching to local fallback")
                if self.fallback_client:
                    self.current_client = self.fallback_client
                    self.primary_healthy = False
    
    def get_client(self) -> redis.Redis:
        """Get Redis client with automatic failover"""
        with self.lock:
            self._check_and_switch()
            
            if not self.current_client:
                raise RuntimeError("No Redis client available")
            
            return self.current_client
    
    def is_using_primary(self) -> bool:
        """Check if currently using primary (Upstash)"""
        return self.current_client == self.primary_client
    
    def get_status(self) -> Dict[str, Any]:
        """Get current failover status"""
        return {
            "using_primary": self.is_using_primary(),
            "primary_available": self.primary_client is not None,
            "fallback_available": self.fallback_client is not None,
            "primary_healthy": self.primary_healthy if self.primary_client else None,
            "current_db": "Upstash" if self.is_using_primary() else "Local Redis"
        }

# Global instance
redis_failover = RedisFailover()

def get_redis_client() -> redis.Redis:
    """Get Redis client with failover"""
    return redis_failover.get_client()

def get_redis_status():
    """Get Redis failover status"""
    return redis_failover.get_status()

