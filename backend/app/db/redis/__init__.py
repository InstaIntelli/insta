"""
Redis connection with failover support
"""

import json
from typing import Optional, Any
from app.db.redis.failover import (
    get_redis_client,
    get_redis_status,
    redis_failover
)

__all__ = [
    "get_redis_client",
    "get_redis_status",
    "redis_failover",
    "cache_get",
    "cache_set",
    "cache_key_search",
    "cache_key_chat",
    "cache_key_profile"
]


def cache_key_search(query: str, user_id: Optional[str] = None) -> str:
    """Generate cache key for search"""
    if user_id:
        return f"search:{hash(query)}:{user_id}"
    return f"search:{hash(query)}"


def cache_key_chat(query: str, user_id: Optional[str] = None) -> str:
    """Generate cache key for chat"""
    if user_id:
        return f"chat:{hash(query)}:{user_id}"
    return f"chat:{hash(query)}"


def cache_key_profile(user_id: str) -> str:
    """Generate cache key for user profile"""
    return f"profile:{user_id}"


def cache_get(key: str) -> Optional[Any]:
    """Get value from Redis cache"""
    try:
        client = get_redis_client()
        if not client:
            return None
        value = client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        # Log error but don't fail - cache is optional
        return None


def cache_set(key: str, value: Any, expire_seconds: int = 3600) -> bool:
    """Set value in Redis cache"""
    try:
        client = get_redis_client()
        if not client:
            return False
        client.setex(key, expire_seconds, json.dumps(value))
        return True
    except Exception as e:
        # Log error but don't fail - cache is optional
        return False
