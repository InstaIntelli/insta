"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.db.postgres import get_db
from app.services.auth import create_user, authenticate_user, get_user_by_user_id
from app.core.security import create_access_token, get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Pydantic schemas
class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    user_id: str
    email: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    created_at: Optional[str] = None


class MFAVerifyLogin(BaseModel):
    user_id: str
    code: str = Field(..., description="6-digit TOTP code or recovery code")


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        User data and access token
    """
    try:
        # Create user
        user = create_user(
            db=db,
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name
        )
        
        # Generate access token
        access_token = create_access_token(
            data={
                "sub": user.user_id,
                "email": user.email,
                "username": user.username
            }
        )
        
        return {
            "user": user.to_safe_dict(),
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=dict)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user
    
    Args:
        user_data: User login credentials
        db: Database session
        
    Returns:
        User data and access token, or MFA required flag
    """
    try:
        # Authenticate user
        user = authenticate_user(db, user_data.email, user_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if MFA is enabled
        if user.mfa_enabled and user.mfa_secret:
            # Return MFA required flag
            return {
                "mfa_required": True,
                "user_id": user.user_id,
                "email": user.email,
                "message": "MFA verification required"
            }
        
        # Generate access token (no MFA)
        access_token = create_access_token(
            data={
                "sub": user.user_id,
                "email": user.email,
                "username": user.username
            }
        )
        
        return {
            "mfa_required": False,
            "user": user.to_safe_dict(),
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login (for Swagger UI)
    
    Args:
        form_data: OAuth2 form data
        db: Database session
        
    Returns:
        Access token
    """
    try:
        # Authenticate user (username field contains email)
        user = authenticate_user(db, form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate access token
        access_token = create_access_token(
            data={
                "sub": user.user_id,
                "email": user.email,
                "username": user.username
            }
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current user information
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        User information
    """
    try:
        user = get_user_by_user_id(db, current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(**user.to_safe_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )


@router.post("/mfa/verify", response_model=dict)
async def verify_mfa_login(mfa_data: MFAVerifyLogin, db: Session = Depends(get_db)):
    """
    Verify MFA code and complete login
    
    Args:
        mfa_data: User ID and MFA code
        db: Database session
        
    Returns:
        User data and access token
    """
    try:
        from app.services.auth.mfa import verify_totp_code, verify_recovery_code
        
        user = get_user_by_user_id(db, mfa_data.user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.mfa_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MFA is not enabled for this user"
            )
        
        # Verify code (TOTP or recovery code)
        valid = False
        if len(mfa_data.code) == 6 and mfa_data.code.isdigit():
            # TOTP code
            valid = verify_totp_code(user.mfa_secret, mfa_data.code)
        elif '-' in mfa_data.code:
            # Recovery code
            valid = verify_recovery_code(user, mfa_data.code, db)
        
        if not valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid verification code",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate access token
        access_token = create_access_token(
            data={
                "sub": user.user_id,
                "email": user.email,
                "username": user.username
            }
        )
        
        return {
            "user": user.to_safe_dict(),
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"MFA verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MFA verification failed"
        )


@router.post("/logout")
async def logout():
    """
    Logout user (client should delete token)
    
    Returns:
        Success message
    """
    return {"message": "Logged out successfully"}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Authentication Service"
    }
