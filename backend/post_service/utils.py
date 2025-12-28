"""
Utility functions for the Post Upload + Storage Service.
"""

import uuid
import logging
from datetime import datetime
from pathlib import Path


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("post_service")


def generate_post_id() -> str:
    """
    Generate a unique post ID.
    
    Returns:
        Unique post identifier string
    """
    return f"post_{uuid.uuid4().hex[:12]}"


def get_file_extension(filename: str) -> str:
    """
    Extract file extension from filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension (e.g., '.jpg', '.png')
    """
    return Path(filename).suffix.lower()


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format.
    
    Args:
        user_id: User identifier to validate
        
    Returns:
        True if valid, False otherwise
    """
    return bool(user_id and isinstance(user_id, str) and len(user_id.strip()) > 0)


def get_storage_path(post_id: str, filename: str, folder: str = "originals") -> str:
    """
    Generate storage path for a file.
    
    Args:
        post_id: Unique identifier for the post
        filename: Original filename
        folder: Folder name (originals or thumbnails)
        
    Returns:
        Storage path string
    """
    extension = get_file_extension(filename)
    return f"{folder}/{post_id}{extension}"

