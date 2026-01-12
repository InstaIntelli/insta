"""
Advanced Recommendation Engine
Implements collaborative filtering, content-based, and hybrid recommendations
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from app.db.neo4j import get_driver
from app.services.posts.mongodb_client import posts_mongodb_client
from app.services.social import (
    get_following, get_followers, get_like_count, get_comment_count,
    is_liked, get_likers, get_following_count, get_follower_count
)
import logging
import math

logger = logging.getLogger("recommendations_service")


def calculate_trending_score(post: Dict, current_time: datetime) -> float:
    """
    Calculate trending score using time-decay and engagement metrics.
    Uses Reddit-style algorithm: score = (likes + comments * 2) / time_decay
    
    Args:
        post: Post dictionary with engagement metrics
        current_time: Current timestamp
        
    Returns:
        Trending score (higher = more trending)
    """
    try:
        # Get engagement metrics
        post_id = post.get("post_id")
        if not post_id:
            return 0.0
        
        likes = get_like_count(post_id)
        comments = get_comment_count(post_id)
        
        # Calculate time decay (posts older than 7 days get lower scores)
        created_at = post.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        elif not isinstance(created_at, datetime):
            created_at = datetime.now()
        
        hours_old = (current_time - created_at.replace(tzinfo=None)).total_seconds() / 3600
        
        # Time decay factor (exponential decay)
        # Posts less than 1 hour old: full weight
        # Posts 24 hours old: 0.5 weight
        # Posts 7 days old: 0.1 weight
        if hours_old < 1:
            time_decay = 1.0
        else:
            time_decay = math.exp(-hours_old / 48)  # Half-life of 48 hours
        
        # Engagement score (comments weighted more than likes)
        engagement = likes + (comments * 2)
        
        # Trending score
        if time_decay > 0:
            score = engagement / (time_decay + 0.1)  # Add small constant to avoid division by zero
        else:
            score = engagement
        
        return score
    except Exception as e:
        logger.error(f"Error calculating trending score: {str(e)}")
        return 0.0


def get_trending_posts(limit: int = 20, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get trending posts based on engagement and time-decay algorithm.
    
    Args:
        limit: Maximum number of posts to return
        user_id: Optional user ID to personalize results
        
    Returns:
        List of trending posts with scores
    """
    try:
        # Get recent posts (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        # Fetch posts from MongoDB
        all_posts = posts_mongodb_client.get_all_posts(limit=500, skip=0)  # Get more to filter
        
        # Filter recent posts and calculate scores
        current_time = datetime.now()
        scored_posts = []
        
        for post in all_posts:
            created_at = post.get("created_at")
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    continue
            elif not isinstance(created_at, datetime):
                continue
            
            # Only include posts from last 7 days
            if created_at.replace(tzinfo=None) < seven_days_ago.replace(tzinfo=None):
                continue
            
            score = calculate_trending_score(post, current_time)
            post["trending_score"] = score
            scored_posts.append(post)
        
        # Sort by trending score
        scored_posts.sort(key=lambda x: x.get("trending_score", 0), reverse=True)
        
        # Return top N
        return scored_posts[:limit]
        
    except Exception as e:
        logger.error(f"Error getting trending posts: {str(e)}")
        return []


