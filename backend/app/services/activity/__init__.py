"""
User Activity Logging Service
Uses Cassandra for high-performance time-series activity logging
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from uuid import uuid4
import json
import logging
from cassandra.query import SimpleStatement
from cassandra.util import uuid_from_time
from app.db.cassandra import cassandra_client
from app.core.config import settings

logger = logging.getLogger(__name__)


class ActivityService:
    """Service for logging and retrieving user activities"""
    
    def __init__(self):
        self.client = cassandra_client
    
    def log_activity(
        self,
        user_id: str,
        activity_type: str,
        activity_data: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> bool:
        """
        Log a user activity
        
        Args:
            user_id: User ID
            activity_type: Type of activity (e.g., 'login', 'post_created', 'like', 'comment')
            activity_data: Additional activity data as dictionary
            ip_address: User's IP address
            user_agent: User's browser/device info
            
        Returns:
            True if successful
        """
        try:
            if not self.client.is_connected():
                self.client.connect()
            
            session = self.client.get_session()
            if not session:
                logger.error("Cassandra session not available")
                return False
            
            # Generate time-based UUID for sorting
            activity_id = uuid_from_time(datetime.utcnow())
            timestamp = datetime.utcnow()
            
            # Convert activity_data to JSON string
            activity_data_json = json.dumps(activity_data) if activity_data else "{}"
            
            # Insert activity
            insert_query = """
            INSERT INTO user_activities 
            (user_id, activity_id, activity_type, activity_data, timestamp, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            session.execute(
                insert_query,
                (
                    user_id,
                    activity_id,
                    activity_type,
                    activity_data_json,
                    timestamp,
                    ip_address or "",
                    user_agent or ""
                )
            )
            
            # Also log to analytics table for aggregated queries
            self._log_analytics_event(activity_type, user_id, activity_data, timestamp)
            
            logger.debug(f"Logged activity: {activity_type} for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging activity: {str(e)}", exc_info=True)
            return False
    
    def _log_analytics_event(
        self,
        event_type: str,
        user_id: str,
        event_data: Dict[str, Any],
        timestamp: datetime
    ):
        """Log event to analytics table for aggregated queries"""
        try:
            session = self.client.get_session()
            if not session:
                return
            
            event_date = timestamp.date()
            event_id = uuid_from_time(timestamp)
            event_data_json = json.dumps(event_data) if event_data else "{}"
            
            insert_query = """
            INSERT INTO analytics_events 
            (event_date, event_id, event_type, user_id, event_data, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            session.execute(
                insert_query,
                (
                    event_date,
                    event_id,
                    event_type,
                    user_id,
                    event_data_json,
                    timestamp
                )
            )
        except Exception as e:
            logger.warning(f"Error logging analytics event: {str(e)}")
            # Don't fail the main activity log if analytics fails
    
    def get_user_activities(
        self,
        user_id: str,
        activity_type: Optional[str] = None,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get user activities
        
        Args:
            user_id: User ID
            activity_type: Filter by activity type (optional)
            limit: Maximum number of activities to return
            start_time: Start time filter (optional)
            end_time: End time filter (optional)
            
        Returns:
            List of activity dictionaries
        """
        try:
            if not self.client.is_connected():
                self.client.connect()
            
            session = self.client.get_session()
            if not session:
                return []
            
            # Build query
            if activity_type:
                query = """
                SELECT activity_id, activity_type, activity_data, timestamp, ip_address, user_agent
                FROM user_activities
                WHERE user_id = ? AND activity_type = ?
                LIMIT ?
                """
                result = session.execute(query, (user_id, activity_type, limit))
            else:
                query = """
                SELECT activity_id, activity_type, activity_data, timestamp, ip_address, user_agent
                FROM user_activities
                WHERE user_id = ?
                LIMIT ?
                """
                result = session.execute(query, (user_id, limit))
            
            activities = []
            for row in result:
                activity_data = json.loads(row.activity_data) if row.activity_data else {}
                activities.append({
                    "activity_id": str(row.activity_id),
                    "activity_type": row.activity_type,
                    "activity_data": activity_data,
                    "timestamp": row.timestamp.isoformat() if row.timestamp else None,
                    "ip_address": row.ip_address,
                    "user_agent": row.user_agent
                })
            
            # Filter by time range if provided
            if start_time or end_time:
                filtered = []
                for activity in activities:
                    if activity["timestamp"]:
                        activity_time = datetime.fromisoformat(activity["timestamp"].replace('Z', '+00:00'))
                        if start_time and activity_time < start_time:
                            continue
                        if end_time and activity_time > end_time:
                            continue
                    filtered.append(activity)
                activities = filtered
            
            return activities
            
        except Exception as e:
            logger.error(f"Error getting user activities: {str(e)}", exc_info=True)
            return []
    
    def get_analytics(
        self,
        event_type: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Get analytics events for a date range
        
        Args:
            event_type: Type of event
            start_date: Start date
            end_date: End date
            
        Returns:
            List of analytics events
        """
        try:
            if not self.client.is_connected():
                self.client.connect()
            
            session = self.client.get_session()
            if not session:
                return []
            
            events = []
            current_date = start_date.date()
            end_date_only = end_date.date()
            
            # Query each date in range
            while current_date <= end_date_only:
                query = """
                SELECT event_id, user_id, event_data, timestamp
                FROM analytics_events
                WHERE event_date = ? AND event_type = ?
                LIMIT 10000
                """
                
                result = session.execute(query, (current_date, event_type))
                
                for row in result:
                    event_data = json.loads(row.event_data) if row.event_data else {}
                    events.append({
                        "event_id": str(row.event_id),
                        "user_id": row.user_id,
                        "event_data": event_data,
                        "timestamp": row.timestamp.isoformat() if row.timestamp else None
                    })
                
                current_date += timedelta(days=1)
            
            return events
            
        except Exception as e:
            logger.error(f"Error getting analytics: {str(e)}", exc_info=True)
            return []
    
    def get_activity_stats(
        self,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get activity statistics for a user
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            Dictionary with activity statistics
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            activities = self.get_user_activities(
                user_id=user_id,
                limit=10000,
                start_time=start_time,
                end_time=end_time
            )
            
            # Count by type
            type_counts = {}
            for activity in activities:
                activity_type = activity.get("activity_type", "unknown")
                type_counts[activity_type] = type_counts.get(activity_type, 0) + 1
            
            return {
                "total_activities": len(activities),
                "activities_by_type": type_counts,
                "period_days": days,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting activity stats: {str(e)}", exc_info=True)
            return {
                "total_activities": 0,
                "activities_by_type": {},
                "period_days": days
            }


# Global instance
activity_service = ActivityService()
