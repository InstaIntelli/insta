"""
Analytics API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_user
from app.services.analytics import (
    get_user_analytics, get_platform_analytics, get_top_performing_posts
)

router = APIRouter()


@router.get("/user")
async def get_user_analytics_endpoint(
    current_user: dict = Depends(get_current_user)
):
    """Get analytics for current user"""
    try:
        user_id = current_user.get("user_id")
        analytics = get_user_analytics(user_id)
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user analytics: {str(e)}"
        )


@router.get("/user/{user_id}")
async def get_user_analytics_by_id_endpoint(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get analytics for a specific user (if authorized)"""
    try:
        # In production, add authorization check here
        analytics = get_user_analytics(user_id)
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user analytics: {str(e)}"
        )


@router.get("/platform")
async def get_platform_analytics_endpoint(
    current_user: dict = Depends(get_current_user)
):
    """Get platform-wide analytics (admin only in production)"""
    try:
        analytics = get_platform_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get platform analytics: {str(e)}"
        )


@router.get("/top-posts/{user_id}")
async def get_top_posts_endpoint(
    user_id: str,
    limit: int = 5,
    current_user: dict = Depends(get_current_user)
):
    """Get top performing posts for a user"""
    try:
        posts = get_top_performing_posts(user_id, limit=limit)
        return {
            "posts": posts,
            "count": len(posts)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get top posts: {str(e)}"
        )

