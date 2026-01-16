"""
Activity Logging Endpoints
Uses Cassandra for high-performance time-series activity logging
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from app.db.postgres import get_db
from app.api.dependencies import get_current_user
from app.services.activity import activity_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/activity", tags=["Activity"])


# Pydantic schemas
class LogActivityRequest(BaseModel):
    activity_type: str = Field(..., description="Type of activity (e.g., 'login', 'post_created', 'like')")
    activity_data: Dict[str, Any] = Field(default_factory=dict, description="Additional activity data")


class ActivityResponse(BaseModel):
    activity_id: str
    activity_type: str
    activity_data: Dict[str, Any]
    timestamp: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]


class ActivityStatsResponse(BaseModel):
    total_activities: int
    activities_by_type: Dict[str, int]
    period_days: int
    start_time: str
    end_time: str


@router.post("/log", status_code=status.HTTP_201_CREATED)
async def log_activity(
    activity: LogActivityRequest,
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Log a user activity
    
    Args:
        activity: Activity data
        request: FastAPI request (for IP and user agent)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    try:
        # Get IP address and user agent
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent", "")
        
        # Log activity
        success = activity_service.log_activity(
            user_id=current_user["user_id"],
            activity_type=activity.activity_type,
            activity_data=activity.activity_data,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to log activity"
            )
        
        return {
            "message": "Activity logged successfully",
            "activity_type": activity.activity_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging activity: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log activity"
        )


@router.get("/me", response_model=List[ActivityResponse])
async def get_my_activities(
    activity_type: Optional[str] = None,
    limit: int = 100,
    days: int = 30,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's activities
    
    Args:
        activity_type: Filter by activity type (optional)
        limit: Maximum number of activities to return
        days: Number of days to look back
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of activities
    """
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        activities = activity_service.get_user_activities(
            user_id=current_user["user_id"],
            activity_type=activity_type,
            limit=limit,
            start_time=start_time,
            end_time=end_time
        )
        
        return activities
        
    except Exception as e:
        logger.error(f"Error getting activities: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get activities"
        )


@router.get("/me/stats", response_model=ActivityStatsResponse)
async def get_my_activity_stats(
    days: int = 30,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get activity statistics for current user
    
    Args:
        days: Number of days to analyze
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Activity statistics
    """
    try:
        stats = activity_service.get_activity_stats(
            user_id=current_user["user_id"],
            days=days
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting activity stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get activity statistics"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        is_connected = activity_service.client.is_connected()
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "service": "Activity Logging Service",
            "database": "Cassandra",
            "connected": is_connected
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Activity Logging Service",
            "error": str(e)
        }
