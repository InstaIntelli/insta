"""
Health Check and Database Status Endpoints
"""

from fastapi import APIRouter
from typing import Dict, Any
from app.db.postgres.failover import get_db_status as get_postgres_status
from app.db.mongodb.failover import get_mongo_status
from app.db.redis.failover import get_redis_status

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Overall application health check"""
    return {
        "status": "healthy",
        "service": "InstaIntelli API",
        "version": "0.1.0"
    }


@router.get("/health/databases")
async def database_health() -> Dict[str, Any]:
    """Get health status of all databases with failover info"""
    try:
        postgres_status = get_postgres_status()
        mongo_status = get_mongo_status()
        redis_status = get_redis_status()
        
        return {
            "postgres": postgres_status,
            "mongodb": mongo_status,
            "redis": redis_status,
            "overall_status": "healthy" if all([
                postgres_status.get("primary_available") or postgres_status.get("fallback_available"),
                mongo_status.get("primary_available") or mongo_status.get("fallback_available"),
                redis_status.get("primary_available") or redis_status.get("fallback_available")
            ]) else "degraded"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

