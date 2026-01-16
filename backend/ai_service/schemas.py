"""
Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ProcessPostRequest(BaseModel):
    """Request schema for processing a post."""
    
    post_id: str = Field(..., description="Unique identifier for the post")
    user_id: str = Field(..., description="Unique identifier for the user")
    text: Optional[str] = Field(None, description="Optional text content of the post")
    image_url: Optional[str] = Field(None, description="Optional image URL of the post")
    
    class Config:
        json_schema_extra = {
            "example": {
                "post_id": "post_123",
                "user_id": "user_456",
                "text": "Beautiful sunset today!",
                "image_url": "https://example.com/image.jpg"
            }
        }


class ProcessPostResponse(BaseModel):
    """Response schema for processing a post."""
    
    status: str = Field(..., description="Processing status")
    post_id: str = Field(..., description="Unique identifier for the post")
    message: Optional[str] = Field(None, description="Optional status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "processing_started",
                "post_id": "post_123",
                "message": "Post processing initiated"
            }
        }


class PostMetadata(BaseModel):
    """Metadata schema for storing in vector database."""
    
    post_id: str
    user_id: str
    topics: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    caption: Optional[str] = None
    text: Optional[str] = None
    image_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for ChromaDB storage."""
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "topics": ",".join(self.topics) if self.topics else "",
            "created_at": self.created_at.isoformat(),
            "caption": self.caption or "",
            "text": self.text or "",
            "image_url": self.image_url or "",
        }


class MongoDBPost(BaseModel):
    """Schema for post data from MongoDB."""
    
    _id: Optional[str] = None
    post_id: str
    user_id: str
    text: Optional[str] = None
    image_url: Optional[str] = None
    caption: Optional[str] = None
    created_at: Optional[datetime] = None
    topics: Optional[List[str]] = None

