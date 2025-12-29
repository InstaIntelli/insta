"""
Authentication and user models (SQLAlchemy)
"""

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime

from app.db.postgres import Base


class User(Base):
    """User model for authentication and profile"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), unique=True, index=True, nullable=False)  # UUID format
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # MFA fields
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(32), nullable=True)  # TOTP secret key
    mfa_recovery_codes = Column(Text, nullable=True)  # JSON array of recovery codes
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_image_url": self.profile_image_url,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_safe_dict(self):
        """Convert model to dictionary without sensitive data"""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_image_url": self.profile_image_url,
            "mfa_enabled": self.mfa_enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
