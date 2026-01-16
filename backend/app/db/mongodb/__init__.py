"""
MongoDB connection with failover support
"""

from app.db.mongodb.failover import (
    get_mongo_db,
    get_mongo_collection,
    get_mongo_status,
    mongo_failover
)

__all__ = [
    "get_mongo_db",
    "get_mongo_collection", 
    "get_mongo_status",
    "mongo_failover"
]
