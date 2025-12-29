"""
Authentication service layer
"""

import uuid
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.auth import User
from app.core.security import verify_password, get_password_hash, create_access_token
import logging

logger = logging.getLogger(__name__)


def generate_user_id() -> str:
    """Generate a unique user ID"""
    return f"user_{uuid.uuid4().hex[:12]}"


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        User object or None
    """
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        logger.error(f"Error getting user by email: {str(e)}")
        return None


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get user by username
    
    Args:
        db: Database session
        username: Username
        
    Returns:
        User object or None
    """
    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as e:
        logger.error(f"Error getting user by username: {str(e)}")
        return None


def get_user_by_user_id(db: Session, user_id: str) -> Optional[User]:
    """
    Get user by user_id
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User object or None
    """
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    except Exception as e:
        logger.error(f"Error getting user by user_id: {str(e)}")
        return None


def create_user(
    db: Session,
    email: str,
    username: str,
    password: str,
    full_name: Optional[str] = None
) -> User:
    """
    Create a new user
    
    Args:
        db: Database session
        email: User email
        username: Username
        password: Plain text password
        full_name: Optional full name
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If user already exists
    """
    try:
        # Check if user already exists
        existing_user = get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_username = get_user_by_username(db, username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        user_id = generate_user_id()
        hashed_password = get_password_hash(password)
        
        db_user = User(
            user_id=user_id,
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User created successfully: {email}")
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
        
    Returns:
        User object if authenticated, None otherwise
    """
    try:
        user = get_user_by_email(db, email)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
        
    except Exception as e:
        logger.error(f"Error authenticating user: {str(e)}")
        return None


def update_user_profile(
    db: Session,
    user_id: str,
    full_name: Optional[str] = None,
    bio: Optional[str] = None,
    profile_image_url: Optional[str] = None
) -> Optional[User]:
    """
    Update user profile
    
    Args:
        db: Database session
        user_id: User ID
        full_name: Optional full name
        bio: Optional bio
        profile_image_url: Optional profile image URL
        
    Returns:
        Updated user object or None
    """
    try:
        user = get_user_by_user_id(db, user_id)
        if not user:
            return None
        
        if full_name is not None:
            user.full_name = full_name
        if bio is not None:
            user.bio = bio
        if profile_image_url is not None:
            user.profile_image_url = profile_image_url
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"User profile updated: {user_id}")
        return user
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user profile: {str(e)}")
        return None
