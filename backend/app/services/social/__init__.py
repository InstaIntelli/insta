"""
Social Graph Service
Handles user relationships, likes, comments, and messages using Neo4j
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from app.db.neo4j import get_driver
import logging

logger = logging.getLogger("social_service")


def create_user_node(user_id: str, username: str):
    """Create a User node in Neo4j"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            session.run("""
                MERGE (u:User {user_id: $user_id})
                SET u.username = $username,
                    u.created_at = datetime()
            """, user_id=user_id, username=username)
        return True
    except Exception as e:
        logger.error(f"Error creating user node: {str(e)}")
        return False


def follow_user(follower_id: str, following_id: str) -> bool:
    """Create FOLLOWS relationship between users"""
    driver = get_driver()
    if not driver:
        return False
    
    if follower_id == following_id:
        return False  # Can't follow yourself
    
    try:
        with driver.session() as session:
            # Create both user nodes if they don't exist
            session.run("""
                MERGE (follower:User {user_id: $follower_id})
                MERGE (following:User {user_id: $following_id})
                MERGE (follower)-[r:FOLLOWS]->(following)
                SET r.created_at = datetime()
            """, follower_id=follower_id, following_id=following_id)
        return True
    except Exception as e:
        logger.error(f"Error following user: {str(e)}")
        return False


def unfollow_user(follower_id: str, following_id: str) -> bool:
    """Remove FOLLOWS relationship"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            session.run("""
                MATCH (follower:User {user_id: $follower_id})-[r:FOLLOWS]->(following:User {user_id: $following_id})
                DELETE r
            """, follower_id=follower_id, following_id=following_id)
        return True
    except Exception as e:
        logger.error(f"Error unfollowing user: {str(e)}")
        return False


def is_following(follower_id: str, following_id: str) -> bool:
    """Check if user is following another user"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (follower:User {user_id: $follower_id})-[r:FOLLOWS]->(following:User {user_id: $following_id})
                RETURN r
            """, follower_id=follower_id, following_id=following_id)
            return result.single() is not None
    except Exception as e:
        logger.error(f"Error checking follow status: {str(e)}")
        return False


def get_followers(user_id: str) -> List[Dict[str, Any]]:
    """Get list of users who follow this user"""
    driver = get_driver()
    if not driver:
        return []
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (follower:User)-[r:FOLLOWS]->(user:User {user_id: $user_id})
                RETURN follower.user_id as user_id, follower.username as username, r.created_at as created_at
                ORDER BY r.created_at DESC
            """, user_id=user_id)
            return [dict(record) for record in result]
    except Exception as e:
        logger.error(f"Error getting followers: {str(e)}")
        return []


def get_following(user_id: str) -> List[Dict[str, Any]]:
    """Get list of users this user is following"""
    driver = get_driver()
    if not driver:
        return []
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User {user_id: $user_id})-[r:FOLLOWS]->(following:User)
                RETURN following.user_id as user_id, following.username as username, r.created_at as created_at
                ORDER BY r.created_at DESC
            """, user_id=user_id)
            return [dict(record) for record in result]
    except Exception as e:
        logger.error(f"Error getting following: {str(e)}")
        return []


def get_follower_count(user_id: str) -> int:
    """Get number of followers"""
    driver = get_driver()
    if not driver:
        return 0
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (follower:User)-[:FOLLOWS]->(user:User {user_id: $user_id})
                RETURN count(follower) as count
            """, user_id=user_id)
            record = result.single()
            return record["count"] if record else 0
    except Exception as e:
        logger.error(f"Error getting follower count: {str(e)}")
        return 0


