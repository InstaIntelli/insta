"""
Profile Management Service
Handles user profile updates, picture uploads, and caching
"""

from typing import Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
import logging

from app.models.auth import User
from app.services.auth import get_user_by_user_id, get_user_by_username, update_user_profile
from app.core.security import verify_password, get_password_hash
from app.db.redis import cache_get, cache_set, cache_key_profile
from app.services.profile.storage import ProfileStorageClient
import uuid

logger = logging.getLogger(__name__)

# Initialize storage client
profile_storage = ProfileStorageClient()


def get_user_profile(db: Session, user_id: str, use_cache: bool = True) -> Optional[User]:
    """
    Get user profile with Redis caching
    
    Args:
        db: Database session
        user_id: User ID
        use_cache: Whether to use cache
        
    Returns:
        User object or None
    """
    # Try cache first
    if use_cache:
        cache_key = cache_key_profile(user_id)
        cached = cache_get(cache_key)
        if cached:
            logger.debug(f"Profile cache hit for {user_id}")
            # Reconstruct user from cache (simplified)
            user = get_user_by_user_id(db, user_id)
            if user:
                return user
    
    # Get from database
    user = get_user_by_user_id(db, user_id)
    
    # Cache the result
    if user and use_cache:
        cache_key = cache_key_profile(user_id)
        cache_set(cache_key, user.to_safe_dict(), expire_seconds=300)  # 5 min cache
    
    return user


def update_profile(
    db: Session,
    user_id: str,
    username: Optional[str] = None,
    full_name: Optional[str] = None,
    bio: Optional[str] = None,
    profile_image_url: Optional[str] = None
) -> Optional[User]:
    """
    Update user profile - Optimized for performance
    
    Args:
        db: Database session
        user_id: User ID
        username: New username (must be unique)
        full_name: New full name
        bio: New bio
        profile_image_url: New profile image URL
        
    Returns:
        Updated user object or None
        
    Raises:
        HTTPException: If username is taken or update fails
    """
    try:
        # Get user in single query
        user = get_user_by_user_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check username uniqueness only if changing (optimized query)
        if username and username != user.username:
            from sqlalchemy import select
            from app.models.auth import User as UserModel
            # Single query to check if username exists for different user
            existing = db.execute(
                select(UserModel).where(
                    UserModel.username == username,
                    UserModel.user_id != user_id
                )
            ).scalar_one_or_none()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
            user.username = username
        
        # Update fields only if provided (minimal writes)
        updated = False
        if full_name is not None and user.full_name != full_name:
            user.full_name = full_name
            updated = True
        if bio is not None and user.bio != bio:
            user.bio = bio
            updated = True
        if profile_image_url is not None and user.profile_image_url != profile_image_url:
            user.profile_image_url = profile_image_url
            updated = True
        
        # Only commit if something changed
        if updated or (username and username != user.username):
            db.commit()
            # Refresh only if we committed
            db.refresh(user)
            
            # Update cache asynchronously (non-blocking)
            try:
                cache_key = cache_key_profile(user_id)
                cache_set(cache_key, user.to_safe_dict(), expire_seconds=300)
            except Exception as cache_err:
                # Don't fail the request if cache fails
                logger.warning(f"Cache update failed (non-critical): {str(cache_err)}")
        
        logger.info(f"Profile updated for user: {user_id}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )


def change_password(
    db: Session,
    user_id: str,
    current_password: str,
    new_password: str
) -> bool:
    """
    Change user password
    
    Args:
        db: Database session
        user_id: User ID
        current_password: Current password
        new_password: New password
        
    Returns:
        True if successful
        
    Raises:
        HTTPException: If current password is wrong or user has no password (OAuth user)
    """
    try:
        user = get_user_by_user_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # OAuth users may not have a password
        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password cannot be changed for OAuth accounts. Please use your OAuth provider to change your password."
            )
        
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        # Update password
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        
        logger.info(f"Password changed for user: {user_id}")
        return True
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error changing password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )


def upload_profile_picture(
    db: Session,
    user_id: str,
    file: UploadFile
) -> str:
    """
    Upload profile picture to MinIO
    
    Args:
        db: Database session
        user_id: User ID
        file: Image file
        
    Returns:
        URL of uploaded profile picture
        
    Raises:
        HTTPException: If upload fails or file is invalid
    """
    try:
        # Validate file
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read file
        file_data = file.file.read()
        if len(file_data) > 5 * 1024 * 1024:  # 5MB limit
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 5MB"
            )
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        object_name = f"profiles/{user_id}/{uuid.uuid4().hex}.{file_extension}"
        
        # Upload to MinIO
        profile_url = profile_storage.upload_file(
            file_data=file_data,
            object_name=object_name,
            content_type=file.content_type
        )
        
        # Update user profile
        user = get_user_by_user_id(db, user_id)
        if user:
            user.profile_image_url = profile_url
            db.commit()
            db.refresh(user)
            
            # Invalidate cache
            cache_key = cache_key_profile(user_id)
            cache_set(cache_key, user.to_safe_dict(), expire_seconds=300)
        
        logger.info(f"Profile picture uploaded for user: {user_id}")
        return profile_url
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading profile picture: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload profile picture: {str(e)}"
        )
