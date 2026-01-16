"""
Security utilities for authentication and authorization
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.postgres import get_db

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# JWT settings
SECRET_KEY = settings.SECRET_KEY or "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash (using SHA256 - no length limit)
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password (format: salt:hash)
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        # Split salt and hash
        parts = hashed_password.split(':')
        if len(parts) != 2:
            return False
        salt, stored_hash = parts
        
        # Hash the provided password with the same salt
        password_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
        
        return password_hash == stored_hash
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using SHA256 (no length limit)
    
    Args:
        password: Plain text password (any length)
        
    Returns:
        Hashed password (format: salt:hash)
    """
    # Generate a random salt
    salt = secrets.token_hex(16)
    # Hash password + salt
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    # Return salt:hash format
    return f"{salt}:{password_hash}"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and verify JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[dict]:
    """
    Get current user from token (optional - returns None if no token)
    
    Args:
        token: JWT token from request
        db: Database session
        
    Returns:
        User data or None
    """
    if not token:
        return None
    
    payload = decode_token(token)
    if not payload:
        return None
    
    user_id: str = payload.get("sub")
    if user_id is None:
        return None
    
    # Return user info from token
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "username": payload.get("username")
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get current user from token (required)
    
    Args:
        token: JWT token from request
        db: Database session
        
    Returns:
        User data
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    payload = decode_token(token)
    if not payload:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Return user info from token
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "username": payload.get("username")
    }
