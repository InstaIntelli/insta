"""
File validation utilities.
"""

import io
from typing import Tuple
from fastapi import UploadFile, HTTPException, status
from PIL import Image

from .config import settings
from .utils import logger


def validate_file_type(file: UploadFile) -> None:
    """
    Validate that the uploaded file is an allowed image type.
    
    Args:
        file: Uploaded file object
        
    Raises:
        HTTPException: If file type is not allowed
    """
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content type is missing"
        )
    
    if file.content_type not in settings.allowed_image_types:
        allowed = ", ".join(settings.allowed_image_types)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {allowed}"
        )


def validate_file_size(file: UploadFile) -> None:
    """
    Validate that the uploaded file size is within limits.
    
    Args:
        file: Uploaded file object
        
    Raises:
        HTTPException: If file size exceeds limit
    """
    if not file.size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size is missing"
        )
    
    if file.size > settings.max_upload_size_bytes:
        max_mb = settings.max_upload_size_mb
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {max_mb}MB"
        )


def validate_image(file: UploadFile) -> Tuple[Image.Image, str]:
    """
    Validate and open image file.
    
    Args:
        file: Uploaded file object
        
    Returns:
        Tuple of (PIL Image object, file extension)
        
    Raises:
        HTTPException: If image is invalid or corrupted
    """
    try:
        # Read file content
        file_content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        # Validate file type
        validate_file_type(file)
        
        # Validate file size
        validate_file_size(file)
        
        # Try to open image with PIL
        try:
            image = Image.open(io.BytesIO(file_content))
            # Verify it's actually an image
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


def validate_user_id(user_id: str) -> None:
    """
    Validate user ID.
    
    Args:
        user_id: User identifier
        
    Raises:
        HTTPException: If user ID is invalid
    """
    if not user_id or not isinstance(user_id, str) or not user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id"
        )

