"""
MongoDB client for storing post metadata.
"""

from typing import Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

from .config import settings
from .schemas import PostMetadata
from .utils import logger


class MongoDBClient:
    """Client for interacting with MongoDB."""
    
    def __init__(self):
        """Initialize MongoDB client."""
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        self.collection: Optional[Collection] = None
        self._connect()
        self._create_indexes()
    
    def _connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(settings.mongodb_uri)
            self.database = self.client[settings.mongodb_db_name]
            self.collection = self.database[settings.mongodb_posts_collection]
            logger.info(f"Connected to MongoDB: {settings.mongodb_db_name}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    def _create_indexes(self) -> None:
        """Create indexes on the posts collection."""
        try:
            if not self.collection:
                raise RuntimeError("MongoDB collection not initialized")
            
            # Create index on user_id
            self.collection.create_index("user_id")
            
            # Create index on created_at
            self.collection.create_index("created_at")
            
            # Create compound index for common queries
            self.collection.create_index([("user_id", 1), ("created_at", -1)])
            
            logger.info("MongoDB indexes created successfully")
        except PyMongoError as e:
            logger.error(f"Error creating indexes: {str(e)}")
            # Don't raise - indexes are optional for functionality
        except Exception as e:
            logger.error(f"Unexpected error creating indexes: {str(e)}")
    
    def create_post(self, metadata: PostMetadata) -> bool:
        """
        Create a new post in MongoDB.
        
        Args:
            metadata: PostMetadata object containing post information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.collection:
                raise RuntimeError("MongoDB collection not initialized")
            
            post_doc = metadata.to_dict()
            
            result = self.collection.insert_one(post_doc)
            
            if result.inserted_id:
                logger.info(f"Created post in MongoDB: {metadata.post_id}")
                return True
            else:
                logger.warning(f"Failed to create post: {metadata.post_id}")
                return False
                
        except PyMongoError as e:
            logger.error(f"Error creating post in MongoDB: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating post: {str(e)}")
            return False
    
    def get_post(self, post_id: str) -> Optional[dict]:
        """
        Retrieve a post from MongoDB.
        
        Args:
            post_id: Unique identifier for the post
            
        Returns:
            Post document if found, None otherwise
        """
        try:
            if not self.collection:
                raise RuntimeError("MongoDB collection not initialized")
            
            post = self.collection.find_one({"post_id": post_id})
            
            if post and "_id" in post:
                post["_id"] = str(post["_id"])
            
            return post
            
        except PyMongoError as e:
            logger.error(f"Error retrieving post from MongoDB: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving post: {str(e)}")
            return None
    
    def get_user_posts(self, user_id: str, limit: int = 50) -> list:
        """
        Retrieve posts for a specific user.
        
        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of posts to return
            
        Returns:
            List of post documents
        """
        try:
            if not self.collection:
                raise RuntimeError("MongoDB collection not initialized")
            
            posts = list(
                self.collection.find({"user_id": user_id})
                .sort("created_at", -1)
                .limit(limit)
            )
            
            # Convert ObjectId to string
            for post in posts:
                if "_id" in post:
                    post["_id"] = str(post["_id"])
            
            return posts
            
        except PyMongoError as e:
            logger.error(f"Error retrieving user posts from MongoDB: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error retrieving user posts: {str(e)}")
            return []
    
    def close(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global MongoDB client instance
mongodb_client = MongoDBClient()

