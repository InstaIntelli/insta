"""
Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UploadPostRequest(BaseModel):
    """Request schema for uploading a post."""
    
    user_id: str = Field(..., description="Unique identifier for the user")
    text: Optional[str] = Field(None, description="Optional text content of the post")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "text": "Beautiful sunset today!"
            }
        }


class UploadPostResponse(BaseModel):
    """Response schema for uploading a post."""
    
    post_id: str = Field(..., description="Unique identifier for the post")
    status: str = Field(..., description="Upload status")
    image_url: str = Field(..., description="URL of the original image")
    thumbnail_url: str = Field(..., description="URL of the thumbnail image")
    message: Optional[str] = Field(None, description="Optional status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "post_id": "post_123",
                "status": "uploaded",
                "image_url": "https://storage.example.com/originals/post_123.jpg",
                "thumbnail_url": "https://storage.example.com/thumbnails/post_123.jpg",
                "message": "Post uploaded successfully"
            }
        }


class PostMetadata(BaseModel):
    """Schema for post metadata stored in MongoDB."""
    
    post_id: str
    user_id: str
    text: Optional[str] = None
    image_url: str
    thumbnail_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> dict:
        """Convert metadata to dictionary for MongoDB storage."""
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "text": self.text,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "created_at": self.created_at
        }