def get_following_count(user_id: str) -> int:
    """Get number of users being followed"""
    driver = get_driver()
    if not driver:
        return 0
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User {user_id: $user_id})-[r:FOLLOWS]->(following:User)
                RETURN count(following) as count
            """, user_id=user_id)
            record = result.single()
            return record["count"] if record else 0
    except Exception as e:
        logger.error(f"Error getting following count: {str(e)}")
        return 0


def like_post(user_id: str, post_id: str) -> bool:
    """Create LIKES relationship between user and post"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            session.run("""
                MERGE (user:User {user_id: $user_id})
                MERGE (post:Post {post_id: $post_id})
                MERGE (user)-[r:LIKES]->(post)
                SET r.created_at = datetime()
            """, user_id=user_id, post_id=post_id)
        return True
    except Exception as e:
        logger.error(f"Error liking post: {str(e)}")
        return False


def unlike_post(user_id: str, post_id: str) -> bool:
    """Remove LIKES relationship"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            session.run("""
                MATCH (user:User {user_id: $user_id})-[r:LIKES]->(post:Post {post_id: $post_id})
                DELETE r
            """, user_id=user_id, post_id=post_id)
        return True
    except Exception as e:
        logger.error(f"Error unliking post: {str(e)}")
        return False


def is_liked(user_id: str, post_id: str) -> bool:
    """Check if user has liked a post"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User {user_id: $user_id})-[r:LIKES]->(post:Post {post_id: $post_id})
                RETURN r
            """, user_id=user_id, post_id=post_id)
            return result.single() is not None
    except Exception as e:
        logger.error(f"Error checking like status: {str(e)}")
        return False


def get_like_count(post_id: str) -> int:
    """Get number of likes for a post"""
    driver = get_driver()
    if not driver:
        return 0
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User)-[:LIKES]->(post:Post {post_id: $post_id})
                RETURN count(user) as count
            """, post_id=post_id)
            record = result.single()
            return record["count"] if record else 0
    except Exception as e:
        logger.error(f"Error getting like count: {str(e)}")
        return 0


def get_likers(post_id: str) -> List[Dict[str, Any]]:
    """Get list of users who liked a post"""
    driver = get_driver()
    if not driver:
        return []
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User)-[r:LIKES]->(post:Post {post_id: $post_id})
                RETURN user.user_id as user_id, user.username as username, r.created_at as created_at
                ORDER BY r.created_at DESC
            """, post_id=post_id)
            return [dict(record) for record in result]
    except Exception as e:
        logger.error(f"Error getting likers: {str(e)}")
        return []


def create_comment(comment_id: str, user_id: str, post_id: str, text: str, parent_comment_id: Optional[str] = None) -> bool:
    """Create a comment on a post or reply to a comment"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            if parent_comment_id:
                # Reply to comment
                session.run("""
                    MERGE (user:User {user_id: $user_id})
                    MERGE (parent:Comment {comment_id: $parent_comment_id})
                    MERGE (comment:Comment {comment_id: $comment_id})
                    SET comment.text = $text,
                        comment.created_at = datetime(),
                        comment.user_id = $user_id
                    MERGE (user)-[:WROTE]->(comment)
                    MERGE (comment)-[:REPLIES_TO]->(parent)
                """, user_id=user_id, comment_id=comment_id, text=text, parent_comment_id=parent_comment_id)
            else:
                # Comment on post
                session.run("""
                    MERGE (user:User {user_id: $user_id})
                    MERGE (post:Post {post_id: $post_id})
                    MERGE (comment:Comment {comment_id: $comment_id})
                    SET comment.text = $text,
                        comment.created_at = datetime(),
                        comment.user_id = $user_id
                    MERGE (user)-[:WROTE]->(comment)
                    MERGE (comment)-[:ON]->(post)
                """, user_id=user_id, post_id=post_id, comment_id=comment_id, text=text)
        return True
    except Exception as e:
        logger.error(f"Error creating comment: {str(e)}")
        return False


def delete_comment(comment_id: str, user_id: str) -> bool:
    """Delete a comment (only if user owns it)"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User {user_id: $user_id})-[:WROTE]->(comment:Comment {comment_id: $comment_id})
                DETACH DELETE comment
                RETURN comment
            """, user_id=user_id, comment_id=comment_id)
            return result.single() is not None
    except Exception as e:
        logger.error(f"Error deleting comment: {str(e)}")
        return False


def get_comments(post_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get all top-level comments on a post"""
    driver = get_driver()
    if not driver:
        return []
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User)-[:WROTE]->(comment:Comment)-[:ON]->(post:Post {post_id: $post_id})
                WHERE NOT (comment)-[:REPLIES_TO]->(:Comment)
                RETURN comment.comment_id as comment_id,
                       comment.text as text,
                       comment.created_at as created_at,
                       user.user_id as user_id,
                       user.username as username
                ORDER BY comment.created_at DESC
                LIMIT $limit
            """, post_id=post_id, limit=limit)
            return [dict(record) for record in result]
    except Exception as e:
        logger.error(f"Error getting comments: {str(e)}")
        return []


