"""
Multi-Factor Authentication (MFA) service
Implements TOTP with Google Authenticator support
"""

import pyotp
import qrcode
import io
import base64
import secrets
import json
from typing import Tuple, List, Optional
from sqlalchemy.orm import Session
import logging

from app.models.auth import User

logger = logging.getLogger(__name__)


def generate_secret_key() -> str:
    """
    Generate a random secret key for TOTP
    
    Returns:
        32-character base32 encoded secret key
    """
    return pyotp.random_base32()


def generate_recovery_codes(count: int = 10) -> List[str]:
    """
    Generate recovery codes for account recovery
    
    Args:
        count: Number of recovery codes to generate
        
    Returns:
        List of recovery codes
    """
    recovery_codes = []
    for _ in range(count):
        # Generate 8-character alphanumeric code
        code = ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(8))
        # Format as XXXX-XXXX for readability
        formatted_code = f"{code[:4]}-{code[4:]}"
        recovery_codes.append(formatted_code)
    
    return recovery_codes


def generate_qr_code(secret: str, email: str, issuer: str = "InstaIntelli") -> str:
    """
    Generate QR code for Google Authenticator
    
    Args:
        secret: TOTP secret key
        email: User's email
        issuer: Application name
        
    Returns:
        Base64 encoded QR code image
    """
    try:
        # Create provisioning URI for Google Authenticator
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=email,
            issuer_name=issuer
        )
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
        
    except Exception as e:
        logger.error(f"Error generating QR code: {str(e)}")
        raise


def verify_totp_code(secret: str, code: str) -> bool:
    """
    Verify TOTP code
    
    Args:
        secret: TOTP secret key
        code: 6-digit TOTP code
        
    Returns:
        True if code is valid, False otherwise
    """
    try:
        # Clean the code - remove spaces and ensure it's 6 digits
        clean_code = code.replace(' ', '').replace('-', '').strip()
        if len(clean_code) != 6 or not clean_code.isdigit():
            logger.warning(f"Invalid code format: {code} (cleaned: {clean_code})")
            return False
        
        totp = pyotp.TOTP(secret)
        # Allow 2 time steps before and after for clock drift (60 seconds each side)
        # This gives more tolerance for time sync issues
        result = totp.verify(clean_code, valid_window=2)
        
        if not result:
            # Debug: Try to see what the current code should be
            current_code = totp.now()
            logger.warning(f"TOTP verification failed. Code provided: {clean_code}, Current code: {current_code}, Secret length: {len(secret)}")
        else:
            logger.info(f"TOTP verification successful for code: {clean_code}")
        
        return result
    except Exception as e:
        logger.error(f"Error verifying TOTP code: {str(e)}")
        return False


def verify_recovery_code(user: User, code: str, db: Session) -> bool:
    """
    Verify and consume a recovery code
    
    Args:
        user: User object
        code: Recovery code to verify
        db: Database session
        
    Returns:
        True if code is valid and consumed, False otherwise
    """
    try:
        if not user.mfa_recovery_codes:
            return False
        
        # Parse recovery codes
        recovery_codes = json.loads(user.mfa_recovery_codes)
        
        # Check if code exists
        if code not in recovery_codes:
            return False
        
        # Remove used code
        recovery_codes.remove(code)
        user.mfa_recovery_codes = json.dumps(recovery_codes)
        
        db.commit()
        
        logger.info(f"Recovery code used for user: {user.user_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error verifying recovery code: {str(e)}")
        db.rollback()
        return False


def setup_mfa(user: User, db: Session) -> Tuple[str, str, List[str]]:
    """
    Setup MFA for a user
    
    Args:
        user: User object
        db: Database session
        
    Returns:
        Tuple of (secret_key, qr_code_base64, recovery_codes)
    """
    try:
        # Generate secret key
        secret = generate_secret_key()
        
        # Generate recovery codes
        recovery_codes = generate_recovery_codes()
        
        # Generate QR code
        qr_code = generate_qr_code(secret, user.email)
        
        # Store in database (not enabled yet until verified)
        user.mfa_secret = secret
        user.mfa_recovery_codes = json.dumps(recovery_codes)
        
        db.commit()
        
        logger.info(f"MFA setup initiated for user: {user.user_id}")
        
        return secret, qr_code, recovery_codes
        
    except Exception as e:
        logger.error(f"Error setting up MFA: {str(e)}")
        db.rollback()
        raise


def enable_mfa(user: User, code: str, db: Session) -> bool:
    """
    Enable MFA after verifying TOTP code
    
    Args:
        user: User object
        code: TOTP code to verify
        db: Database session
        
    Returns:
        True if MFA enabled successfully, False otherwise
    """
    try:
        if not user.mfa_secret:
            return False
        
        # Verify TOTP code
        if not verify_totp_code(user.mfa_secret, code):
            return False
        
        # Enable MFA
        user.mfa_enabled = True
        db.commit()
        
        logger.info(f"MFA enabled for user: {user.user_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error enabling MFA: {str(e)}")
        db.rollback()
        return False


def disable_mfa(user: User, db: Session) -> bool:
    """
    Disable MFA for a user
    
    Args:
        user: User object
        db: Database session
        
    Returns:
        True if MFA disabled successfully, False otherwise
    """
    try:
        user.mfa_enabled = False
        user.mfa_secret = None
        user.mfa_recovery_codes = None
        
        db.commit()
        
        logger.info(f"MFA disabled for user: {user.user_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error disabling MFA: {str(e)}")
        db.rollback()
        return False


def regenerate_recovery_codes(user: User, db: Session) -> List[str]:
    """
    Regenerate recovery codes for a user
    
    Args:
        user: User object
        db: Database session
        
    Returns:
        List of new recovery codes
    """
    try:
        # Generate new recovery codes
        recovery_codes = generate_recovery_codes()
        
        # Store in database
        user.mfa_recovery_codes = json.dumps(recovery_codes)
        db.commit()
        
        logger.info(f"Recovery codes regenerated for user: {user.user_id}")
        
        return recovery_codes
        
    except Exception as e:
        logger.error(f"Error regenerating recovery codes: {str(e)}")
        db.rollback()
        raise


