"""
Redis connection and caching utilities
Implemented by Alisha (Semantic Search & RAG)
"""

import redis
from typing import Optional, Any
import json
from datetime import timedelta
from app.core.config import settings
import logging

logger = logging.getLogger("redis_client")

# Redis client instance
redis_client: Optional[redis.Redis] = None


def get_redis_client() -> redis.Redis:
    """
    Get or create Redis client instance.
    
    Returns:
        Redis client instance
    """
    global redis_client
    
    if redis_client is None:
        try:
            # Parse Redis URL or use individual settings
            if settings.REDIS_URL:
                redis_client = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True
                )
            else:
                redis_client = redis.Redis(
                    host=settings.REDIS_HOST if hasattr(settings, 'REDIS_HOST') else 'localhost',
                    port=settings.REDIS_PORT if hasattr(settings, 'REDIS_PORT') else 6379,
                    db=settings.REDIS_DB if hasattr(settings, 'REDIS_DB') else 0,
                    password=settings.REDIS_PASSWORD if hasattr(settings, 'REDIS_PASSWORD') and settings.REDIS_PASSWORD else None,
                    decode_responses=True
                )
            
            # Test connection
            redis_client.ping()
            logger.info("Connected to Redis successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    
    return redis_client


def cache_get(key: str) -> Optional[Any]:
    """
    Get value from Redis cache.
    
    Args:
        key: Cache key
        
    Returns:
        Cached value or None if not found
    """
    try:
        client = get_redis_client()
        value = client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        logger.error(f"Error getting from cache: {str(e)}")
        return None


def cache_set(key: str, value: Any, expire_seconds: int = 3600) -> bool:
    """
    Set value in Redis cache.
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        expire_seconds: Expiration time in seconds (default: 1 hour)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_redis_client()
        serialized = json.dumps(value)
        client.setex(key, expire_seconds, serialized)
        return True
    except Exception as e:
        logger.error(f"Error setting cache: {str(e)}")
        return False


def cache_delete(key: str) -> bool:
    """
    Delete key from Redis cache.
    
    Args:
        key: Cache key to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_redis_client()
        client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Error deleting from cache: {str(e)}")
        return False


def cache_key_search(query: str, user_id: Optional[str] = None) -> str:
    """
    Generate cache key for search query.
    
    Args:
        query: Search query
        user_id: Optional user ID
        
    Returns:
        Cache key string
    """
    if user_id:
        return f"search:{user_id}:{query.lower().strip()}"
    return f"search:{query.lower().strip()}"


def cache_key_chat(user_id: str, conversation_id: Optional[str] = None) -> str:
    """
    Generate cache key for chat conversation.
    
    Args:
        user_id: User ID
        conversation_id: Optional conversation ID
        
    Returns:
        Cache key string
    """
    if conversation_id:
        return f"chat:{user_id}:{conversation_id}"
    return f"chat:{user_id}:default"