def get_replies(comment_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Get replies to a comment"""
    driver = get_driver()
    if not driver:
        return []
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User)-[:WROTE]->(reply:Comment)-[:REPLIES_TO]->(parent:Comment {comment_id: $comment_id})
                RETURN reply.comment_id as comment_id,
                       reply.text as text,
                       reply.created_at as created_at,
                       user.user_id as user_id,
                       user.username as username
                ORDER BY reply.created_at ASC
                LIMIT $limit
            """, comment_id=comment_id, limit=limit)
            return [dict(record) for record in result]
    except Exception as e:
        logger.error(f"Error getting replies: {str(e)}")
        return []


def get_comment_count(post_id: str) -> int:
    """Get total number of comments (including replies) on a post"""
    driver = get_driver()
    if not driver:
        return 0
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (comment:Comment)-[:ON]->(post:Post {post_id: $post_id})
                RETURN count(comment) as count
            """, post_id=post_id)
            record = result.single()
            return record["count"] if record else 0
    except Exception as e:
        logger.error(f"Error getting comment count: {str(e)}")
        return 0


def send_message(sender_id: str, recipient_id: str, text: str, message_id: str) -> bool:
    """Send a message from one user to another"""
    driver = get_driver()
    if not driver:
        return False
    
    if sender_id == recipient_id:
        return False  # Can't message yourself
    
    try:
        with driver.session() as session:
            session.run("""
                MERGE (sender:User {user_id: $sender_id})
                MERGE (recipient:User {user_id: $recipient_id})
                MERGE (message:Message {message_id: $message_id})
                SET message.text = $text,
                    message.created_at = datetime(),
                    message.sender_id = $sender_id,
                    message.recipient_id = $recipient_id,
                    message.read = false
                MERGE (sender)-[:SENT]->(message)
                MERGE (message)-[:TO]->(recipient)
            """, sender_id=sender_id, recipient_id=recipient_id, text=text, message_id=message_id)
        return True
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return False


def get_conversations(user_id: str) -> List[Dict[str, Any]]:
    """Get all conversations for a user"""
    driver = get_driver()
    if not driver:
        return []
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (user:User {user_id: $user_id})<-[:TO]-(message:Message)-[:SENT]->(other:User)
                WHERE message.sender_id = other.user_id
                WITH other, message, user
                ORDER BY message.created_at DESC
                WITH other, collect(message)[0] as last_message
                RETURN other.user_id as user_id,
                       other.username as username,
                       last_message.message_id as last_message_id,
                       last_message.text as last_message_text,
                       last_message.created_at as last_message_at,
                       last_message.read as read
                ORDER BY last_message.created_at DESC
            """, user_id=user_id)
            return [dict(record) for record in result]
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        return []


def get_messages(user_id: str, other_user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get messages between two users"""
    driver = get_driver()
    if not driver:
        return []
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (sender:User)-[:SENT]->(message:Message)-[:TO]->(recipient:User)
                WHERE (sender.user_id = $user_id AND recipient.user_id = $other_user_id)
                   OR (sender.user_id = $other_user_id AND recipient.user_id = $user_id)
                RETURN message.message_id as message_id,
                       message.text as text,
                       message.created_at as created_at,
                       message.read as read,
                       sender.user_id as sender_id,
                       sender.username as sender_username
                ORDER BY message.created_at ASC
                LIMIT $limit
            """, user_id=user_id, other_user_id=other_user_id, limit=limit)
            return [dict(record) for record in result]
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        return []


def mark_messages_read(user_id: str, other_user_id: str) -> bool:
    """Mark messages as read"""
    driver = get_driver()
    if not driver:
        return False
    
    try:
        with driver.session() as session:
            session.run("""
                MATCH (sender:User {user_id: $other_user_id})-[:SENT]->(message:Message)-[:TO]->(recipient:User {user_id: $user_id})
                WHERE message.read = false
                SET message.read = true
            """, user_id=user_id, other_user_id=other_user_id)
        return True
    except Exception as e:
        logger.error(f"Error marking messages as read: {str(e)}")
        return False


def get_unread_count(user_id: str) -> int:
    """Get count of unread messages"""
    driver = get_driver()
    if not driver:
        return 0
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (message:Message)-[:TO]->(user:User {user_id: $user_id})
                WHERE message.read = false
                RETURN count(message) as count
            """, user_id=user_id)
            record = result.single()
            return record["count"] if record else 0
    except Exception as e:
        logger.error(f"Error getting unread count: {str(e)}")
        return 0


