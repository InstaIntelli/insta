"""
Image processing utilities using Pillow.
"""

import io
from typing import Tuple
from PIL import Image

from .config import settings
from .utils import logger


def generate_thumbnail(image: Image.Image, size: Tuple[int, int] = None) -> Image.Image:
    """
    Generate a thumbnail from an image while maintaining aspect ratio.
    
    Args:
        image: PIL Image object
        size: Target size tuple (width, height). Defaults to settings.thumbnail_size
        
    Returns:
        Thumbnail PIL Image object
    """
    if size is None:
        size = settings.thumbnail_size
    
    try:
        # Calculate thumbnail size maintaining aspect ratio
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Create a new image with the thumbnail
        thumbnail = image.copy()
        
        logger.info(f"Thumbnail generated: {thumbnail.size}")
        return thumbnail
        
    except Exception as e:
        logger.error(f"Error generating thumbnail: {str(e)}")
        raise ValueError(f"Failed to generate thumbnail: {str(e)}")


def image_to_bytes(image: Image.Image, format: str = "JPEG") -> bytes:
    """
    Convert PIL Image to bytes.
    
    Args:
        image: PIL Image object
        format: Image format (JPEG, PNG, etc.)
        
    Returns:
        Image bytes
    """
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
    """
    Get PIL format string from file extension.
    
    Args:
        extension: File extension (e.g., '.jpg', '.png')
        
    Returns:
        PIL format string (JPEG, PNG, etc.)
    """
    extension = extension.lower().lstrip('.')
    format_map = {
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'png': 'PNG'
    }
    return format_map.get(extension, 'JPEG')

