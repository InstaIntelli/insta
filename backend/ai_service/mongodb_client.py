"""
MongoDB client for fetching post data.

Assumes MongoDB is already set up and stores posts.
"""

from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from .config import settings
from .schemas import MongoDBPost
from .utils import logger


class MongoDBClient:
    """Client for interacting with MongoDB."""
    
    def __init__(self):
        """Initialize MongoDB client."""
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        self.collection: Optional[Collection] = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(settings.mongodb_uri)
            self.database = self.client[settings.mongodb_database]
            self.collection = self.database[settings.mongodb_posts_collection]
            logger.info(f"Connected to MongoDB: {settings.mongodb_database}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    def get_post(self, post_id: str) -> Optional[MongoDBPost]:
        """
        Fetch post data from MongoDB.
        
        Args:
            post_id: Unique identifier for the post
            
        Returns:
            MongoDBPost if found, None otherwise
        """
        try:
            if not self.collection:
                raise RuntimeError("MongoDB collection not initialized")
            
            # Try to find by post_id field first, then by _id
            post_data = self.collection.find_one({"post_id": post_id})
            if not post_data:
                post_data = self.collection.find_one({"_id": post_id})
            
            if not post_data:
                logger.warning(f"Post not found in MongoDB: {post_id}")
                return None
            
            # Convert ObjectId to string if present
            if "_id" in post_data:
                post_data["_id"] = str(post_data["_id"])
            
            return MongoDBPost(**post_data)
        except Exception as e:
            logger.error(f"Error fetching post from MongoDB: {str(e)}")
            return None
    
    def update_post_caption(self, post_id: str, caption: str) -> bool:
        """
        Update post caption in MongoDB.
        
        Args:
            post_id: Unique identifier for the post
            caption: Generated caption to store
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            if not self.collection:
                raise RuntimeError("MongoDB collection not initialized")
            
            result = self.collection.update_one(
                {"post_id": post_id},
                {"$set": {"caption": caption}},
                upsert=False
            )
            
            if result.modified_count > 0:
                logger.info(f"Updated caption for post: {post_id}")
                return True
            else:
                logger.warning(f"Post not found for caption update: {post_id}")
                return False
        except Exception as e:
            logger.error(f"Error updating post caption: {str(e)}")
            return False
    
    def close(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global MongoDB client instance
mongodb_client = MongoDBClient()

