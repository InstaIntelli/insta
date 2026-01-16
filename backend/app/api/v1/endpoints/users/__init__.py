"""
User profile endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from app.db.postgres import get_db
from app.services.auth import get_user_by_user_id, get_user_by_username, update_user_profile
from app.core.security import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


# Pydantic schemas
class UserProfile(BaseModel):
    user_id: str
    email: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    created_at: Optional[str] = None


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    profile_image_url: Optional[str] = Field(None, max_length=500)


@router.get("/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """
    Get user profile by user ID
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        User profile
    """
    try:
        user = get_user_by_user_id(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfile(**user.to_safe_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )


@router.get("/username/{username}", response_model=UserProfile)
async def get_user_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    """
    Get user profile by username
    
    Args:
        username: Username
        db: Database session
        
    Returns:
        User profile
    """
    try:
        user = get_user_by_username(db, username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfile(**user.to_safe_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user by username: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )


@router.put("/{user_id}", response_model=UserProfile)
async def update_user(
    user_id: str,
    update_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile (users can only update their own profile)
    
    Args:
        user_id: User ID to update
        update_data: Updated profile data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated user profile
    """
    try:
        # Check if user is updating their own profile
        if current_user["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this profile"
            )
        
        # Update profile
        user = update_user_profile(
            db=db,
            user_id=user_id,
            full_name=update_data.full_name,
            bio=update_data.bio,
            profile_image_url=update_data.profile_image_url
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfile(**user.to_safe_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "User Profile Service"
    }
