"""
FastAPI routes for Post Upload + Storage Service.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse

from .schemas import UploadPostResponse
from .validators import validate_image, validate_user_id
from .image_processor import generate_thumbnail, image_to_bytes, get_image_format
from .storage_client import storage_client
from .mongodb_client import mongodb_client
from .schemas import PostMetadata
from .utils import logger, generate_post_id, get_storage_path

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
        original_url = storage_client.upload_file(
            file_data=original_bytes,
            object_name=original_path,
            content_type=file.content_type or "image/jpeg"
        )
        
        # Upload thumbnail
        thumbnail_path = get_storage_path(post_id, file.filename or f"image.{extension}", "thumbnails")
        logger.info(f"Uploading thumbnail: {thumbnail_path}")
        thumbnail_url = storage_client.upload_file(
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
        success = mongodb_client.create_post(metadata)
        
        if not success:
            logger.error(f"Failed to store post metadata: {post_id}")
            # Try to clean up uploaded files
            try:
                storage_client.delete_file(original_path)
                storage_client.delete_file(thumbnail_path)
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
    "/health",
    summary="Health check endpoint",
    description="Check if the Post Upload + Storage Service is running"
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

