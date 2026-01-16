"""
Analytics Service
Provides user engagement metrics, post performance analytics, and insights
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from app.db.neo4j import get_driver
from app.services.posts.mongodb_client import posts_mongodb_client
from app.services.social import (
    get_follower_count, get_following_count, get_like_count, get_comment_count,
    get_followers, get_following, get_likers
)
import logging

logger = logging.getLogger("analytics_service")


def get_user_analytics(user_id: str) -> Dict[str, Any]:
    """
    Get comprehensive analytics for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        Dictionary with analytics data
    """
    try:
        # Get user's posts
        user_posts = posts_mongodb_client.get_user_posts(user_id, limit=1000)
        
        # Calculate metrics
        total_posts = len(user_posts)
        total_likes = 0
        total_comments = 0
        total_views = 0  # Placeholder - would need view tracking
        
        # Engagement over time (last 30 days)
        engagement_by_day = {}
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        for post in user_posts:
            post_id = post.get("post_id")
            if post_id:
                likes = get_like_count(post_id)
                comments = get_comment_count(post_id)
                total_likes += likes
                total_comments += comments
                
                # Track engagement by day
                created_at = post.get("created_at")
                if isinstance(created_at, str):
                    try:
                        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    except:
                        continue
                elif not isinstance(created_at, datetime):
                    continue
                
                if created_at.replace(tzinfo=None) >= thirty_days_ago.replace(tzinfo=None):
                    day_key = created_at.strftime("%Y-%m-%d")
                    if day_key not in engagement_by_day:
                        engagement_by_day[day_key] = {"likes": 0, "comments": 0, "posts": 0}
                    engagement_by_day[day_key]["likes"] += likes
                    engagement_by_day[day_key]["comments"] += comments
                    engagement_by_day[day_key]["posts"] += 1
        
        # Calculate averages
        avg_likes_per_post = total_likes / total_posts if total_posts > 0 else 0
        avg_comments_per_post = total_comments / total_posts if total_posts > 0 else 0
        engagement_rate = ((total_likes + total_comments) / (total_posts * 100)) * 100 if total_posts > 0 else 0
        
        # Follower metrics
        followers_count = get_follower_count(user_id)
        following_count = get_following_count(user_id)
        follower_growth = calculate_follower_growth(user_id)
        
        # Top performing posts
        top_posts = get_top_performing_posts(user_id, limit=5)
        
        # Best posting times
        best_posting_times = analyze_best_posting_times(user_posts)
        
        return {
            "user_id": user_id,
            "overview": {
                "total_posts": total_posts,
                "total_likes": total_likes,
                "total_comments": total_comments,
                "total_views": total_views,
                "followers": followers_count,
                "following": following_count,
                "avg_likes_per_post": round(avg_likes_per_post, 2),
                "avg_comments_per_post": round(avg_comments_per_post, 2),
                "engagement_rate": round(engagement_rate, 2)
            },
            "engagement_timeline": engagement_by_day,
            "follower_growth": follower_growth,
            "top_posts": top_posts,
            "best_posting_times": best_posting_times,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting user analytics: {str(e)}")
        return {
            "user_id": user_id,
            "error": str(e)
        }


def calculate_follower_growth(user_id: str, days: int = 30) -> List[Dict[str, Any]]:
    """
    Calculate follower growth over time.
    
    Args:
        user_id: User ID
        days: Number of days to analyze
        
    Returns:
        List of daily follower counts
    """
    try:
        # This is a simplified version - in production, you'd track follower history
        # For now, we'll return current count
        current_count = get_follower_count(user_id)
        
        growth_data = []
        for i in range(days, -1, -1):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            # Simplified: assume linear growth (in production, track actual history)
            estimated_count = max(0, current_count - (days - i))
            growth_data.append({
                "date": date,
                "followers": estimated_count
            })
        
        return growth_data
    except Exception as e:
        logger.error(f"Error calculating follower growth: {str(e)}")
        return []


def get_top_performing_posts(user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get top performing posts for a user.
    
    Args:
        user_id: User ID
        limit: Number of posts to return
        
    Returns:
        List of top posts with metrics
    """
    try:
        posts = posts_mongodb_client.get_user_posts(user_id, limit=100)
        
        scored_posts = []
        for post in posts:
            post_id = post.get("post_id")
            if post_id:
                likes = get_like_count(post_id)
                comments = get_comment_count(post_id)
                score = likes + (comments * 2)  # Comments weighted more
                
                scored_posts.append({
                    "post_id": post_id,
                    "image_url": post.get("image_url"),
                    "caption": post.get("caption") or post.get("text"),
                    "created_at": post.get("created_at"),
                    "likes": likes,
                    "comments": comments,
                    "engagement_score": score
                })
        
        # Sort by engagement score
        scored_posts.sort(key=lambda x: x.get("engagement_score", 0), reverse=True)
        
        return scored_posts[:limit]
        
    except Exception as e:
        logger.error(f"Error getting top performing posts: {str(e)}")
        return []


