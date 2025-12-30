"""
Social Features API Endpoints
Follow/Unfollow, Likes, Comments, Messages
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

from app.api.dependencies import get_current_user
from app.services.social import (
    create_user_node, follow_user, unfollow_user, is_following,
    get_followers, get_following, get_follower_count, get_following_count,
    like_post, unlike_post, is_liked, get_like_count, get_likers,
    create_comment, delete_comment, get_comments, get_replies, get_comment_count,
    send_message, get_conversations, get_messages, mark_messages_read, get_unread_count
)

router = APIRouter()


# ==================== Follow/Unfollow ====================

class FollowRequest(BaseModel):
    user_id: str


@router.post("/follow")
async def follow_user_endpoint(
    request: FollowRequest,
    current_user: dict = Depends(get_current_user)
):
    """Follow a user"""
    follower_id = current_user["user_id"]
    following_id = request.user_id
    
    if follower_id == following_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot follow yourself"
        )
    
    success = follow_user(follower_id, following_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to follow user"
        )
    
    return {"message": "User followed successfully", "following_id": following_id}


@router.post("/unfollow")
async def unfollow_user_endpoint(
    request: FollowRequest,
    current_user: dict = Depends(get_current_user)
):
    """Unfollow a user"""
    follower_id = current_user["user_id"]
    following_id = request.user_id
    
    success = unfollow_user(follower_id, following_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unfollow user"
        )
    
    return {"message": "User unfollowed successfully", "following_id": following_id}


@router.get("/followers/{user_id}")
async def get_followers_endpoint(user_id: str):
    """Get list of followers for a user"""
    followers = get_followers(user_id)
    return {"followers": followers, "count": len(followers)}


@router.get("/following/{user_id}")
async def get_following_endpoint(user_id: str):
    """Get list of users a user is following"""
    following = get_following(user_id)
    return {"following": following, "count": len(following)}


@router.get("/follow-status/{user_id}")
async def get_follow_status(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Check if current user is following another user"""
    is_following_user = is_following(current_user["user_id"], user_id)
    return {"is_following": is_following_user}


@router.get("/stats/{user_id}")
async def get_user_stats(user_id: str):
    """Get follower and following counts for a user"""
    return {
        "follower_count": get_follower_count(user_id),
        "following_count": get_following_count(user_id)
    }


# ==================== Likes ====================

class LikeRequest(BaseModel):
    post_id: str


@router.post("/like")
async def like_post_endpoint(
    request: LikeRequest,
    current_user: dict = Depends(get_current_user)
):
    """Like a post"""
    success = like_post(current_user["user_id"], request.post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to like post"
        )
    
    return {"message": "Post liked successfully", "post_id": request.post_id}


@router.post("/unlike")
async def unlike_post_endpoint(
    request: LikeRequest,
    current_user: dict = Depends(get_current_user)
):
    """Unlike a post"""
    success = unlike_post(current_user["user_id"], request.post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unlike post"
        )
    
    return {"message": "Post unliked successfully", "post_id": request.post_id}


@router.get("/like-status/{post_id}")
async def get_like_status(
    post_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Check if current user has liked a post"""
    liked = is_liked(current_user["user_id"], post_id)
    return {"liked": liked}


@router.get("/likes/{post_id}")
async def get_post_likes(post_id: str):
    """Get likes for a post"""
    likers = get_likers(post_id)
    count = get_like_count(post_id)
    return {"likers": likers, "count": count}


# ==================== Comments ====================

class CommentRequest(BaseModel):
    post_id: str
    text: str
    parent_comment_id: Optional[str] = None


class CommentResponse(BaseModel):
    comment_id: str
    text: str
    user_id: str
    username: str
    created_at: str
    replies: List["CommentResponse"] = []


CommentResponse.model_rebuild()


@router.post("/comment")
async def create_comment_endpoint(
    request: CommentRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a comment on a post or reply to a comment"""
    comment_id = f"comment_{uuid.uuid4().hex[:12]}"
    
    success = create_comment(
        comment_id=comment_id,
        user_id=current_user["user_id"],
        post_id=request.post_id,
        text=request.text,
        parent_comment_id=request.parent_comment_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create comment"
        )
    
    return {
        "message": "Comment created successfully",
        "comment_id": comment_id
    }


@router.delete("/comment/{comment_id}")
async def delete_comment_endpoint(
    comment_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a comment"""
    success = delete_comment(comment_id, current_user["user_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found or you don't have permission"
        )
    
    return {"message": "Comment deleted successfully"}


@router.get("/comments/{post_id}")
async def get_post_comments(post_id: str):
    """Get all comments for a post"""
    comments = get_comments(post_id)
    
    # Get replies for each comment
    result = []
    for comment in comments:
        replies = get_replies(comment["comment_id"])
        comment["replies"] = replies
        result.append(comment)
    
    return {
        "comments": result,
        "count": get_comment_count(post_id)
    }


# ==================== Messages ====================

class MessageRequest(BaseModel):
    recipient_id: str
    text: str


class MessageResponse(BaseModel):
    message_id: str
    text: str
    sender_id: str
    sender_username: str
    created_at: str
    read: bool


@router.post("/message")
async def send_message_endpoint(
    request: MessageRequest,
    current_user: dict = Depends(get_current_user)
):
    """Send a message to another user"""
    message_id = f"msg_{uuid.uuid4().hex[:12]}"
    
    success = send_message(
        sender_id=current_user["user_id"],
        recipient_id=request.recipient_id,
        text=request.text,
        message_id=message_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
        )
    
    return {
        "message": "Message sent successfully",
        "message_id": message_id
    }


@router.get("/conversations")
async def get_conversations_endpoint(
    current_user: dict = Depends(get_current_user)
):
    """Get all conversations for current user"""
    conversations = get_conversations(current_user["user_id"])
    return {"conversations": conversations}


@router.get("/messages/{user_id}")
async def get_messages_endpoint(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get messages between current user and another user"""
    messages = get_messages(current_user["user_id"], user_id)
    
    # Mark messages as read
    mark_messages_read(current_user["user_id"], user_id)
    
    return {"messages": messages}


@router.post("/messages/{user_id}/read")
async def mark_messages_read_endpoint(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark messages from a user as read"""
    success = mark_messages_read(current_user["user_id"], user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark messages as read"
        )
    
    return {"message": "Messages marked as read"}


@router.get("/unread-count")
async def get_unread_count_endpoint(
    current_user: dict = Depends(get_current_user)
):
    """Get count of unread messages"""
    count = get_unread_count(current_user["user_id"])
    return {"unread_count": count}

