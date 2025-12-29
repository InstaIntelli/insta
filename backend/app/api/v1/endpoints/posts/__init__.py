"""
Post upload and management endpoints
Integrated from Sami's Post Service
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import List

from app.services.posts.schemas import UploadPostResponse, PostResponse, PostsListResponse
from app.services.posts.validators import validate_image, validate_user_id
from app.services.posts.image_processor import generate_thumbnail, image_to_bytes, get_image_format
from app.services.posts.storage_client import posts_storage_client
from app.services.posts.mongodb_client import posts_mongodb_client
from app.services.posts.schemas import PostMetadata
from app.services.posts.utils import generate_post_id, get_storage_path
import logging

logger = logging.getLogger("posts_service")

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post(
    "/upload",
    response_model=UploadPostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a post",
    description="Upload an image post with optional text. Returns post ID and URLs."
)
async def upload_post(
    file: UploadFile = File(..., description="Image file (JPG or PNG)"),
    user_id: str = Form(..., description="User identifier"),
    text: str = Form(None, description="Optional text content")
) -> UploadPostResponse:
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
        
        # Upload original image
        original_path = get_storage_path(post_id, file.filename or f"image.{extension}", "originals")
        logger.info(f"Uploading original image: {original_path}")
        original_url = posts_storage_client.upload_file(
            file_data=original_bytes,
            object_name=original_path,
            content_type=file.content_type or "image/jpeg"
        )
        
        # Upload thumbnail
        thumbnail_path = get_storage_path(post_id, file.filename or f"image.{extension}", "thumbnails")
        logger.info(f"Uploading thumbnail: {thumbnail_path}")
        thumbnail_url = posts_storage_client.upload_file(
            file_data=thumbnail_bytes,
            object_name=thumbnail_path,
            content_type=file.content_type or "image/jpeg"
        )
        
        # Create post metadata
        metadata = PostMetadata(
            post_id=post_id,
            user_id=user_id,
            text=text if text else None,
            image_url=original_url,
            thumbnail_url=thumbnail_url
        )
        
        # Store in MongoDB
        logger.info(f"Storing post metadata in MongoDB: {post_id}")
        success = posts_mongodb_client.create_post(metadata)
        
        if not success:
            logger.error(f"Failed to store post metadata: {post_id}")
            # Try to clean up uploaded files
            try:
                posts_storage_client.delete_file(original_path)
                posts_storage_client.delete_file(thumbnail_path)
            except Exception as cleanup_error:
                logger.error(f"Error cleaning up files: {str(cleanup_error)}")
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store post metadata"
            )
        
        logger.info(f"Post uploaded successfully: {post_id}")
        
        return UploadPostResponse(
            post_id=post_id,
            status="uploaded",
            image_url=original_url,
            thumbnail_url=thumbnail_url,
            message="Post uploaded successfully"
        )
        
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
    response_model=PostResponse,
    summary="Get post by ID",
    description="Retrieve a post by its unique identifier"
)
async def get_post(post_id: str) -> PostResponse:
    """
    Get a post by ID.
    
    Args:
        post_id: Unique identifier for the post
        
    Returns:
        PostResponse with post data
        
    Raises:
        HTTPException: If post not found
    """
    try:
        post = posts_mongodb_client.get_post(post_id)
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post not found: {post_id}"
            )
        
        return PostResponse(**post)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve post: {str(e)}"
        )


@router.get(
    "/user/{user_id}",
    response_model=PostsListResponse,
    summary="Get user posts",
    description="Retrieve all posts for a specific user"
)
async def get_user_posts(user_id: str, limit: int = 50) -> PostsListResponse:
    """
    Get all posts for a user.
    
    Args:
        user_id: Unique identifier for the user
        limit: Maximum number of posts to return (default: 50)
        
    Returns:
        PostsListResponse with list of posts
    """
    try:
        posts = posts_mongodb_client.get_user_posts(user_id, limit=limit)
        
        return PostsListResponse(
            posts=posts,
            count=len(posts)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving user posts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user posts: {str(e)}"
        )


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete post",
    description="Delete a post by its unique identifier"
)
async def delete_post(post_id: str):
    """
    Delete a post.
    
    Args:
        post_id: Unique identifier for the post
        
    Raises:
        HTTPException: If post not found or deletion fails
    """
    try:
        # Get post first to find image paths
        post = posts_mongodb_client.get_post(post_id)
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post not found: {post_id}"
            )
        
        # Delete from MongoDB
        success = posts_mongodb_client.delete_post(post_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete post from database"
            )
        
        # Try to delete images from storage (don't fail if this fails)
        try:
            if "image_url" in post:
                # Extract object name from URL
                # URL format: http://endpoint/bucket/path
                image_url = post.get("image_url", "")
                if image_url:
                    # Extract path after bucket name
                    parts = image_url.split("/")
                    if len(parts) > 3:
                        object_path = "/".join(parts[3:])  # Skip http://, endpoint, bucket
                        posts_storage_client.delete_file(object_path)
            
            if "thumbnail_url" in post:
                thumbnail_url = post.get("thumbnail_url", "")
                if thumbnail_url:
                    parts = thumbnail_url.split("/")
                    if len(parts) > 3:
                        object_path = "/".join(parts[3:])
                        posts_storage_client.delete_file(object_path)
        except Exception as storage_error:
            logger.warning(f"Failed to delete images from storage: {str(storage_error)}")
            # Don't fail the request if storage deletion fails
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete post: {str(e)}"
        )


@router.get(
    "/feed",
    response_model=PostsListResponse,
    summary="Get feed",
    description="Retrieve all posts for the feed (paginated)"
)
async def get_feed(limit: int = 50, skip: int = 0) -> PostsListResponse:
    """
    Get feed of all posts.
    
    Args:
        limit: Maximum number of posts to return (default: 50)
        skip: Number of posts to skip for pagination (default: 0)
        
    Returns:
        PostsListResponse with list of posts
    """
    try:
        posts = posts_mongodb_client.get_all_posts(limit=limit, skip=skip)
        
        return PostsListResponse(
            posts=posts,
            count=len(posts)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving feed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve feed: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check endpoint",
    description="Check if the Post Service is running"
)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        Status dictionary
    """
    return {
        "status": "healthy",
        "service": "Post Upload + Storage Service"
    }
