"""
MongoDB Failover Manager
Supports MongoDB Atlas (cloud) as primary, local MongoDB as fallback
"""

from typing import Optional, Dict, Any
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import logging
import time
from threading import Lock

from app.core.config import settings

logger = logging.getLogger("mongodb_failover")

class MongoFailover:
    """Manages MongoDB connections with Atlas (primary) and local (fallback)"""
    
    def __init__(self):
        self.primary_client: Optional[MongoClient] = None
        self.fallback_client: Optional[MongoClient] = None
        self.current_client: Optional[MongoClient] = None
        self.current_database: Optional[Database] = None
        self.lock = Lock()
        self.last_health_check = 0
        self.health_check_interval = 30
        self.primary_healthy = True
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize both primary (Atlas) and fallback (local) clients"""
        try:
            # Primary: MongoDB Atlas (cloud)
            if settings.MONGODB_ATLAS_URL:
                self.primary_client = MongoClient(
                    settings.MONGODB_ATLAS_URL,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000
                )
                logger.info("✅ MongoDB Atlas (primary) client initialized")
            else:
                logger.warning("⚠️ MONGODB_ATLAS_URL not configured, using local MongoDB only")
            
            # Fallback: Local MongoDB
            if settings.MONGODB_URL:
                self.fallback_client = MongoClient(
                    settings.MONGODB_URL,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000
                )
                logger.info("✅ Local (fallback) MongoDB client initialized")
            else:
                logger.warning("⚠️ MONGODB_URL not configured")
            
            # Set current client (prefer primary)
            self.current_client = self.primary_client or self.fallback_client
            
            if self.current_client:
                database_name = settings.MONGODB_ATLAS_DATABASE or settings.MONGODB_DATABASE
                self.current_database = self.current_client[database_name]
                logger.info("✅ MongoDB failover manager initialized")
            else:
                logger.error("❌ No MongoDB clients available!")
                
        except Exception as e:
            logger.error(f"❌ Error initializing MongoDB clients: {str(e)}")
            if not self.current_client and self.fallback_client:
                self.current_client = self.fallback_client
                database_name = settings.MONGODB_DATABASE
                self.current_database = self.current_client[database_name]
    
    def _health_check(self, client: MongoClient) -> bool:
        """Check if MongoDB connection is healthy"""
        try:
            client.admin.command('ping')
            return True
        except Exception as e:
            logger.debug(f"MongoDB health check failed: {str(e)}")
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
                logger.info("🔄 Switching back to MongoDB Atlas (primary)")
                self.current_client = self.primary_client
                self.primary_healthy = True
                database_name = settings.MONGODB_ATLAS_DATABASE or settings.MONGODB_DATABASE
                self.current_database = self.current_client[database_name]
                return
        
        # If using primary, check health
        if self.current_client == self.primary_client:
            if not self._health_check(self.primary_client):
                logger.warning("⚠️ MongoDB Atlas (primary) unhealthy, switching to local fallback")
                if self.fallback_client:
                    self.current_client = self.fallback_client
                    self.primary_healthy = False
                    database_name = settings.MONGODB_DATABASE
                    self.current_database = self.current_client[database_name]
    
    def get_database(self) -> Database:
        """Get database with automatic failover"""
        with self.lock:
            self._check_and_switch()
            
            if not self.current_database:
                raise RuntimeError("No MongoDB database available")
            
            return self.current_database
    
    def get_collection(self, collection_name: str) -> Collection:
        """Get collection with automatic failover"""
        database = self.get_database()
        return database[collection_name]
    
    def get_client(self) -> MongoClient:
        """Get current MongoDB client"""
        with self.lock:
            self._check_and_switch()
            return self.current_client
    
    def is_using_primary(self) -> bool:
        """Check if currently using primary (Atlas)"""
        return self.current_client == self.primary_client
    
    def get_status(self) -> Dict[str, Any]:
        """Get current failover status"""
        return {
            "using_primary": self.is_using_primary(),
            "primary_available": self.primary_client is not None,
            "fallback_available": self.fallback_client is not None,
            "primary_healthy": self.primary_healthy if self.primary_client else None,
            "current_db": "MongoDB Atlas" if self.is_using_primary() else "Local MongoDB"
        }

# Global instance
mongo_failover = MongoFailover()

def get_mongo_db() -> Database:
    """Get MongoDB database with failover"""
    return mongo_failover.get_database()

def get_mongo_collection(collection_name: str) -> Collection:
    """Get MongoDB collection with failover"""
    return mongo_failover.get_collection(collection_name)

def get_mongo_status():
    """Get MongoDB failover status"""
    return mongo_failover.get_status()

