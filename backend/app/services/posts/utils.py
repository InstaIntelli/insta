"""
Utility functions for post operations.
"""

import uuid
import logging
from pathlib import Path

logger = logging.getLogger("posts_service")


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