def get_user_recommendations(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get user recommendations using collaborative filtering.
    Finds users who follow similar people.
    
    Args:
        user_id: User ID to get recommendations for
        limit: Maximum number of recommendations
        
    Returns:
        List of recommended users with similarity scores
    """
    try:
        driver = get_driver()
        if not driver:
            return []
        
        # Get users that current user follows
        following = get_following(user_id)
        following_ids = [f.get("user_id") for f in following]
        
        if not following_ids:
            # If user doesn't follow anyone, recommend popular users
            return get_popular_users(limit)
        
        # Find users who follow similar people (collaborative filtering)
        with driver.session() as session:
            result = session.run("""
                MATCH (current:User {user_id: $user_id})-[r1:FOLLOWS]->(followed:User)
                MATCH (other:User)-[r2:FOLLOWS]->(followed)
                WHERE other.user_id <> $user_id 
                  AND NOT (current)-[:FOLLOWS]->(other)
                WITH other, count(followed) as common_follows
                ORDER BY common_follows DESC
                LIMIT $limit
                RETURN other.user_id as user_id, 
                       other.username as username,
                       common_follows as similarity_score
            """, user_id=user_id, limit=limit)
            
            recommendations = []
            for record in result:
                recommendations.append({
                    "user_id": record["user_id"],
                    "username": record["username"],
                    "similarity_score": record["similarity_score"],
                    "reason": f"Follows {record['similarity_score']} people you follow"
                })
            
            # If not enough recommendations, add popular users
            if len(recommendations) < limit:
                popular = get_popular_users(limit - len(recommendations))
                # Filter out already recommended users
                recommended_ids = {r["user_id"] for r in recommendations}
                for user in popular:
                    if user["user_id"] not in recommended_ids:
                        recommendations.append(user)
            
            return recommendations[:limit]
            
    except Exception as e:
        logger.error(f"Error getting user recommendations: {str(e)}")
        return []


def get_popular_users(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get popular users based on follower count.
    
    Args:
        limit: Maximum number of users
        
    Returns:
        List of popular users
    """
    try:
        driver = get_driver()
        if not driver:
            return []
        
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User)
                OPTIONAL MATCH (follower:User)-[:FOLLOWS]->(user)
                WITH user, count(follower) as follower_count
                ORDER BY follower_count DESC
                LIMIT $limit
                RETURN user.user_id as user_id,
                       user.username as username,
                       follower_count
            """, limit=limit)
            
            return [
                {
                    "user_id": record["user_id"],
                    "username": record["username"],
                    "follower_count": record["follower_count"],
                    "reason": "Popular user"
                }
                for record in result
            ]
    except Exception as e:
        logger.error(f"Error getting popular users: {str(e)}")
        return []


def get_content_recommendations(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get content recommendations based on user's interaction history.
    Uses collaborative filtering: recommends posts liked by users with similar tastes.
    
    Args:
        user_id: User ID to get recommendations for
        limit: Maximum number of posts
        
    Returns:
        List of recommended posts
    """
    try:
        driver = get_driver()
        if not driver:
            return []
        
        # Get posts user has liked
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User {user_id: $user_id})-[r:LIKES]->(liked:Post)
                RETURN liked.post_id as post_id
                LIMIT 50
            """, user_id=user_id)
            
            liked_post_ids = [record["post_id"] for record in result]
        
        if not liked_post_ids:
            # If user hasn't liked anything, return trending posts
            return get_trending_posts(limit, user_id)
        
        # Find users who liked similar posts
        with driver.session() as session:
            result = session.run("""
                MATCH (current:User {user_id: $user_id})-[r1:LIKES]->(post:Post)
                MATCH (similar:User)-[r2:LIKES]->(post)
                WHERE similar.user_id <> $user_id
                WITH similar, count(post) as common_likes
                ORDER BY common_likes DESC
                LIMIT 10
                MATCH (similar)-[:LIKES]->(recommended:Post)
                WHERE NOT (current)-[:LIKES]->(recommended)
                WITH recommended, count(similar) as recommendation_score
                ORDER BY recommendation_score DESC
                LIMIT $limit
                RETURN recommended.post_id as post_id, recommendation_score
            """, user_id=user_id, limit=limit)
            
            recommended_post_ids = [record["post_id"] for record in result]
        
        # Fetch post details from MongoDB
        if not recommended_post_ids:
            return get_trending_posts(limit, user_id)
        
        posts = []
        for post_id in recommended_post_ids:
            post = posts_mongodb_client.get_post(post_id)
            if post:
                posts.append(post)
        
        return posts[:limit]
        
    except Exception as e:
        logger.error(f"Error getting content recommendations: {str(e)}")
        return get_trending_posts(limit, user_id)


def get_hybrid_recommendations(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get hybrid recommendations combining multiple algorithms.
    50% trending, 30% collaborative filtering, 20% content-based
    
    Args:
        user_id: User ID
        limit: Maximum number of posts
        
    Returns:
        List of recommended posts
    """
    try:
        trending = get_trending_posts(int(limit * 0.5), user_id)
        content = get_content_recommendations(user_id, int(limit * 0.3))
        # Add some random diverse posts
        all_posts = posts_mongodb_client.get_all_posts(limit=100, skip=0)
        
        # Combine and deduplicate
        seen_ids = set()
        recommendations = []
        
        # Add trending posts
        for post in trending:
            post_id = post.get("post_id")
            if post_id and post_id not in seen_ids:
                post["recommendation_type"] = "trending"
                recommendations.append(post)
                seen_ids.add(post_id)
        
        # Add content-based recommendations
        for post in content:
            post_id = post.get("post_id")
            if post_id and post_id not in seen_ids:
                post["recommendation_type"] = "content_based"
                recommendations.append(post)
                seen_ids.add(post_id)
        
        # Fill remaining with diverse posts
        remaining = limit - len(recommendations)
        for post in all_posts:
            if remaining <= 0:
                break
            post_id = post.get("post_id")
            if post_id and post_id not in seen_ids:
                post["recommendation_type"] = "diverse"
                recommendations.append(post)
                seen_ids.add(post_id)
                remaining -= 1
        
        return recommendations[:limit]
        
    except Exception as e:
        logger.error(f"Error getting hybrid recommendations: {str(e)}")
        return get_trending_posts(limit, user_id)

