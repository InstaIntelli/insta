"""
Recommendations API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.api.dependencies import get_current_user
from app.services.recommendations import (
    get_trending_posts, get_user_recommendations, get_content_recommendations,
    get_hybrid_recommendations, get_popular_users
)

router = APIRouter()


@router.get("/trending")
async def get_trending(
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get trending posts"""
    try:
        user_id = current_user.get("user_id")
        posts = get_trending_posts(limit=limit, user_id=user_id)
        return {
            "posts": posts,
            "count": len(posts),
            "type": "trending"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get trending posts: {str(e)}"
        )


@router.get("/users")
async def get_user_recommendations_endpoint(
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get user recommendations (people you may know)"""
    try:
        user_id = current_user.get("user_id")
        recommendations = get_user_recommendations(user_id, limit=limit)
        return {
            "users": recommendations,
            "count": len(recommendations)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user recommendations: {str(e)}"
        )


@router.get("/content")
async def get_content_recommendations_endpoint(
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get content recommendations based on your interests"""
    try:
        user_id = current_user.get("user_id")
        posts = get_content_recommendations(user_id, limit=limit)
        return {
            "posts": posts,
            "count": len(posts),
            "type": "content_based"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get content recommendations: {str(e)}"
        )


@router.get("/hybrid")
async def get_hybrid_recommendations_endpoint(
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get hybrid recommendations (combines multiple algorithms)"""
    try:
        user_id = current_user.get("user_id")
        posts = get_hybrid_recommendations(user_id, limit=limit)
        return {
            "posts": posts,
            "count": len(posts),
            "type": "hybrid"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(e)}"
        )


@router.get("/popular-users")
async def get_popular_users_endpoint(
    limit: int = 10
):
    """Get popular users"""
    try:
        users = get_popular_users(limit=limit)
        return {
            "users": users,
            "count": len(users)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get popular users: {str(e)}"
        )

