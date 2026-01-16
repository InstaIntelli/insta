"""
Profile Management Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from app.core.config import settings

from app.db.postgres import get_db
from app.api.dependencies import get_current_user
from app.services.profile import (
    get_user_profile,
    update_profile,
    change_password,
    upload_profile_picture
)
import logging

logger = logging.getLogger(__name__)

# Helper to rewrite image URLs
def get_proxied_image_url(original_url: Optional[str]) -> Optional[str]:
    if not original_url:
        return None
    
    # Extract path from various URL formats
    object_path = None
    if "/instaintelli-media/" in original_url:
        object_path = original_url.split("/instaintelli-media/")[-1]
    elif "minio:9000" in original_url or "localhost:9000" in original_url:
        parts = original_url.split("/")
        if len(parts) > 3:
            object_path = "/".join(parts[3:])
    elif "s3.amazonaws" in original_url:
        # Don't proxy external S3 URLs
        return original_url
            
    if object_path:
        # Use backend proxy endpoint
        return f"http://localhost:8000/api/v1/profile/images/{object_path}"
    
    return original_url


router = APIRouter(prefix="/profile", tags=["Profile"])


# Pydantic schemas
class UpdateProfileRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    
    class Config:
        # Allow partial updates (all fields optional)
        extra = "forbid"


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6, max_length=50)


class ProfileResponse(BaseModel):
    user_id: str
    email: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    created_at: Optional[str] = None
    posts_count: Optional[int] = 0
    followers_count: Optional[int] = 0
    following_count: Optional[int] = 0


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile
    
    Returns:
        User profile data
    """
    try:
        user = get_user_profile(db, current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        response = user.to_safe_dict()
        response['profile_image_url'] = get_proxied_image_url(response.get('profile_image_url'))
        
        return ProfileResponse(**response)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get profile"
        )


@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile - Optimized for performance
    
    Args:
        profile_data: Profile update data (all fields optional)
        
    Returns:
        Updated user profile
    """
    try:
        # Only pass fields that are provided (not None)
        update_kwargs = {}
        if profile_data.username is not None:
            update_kwargs['username'] = profile_data.username
        if profile_data.full_name is not None:
            update_kwargs['full_name'] = profile_data.full_name
        if profile_data.bio is not None:
            update_kwargs['bio'] = profile_data.bio
        
        # Only update if there's something to update
        if not update_kwargs:
            # Return current profile if nothing to update
            from app.services.auth import get_user_by_user_id
            user = get_user_by_user_id(db, current_user["user_id"])
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            response = user.to_safe_dict()
            response['profile_image_url'] = get_proxied_image_url(response.get('profile_image_url'))
            return ProfileResponse(**response)
        
        user = update_profile(
            db=db,
            user_id=current_user["user_id"],
            **update_kwargs
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        response = user.to_safe_dict()
        response['profile_image_url'] = get_proxied_image_url(response.get('profile_image_url'))
        return ProfileResponse(**response)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.post("/me/picture", response_model=ProfileResponse)
async def upload_my_profile_picture(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload profile picture
    
    Args:
        file: Image file (JPG, PNG, etc.)
        
    Returns:
        Updated user profile with new picture URL
    """
    try:
        profile_url = upload_profile_picture(
            db=db,
            user_id=current_user["user_id"],
            file=file
        )
        
        user = get_user_profile(db, current_user["user_id"], use_cache=False)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        response = user.to_safe_dict()
        response['profile_image_url'] = get_proxied_image_url(response.get('profile_image_url'))
        return ProfileResponse(**response)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading profile picture: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload profile picture"
        )


@router.post("/me/password")
async def change_my_password(
    password_data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password
    
    Args:
        password_data: Current and new password
        
    Returns:
        Success message
    """
    try:
        change_password(
            db=db,
            user_id=current_user["user_id"],
            current_password=password_data.current_password,
            new_password=password_data.new_password
        )
        
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_user_profile_by_id(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get user profile by user_id (public) with counts
    
    Args:
        user_id: User ID
        
    Returns:
        User profile data with posts, followers, and following counts
    """
    try:
        user = get_user_profile(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get counts from different services
        from app.services.posts.mongodb_client import posts_mongodb_client
        from app.services.social import get_follower_count, get_following_count
        
        # Get posts count
        try:
            posts = posts_mongodb_client.get_user_posts(user_id, limit=1000)
            posts_count = len(posts)
        except Exception as e:
            logger.warning(f"Error getting posts count: {str(e)}")
            posts_count = 0
        
        # Get followers and following counts
        try:
            followers_count = get_follower_count(user_id)
            following_count = get_following_count(user_id)
        except Exception as e:
            logger.warning(f"Error getting social counts: {str(e)}")
            followers_count = 0
            following_count = 0
        
        # Add counts to response
        profile_dict = user.to_safe_dict()
        profile_dict['posts_count'] = posts_count
        profile_dict['followers_count'] = followers_count
        profile_dict['following_count'] = following_count
        profile_dict['profile_image_url'] = get_proxied_image_url(profile_dict.get('profile_image_url'))
        
        return ProfileResponse(**profile_dict)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get profile"
        )


@router.get("/images/{path:path}")
async def get_image(path: str):
    """
    Proxy profile images from MinIO
    """
    try:
        from app.services.profile import profile_storage
        
        # Use MinIO client directly
        minio_client = profile_storage.client
        bucket_name = profile_storage.bucket_name
        
        if not minio_client:
             raise HTTPException(status_code=503, detail="Storage unavailable")

        # Stream image
        try:
            response = minio_client.get_object(bucket_name, path)
            image_data = response.read()
            response.close()
            
            # Determine content type
            content_type = "image/jpeg"
            if path.endswith(".png"): content_type = "image/png"
            elif path.endswith(".gif"): content_type = "image/gif"
            
            from fastapi.responses import Response
            return Response(
                content=image_data,
                media_type=content_type,
                headers={
                    "Cache-Control": "public, max-age=31536000, immutable",
                    "Access-Control-Allow-Origin": "*"
                }
            )
        except Exception:
            raise HTTPException(status_code=404, detail="Image not found")
            
    except HTTPException:
        raise
    except Exception as e:
         logger.error(f"Error serving image: {str(e)}")
         raise HTTPException(status_code=500, detail="Internal Error")
