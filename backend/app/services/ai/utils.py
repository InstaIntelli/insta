"""
Utility functions for the AI Processing Service.
"""

import logging
from typing import List, Optional
from datetime import datetime


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("ai_service")


def parse_topics(topics_string: str) -> List[str]:
    """
    Parse comma-separated topics string into list.
    
    Args:
        topics_string: Comma-separated topics string
        
    Returns:
        List of cleaned topic strings
    """
    if not topics_string:
        return []
    
    topics = [topic.strip() for topic in topics_string.split(",")]
    return [topic for topic in topics if topic]


def combine_content(text: Optional[str], caption: Optional[str]) -> str:
    """
    Combine text and caption into a single content string.
    
    Args:
        text: Post text content
        caption: Post caption
        
    Returns:
        Combined content string
    """
    parts = []
    if text:
        parts.append(text)
    if caption:
        parts.append(caption)
    
    return " ".join(parts) if parts else ""


def validate_post_id(post_id: str) -> bool:
    """
    Validate post ID format.
    
    Args:
        post_id: Post identifier to validate
        
    Returns:
        True if valid, False otherwise
    """
    return bool(post_id and isinstance(post_id, str) and len(post_id.strip()) > 0)


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format.
    
    Args:
        user_id: User identifier to validate
        
    Returns:
        True if valid, False otherwise
    """
    return bool(user_id and isinstance(user_id, str) and len(user_id.strip()) > 0)