def analyze_best_posting_times(posts: List[Dict]) -> Dict[str, Any]:
    """
    Analyze best posting times based on engagement.
    
    Args:
        posts: List of post dictionaries
        
    Returns:
        Dictionary with best posting times analysis
    """
    try:
        hour_engagement = {}
        
        for post in posts:
            post_id = post.get("post_id")
            if not post_id:
                continue
            
            created_at = post.get("created_at")
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    continue
            elif not isinstance(created_at, datetime):
                continue
            
            hour = created_at.hour
            likes = get_like_count(post_id)
            comments = get_comment_count(post_id)
            engagement = likes + comments
            
            if hour not in hour_engagement:
                hour_engagement[hour] = {"total": 0, "count": 0}
            
            hour_engagement[hour]["total"] += engagement
            hour_engagement[hour]["count"] += 1
        
        # Calculate average engagement per hour
        avg_by_hour = {}
        for hour, data in hour_engagement.items():
            avg_by_hour[hour] = data["total"] / data["count"] if data["count"] > 0 else 0
        
        # Find best hours
        if avg_by_hour:
            sorted_hours = sorted(avg_by_hour.items(), key=lambda x: x[1], reverse=True)
            best_hours = [hour for hour, _ in sorted_hours[:3]]
        else:
            best_hours = []
        
        return {
            "best_hours": best_hours,
            "hourly_averages": avg_by_hour,
            "recommendation": f"Best posting times: {', '.join([f'{h}:00' for h in best_hours])}" if best_hours else "Not enough data"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing posting times: {str(e)}")
        return {
            "best_hours": [],
            "hourly_averages": {},
            "recommendation": "Not enough data"
        }


def get_platform_analytics() -> Dict[str, Any]:
    """
    Get platform-wide analytics (admin view).
    
    Returns:
        Dictionary with platform metrics
    """
    try:
        # Get all posts
        all_posts = posts_mongodb_client.get_all_posts(limit=10000, skip=0)
        
        total_posts = len(all_posts)
        total_likes = 0
        total_comments = 0
        active_users = set()
        
        for post in all_posts:
            post_id = post.get("post_id")
            user_id = post.get("user_id")
            if user_id:
                active_users.add(user_id)
            
            if post_id:
                total_likes += get_like_count(post_id)
                total_comments += get_comment_count(post_id)
        
        # Calculate averages
        avg_likes_per_post = total_likes / total_posts if total_posts > 0 else 0
        avg_comments_per_post = total_comments / total_posts if total_posts > 0 else 0
        
        return {
            "total_posts": total_posts,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "active_users": len(active_users),
            "avg_likes_per_post": round(avg_likes_per_post, 2),
            "avg_comments_per_post": round(avg_comments_per_post, 2),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting platform analytics: {str(e)}")
        return {
            "error": str(e)
        }

