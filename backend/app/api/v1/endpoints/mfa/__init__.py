"""
Multi-Factor Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional

from app.db.postgres import get_db
from app.core.security import get_current_user
from app.services.auth import get_user_by_user_id
from app.services.auth.mfa import (
    setup_mfa,
    enable_mfa,
    disable_mfa,
    verify_totp_code,
    verify_recovery_code,
    regenerate_recovery_codes
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mfa", tags=["Multi-Factor Authentication"])


# Pydantic schemas
class MFASetupResponse(BaseModel):
    secret: str
    qr_code: str
    recovery_codes: List[str]
    message: str


class MFAVerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=6, description="6-digit TOTP code")


class MFAStatusResponse(BaseModel):
    mfa_enabled: bool
    has_recovery_codes: bool


class RecoveryCodesResponse(BaseModel):
    recovery_codes: List[str]
    message: str


@router.post("/setup", response_model=MFASetupResponse)
async def setup_mfa_endpoint(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Setup MFA for the current user
    
    Returns:
        - Secret key (for manual entry)
        - QR code (base64 encoded image)
        - Recovery codes (save these!)
    """
    try:
        user = get_user_by_user_id(db, current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.mfa_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MFA is already enabled. Disable it first to reconfigure."
            )
        
        # Setup MFA
        secret, qr_code, recovery_codes = setup_mfa(user, db)
        
        return MFASetupResponse(
            secret=secret,
            qr_code=qr_code,
            recovery_codes=recovery_codes,
            message="MFA setup initiated. Scan QR code with Google Authenticator and verify with a code to enable."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting up MFA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to setup MFA"
        )


@router.post("/enable")
async def enable_mfa_endpoint(
    request: MFAVerifyRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enable MFA by verifying TOTP code
    
    User must first call /setup to get QR code and secret,
    then verify with a code from their authenticator app.
    """
    try:
        user = get_user_by_user_id(db, current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.mfa_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MFA is already enabled"
            )
        
        if not user.mfa_secret:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MFA not setup. Call /setup first."
            )
        
        # Verify and enable MFA
        if not enable_mfa(user, request.code, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code"
            )
        
        return {
            "message": "MFA enabled successfully",
            "mfa_enabled": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enabling MFA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to enable MFA"
        )


@router.post("/disable")
async def disable_mfa_endpoint(
    request: MFAVerifyRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Disable MFA by verifying TOTP code or recovery code
    """
    try:
        user = get_user_by_user_id(db, current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.mfa_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MFA is not enabled"
            )
        
        # Verify TOTP code or recovery code
        valid = False
        if len(request.code) == 6 and request.code.isdigit():
            # TOTP code
            valid = verify_totp_code(user.mfa_secret, request.code)
        elif '-' in request.code:
            # Recovery code
            valid = verify_recovery_code(user, request.code, db)
        
        if not valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code"
            )
        
        # Disable MFA
        if not disable_mfa(user, db):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to disable MFA"
            )
        
        return {
            "message": "MFA disabled successfully",
            "mfa_enabled": False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disabling MFA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to disable MFA"
        )


@router.get("/status", response_model=MFAStatusResponse)
async def get_mfa_status(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get MFA status for current user
    """
    try:
        user = get_user_by_user_id(db, current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        import json
        has_recovery_codes = False
        if user.mfa_recovery_codes:
            recovery_codes = json.loads(user.mfa_recovery_codes)
            has_recovery_codes = len(recovery_codes) > 0
        
        return MFAStatusResponse(
            mfa_enabled=user.mfa_enabled or False,
            has_recovery_codes=has_recovery_codes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting MFA status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get MFA status"
        )


@router.post("/recovery-codes/regenerate", response_model=RecoveryCodesResponse)
async def regenerate_recovery_codes_endpoint(
    request: MFAVerifyRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Regenerate recovery codes (requires TOTP verification)
    """
    try:
        user = get_user_by_user_id(db, current_user["user_id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.mfa_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MFA is not enabled"
            )
        
        # Verify TOTP code
        if not verify_totp_code(user.mfa_secret, request.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code"
            )
        
        # Regenerate recovery codes
        recovery_codes = regenerate_recovery_codes(user, db)
        
        return RecoveryCodesResponse(
            recovery_codes=recovery_codes,
            message="Recovery codes regenerated successfully. Save these codes in a safe place!"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error regenerating recovery codes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to regenerate recovery codes"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MFA Service"
    }

