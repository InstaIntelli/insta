"""
Post upload and management endpoints
Integrated from Sami's Post Upload & Media Storage Service
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional, Tuple
from datetime import datetime
import sys
import os
import io
import uuid
import logging
from pathlib import Path

# Add post_service to path to import Sami's modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))

# Import main app config
from app.core.config import settings

# Import storage and MongoDB clients
from pymongo import MongoClient
from minio import Minio
from io import BytesIO
from PIL import Image

# Configure logging
logger = logging.getLogger("post_service")

router = APIRouter(prefix="/posts", tags=["Posts"])

# Configuration constants
MAX_UPLOAD_SIZE_MB = 10
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png"]
THUMBNAIL_SIZE = (300, 300)


# Helper functions (adapted from Sami's service)
def generate_post_id() -> str:
    """Generate a unique post ID."""
    return f"post_{uuid.uuid4().hex[:12]}"


def get_storage_path(post_id: str, filename: str, folder: str = "originals") -> str:
    """Generate storage path for a file."""
    extension = Path(filename).suffix.lower()
    return f"{folder}/{post_id}{extension}"


def validate_user_id(user_id: str) -> None:
    """Validate user ID."""
    if not user_id or not isinstance(user_id, str) or not user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id"
        )


def validate_image(file: UploadFile) -> Tuple[Image.Image, str]:
    """Validate and open image file."""
    try:
        # Read file content
        file_content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        # Validate file type
        if not file.content_type or file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )
        
        # Validate file size
        if file.size and file.size > MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum allowed size of {MAX_UPLOAD_SIZE_MB}MB"
            )
        
        # Try to open image with PIL
        try:
            image = Image.open(io.BytesIO(file_content))
            image.verify()
        except Exception as e:
            logger.error(f"Failed to open image: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or corrupted image file"
            )
        
        # Reopen image (verify() closes it)
        image = Image.open(io.BytesIO(file_content))
        
        # Get file extension
        extension = file.filename.split('.')[-1].lower() if file.filename else 'jpg'
        if extension not in ['jpg', 'jpeg', 'png']:
            extension = 'jpg'
        
        logger.info(f"Image validated: {image.size}, format: {image.format}")
        return image, extension
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to validate image: {str(e)}"
        )


def generate_thumbnail(image: Image.Image, size: Tuple[int, int] = None) -> Image.Image:
    """Generate a thumbnail from an image while maintaining aspect ratio."""
    if size is None:
        size = THUMBNAIL_SIZE
    
    try:
        image.thumbnail(size, Image.Resampling.LANCZOS)
        thumbnail = image.copy()
        logger.info(f"Thumbnail generated: {thumbnail.size}")
        return thumbnail
    except Exception as e:
        logger.error(f"Error generating thumbnail: {str(e)}")
        raise ValueError(f"Failed to generate thumbnail: {str(e)}")


def image_to_bytes(image: Image.Image, format: str = "JPEG") -> bytes:
    """Convert PIL Image to bytes."""
    try:
        buffer = io.BytesIO()
        
        # Convert RGBA to RGB for JPEG
        if format.upper() == "JPEG" and image.mode in ("RGBA", "LA", "P"):
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            image = rgb_image
        
        image.save(buffer, format=format, quality=85, optimize=True)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"Error converting image to bytes: {str(e)}")
        raise ValueError(f"Failed to convert image to bytes: {str(e)}")


def get_image_format(extension: str) -> str:
    """Get PIL format string from file extension."""
    extension = extension.lower().lstrip('.')
    format_map = {
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'png': 'PNG'
    }
    return format_map.get(extension, 'JPEG')


# Initialize MongoDB client using main app config
def get_mongodb_client():
    """Get MongoDB client using main app configuration."""
    client = MongoClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DATABASE]
    collection = database[settings.MONGODB_POSTS_COLLECTION]
    return collection


# Initialize MinIO client using main app config
def get_storage_client():
    """Get MinIO client using main app configuration."""
    # Parse endpoint (remove http:// if present)
    endpoint = settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
    
    client = Minio(
        endpoint,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False  # MinIO in Docker typically uses HTTP
    )
    
    # Ensure bucket exists
    if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
        client.make_bucket(settings.MINIO_BUCKET_NAME)
        logger.info(f"Created bucket: {settings.MINIO_BUCKET_NAME}")
    
    return client


def upload_file_to_minio(client: Minio, file_data: bytes, object_name: str, content_type: str) -> str:
    """Upload file to MinIO and return URL."""
    from datetime import timedelta
    
    # Upload file
    client.put_object(
        settings.MINIO_BUCKET_NAME,
        object_name,
        BytesIO(file_data),
        length=len(file_data),
        content_type=content_type
    )
    
    # Generate URL (using MinIO endpoint from settings)
    # In production, you'd use a proper CDN or public bucket
    base_url = f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{object_name}"
    return base_url


# Response models
class UploadPostResponse:
    """Response model for post upload."""
    def __init__(self, post_id: str, status: str, image_url: str, thumbnail_url: str, message: str = None):
        self.post_id = post_id
        self.status = status
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.message = message
    
    def dict(self):
        return {
            "post_id": self.post_id,
            "status": self.status,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "message": self.message
        }


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a post",
    description="Upload an image post with optional text. Returns post ID and URLs."
)
async def upload_post(
    file: UploadFile = File(..., description="Image file (JPG or PNG)"),
    user_id: str = Form(..., description="User identifier"),
    text: str = Form(None, description="Optional text content")
):
    """
    Upload a post with image and optional text.
    
    This endpoint:
    - Validates the uploaded image
    - Uploads original image to MinIO
    - Generates and uploads thumbnail
    - Stores post metadata in MongoDB
    
    Args:
        file: Image file (JPG or PNG)
        user_id: User identifier
        text: Optional text content
        
    Returns:
        UploadPostResponse with post_id, status, and URLs
        
    Raises:
        HTTPException: If validation fails or upload fails
    """
    try:
        # Validate user_id
        validate_user_id(user_id)
        
        # Validate and open image
        logger.info(f"Validating image for user: {user_id}")
        image, extension = validate_image(file)
        
        # Generate post ID
        post_id = generate_post_id()
        logger.info(f"Generated post_id: {post_id}")
        
        # Prepare file data
        image_format = get_image_format(extension)
        original_bytes = image_to_bytes(image, format=image_format)
        
        # Generate thumbnail
        logger.info("Generating thumbnail")
        thumbnail = generate_thumbnail(image.copy())
        thumbnail_bytes = image_to_bytes(thumbnail, format=image_format)
        
        # Get storage client
        storage_client = get_storage_client()
        
        # Upload original image
        original_path = get_storage_path(post_id, file.filename or f"image.{extension}", "originals")
        logger.info(f"Uploading original image: {original_path}")
        original_url = upload_file_to_minio(
            storage_client,
            original_bytes,
            original_path,
            file.content_type or "image/jpeg"
        )
        
        # Upload thumbnail
        thumbnail_path = get_storage_path(post_id, file.filename or f"image.{extension}", "thumbnails")
        logger.info(f"Uploading thumbnail: {thumbnail_path}")
        thumbnail_url = upload_file_to_minio(
            storage_client,
            thumbnail_bytes,
            thumbnail_path,
            file.content_type or "image/jpeg"
        )
        
        # Create post metadata
        metadata = {
            "post_id": post_id,
            "user_id": user_id,
            "text": text if text else None,
            "image_url": original_url,
            "thumbnail_url": thumbnail_url,
            "created_at": datetime.utcnow()
        }
        
        # Store in MongoDB
        logger.info(f"Storing post metadata in MongoDB: {post_id}")
        collection = get_mongodb_client()
        result = collection.insert_one(metadata)
        
        if not result.inserted_id:
            logger.error(f"Failed to store post metadata: {post_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store post metadata"
            )
        
        logger.info(f"Post uploaded successfully: {post_id}")
        
        response = UploadPostResponse(
            post_id=post_id,
            status="uploaded",
            image_url=original_url,
            thumbnail_url=thumbnail_url,
            message="Post uploaded successfully"
        )
        return response.dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload post: {str(e)}"
        )


@router.get(
    "/{post_id}",
    summary="Get post by ID",
    description="Retrieve a post by its ID"
)
async def get_post(post_id: str):
    """Get a post by ID."""
    try:
        collection = get_mongodb_client()
        post = collection.find_one({"post_id": post_id})
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post not found: {post_id}"
            )
        
        # Remove MongoDB _id field
        post.pop("_id", None)
        return post
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get post: {str(e)}"
        )


@router.get(
    "/user/{user_id}",
    summary="Get posts by user",
    description="Retrieve all posts for a specific user"
)
async def get_user_posts(
    user_id: str,
    limit: int = 20,
    skip: int = 0
):
    """Get posts by user ID."""
    try:
        collection = get_mongodb_client()
        posts = list(collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).skip(skip).limit(limit))
        
        # Remove MongoDB _id fields
        for post in posts:
            post.pop("_id", None)
        
        return {
            "user_id": user_id,
            "posts": posts,
            "count": len(posts)
        }
        
    except Exception as e:
        logger.error(f"Error getting user posts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user posts: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check endpoint",
    description="Check if the Post Upload + Storage Service is running"
)
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Post Upload + Storage Service"
    }
