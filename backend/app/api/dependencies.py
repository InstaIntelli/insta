"""
API Dependencies
Shared dependencies for API endpoints
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user as _get_current_user

# Re-export get_current_user for convenience
get_current_user = _get_current_user

def get_current_user_optional(current_user: Optional[dict] = Depends(_get_current_user)) -> Optional[dict]:
    """
    Optional current user dependency - doesn't raise error if not authenticated
    Returns None if user is not authenticated
    """
    try:
        return current_user
    except HTTPException:
        return None
    except Exception:
        return None


