"""
Supabase Auth Service for Google OAuth
"""

from typing import Optional, Dict, Any
from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class SupabaseAuthService:
    """Service for handling Supabase authentication, including Google OAuth"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client"""
        # Note: We don't actually need the client for OAuth URL generation
        # We can construct the URL manually, so we'll skip client initialization
        # to avoid version compatibility issues
        if settings.SUPABASE_PROJECT_URL and settings.SUPABASE_ANON_KEY:
            logger.info("✅ Supabase credentials configured (using manual URL construction)")
            # Don't create client to avoid httpx version conflicts
            self.client = None  # We'll use manual URL construction instead
        else:
            logger.warning("⚠️ Supabase credentials not configured")
            self.client = None
    
    def get_google_oauth_url(self, redirect_to: str) -> Optional[str]:
        """
        Get Google OAuth URL for authentication
        
        Args:
            redirect_to: URL to redirect after OAuth
            
        Returns:
            OAuth URL or None if client not initialized
        """
        if not settings.SUPABASE_PROJECT_URL:
            logger.error("SUPABASE_PROJECT_URL not configured")
            return None
        
        try:
            # Construct OAuth URL manually (Supabase format)
            # Format: {project_url}/auth/v1/authorize?provider=google&redirect_to={redirect_to}
            from urllib.parse import urlencode
            base_url = settings.SUPABASE_PROJECT_URL.rstrip('/')
            params = {
                "provider": "google",
                "redirect_to": redirect_to
            }
            oauth_url = f"{base_url}/auth/v1/authorize?{urlencode(params)}"
            logger.info(f"Generated OAuth URL: {oauth_url[:80]}...")
            return oauth_url
            
        except Exception as e:
            logger.error(f"Error generating Google OAuth URL: {str(e)}", exc_info=True)
            return None
    
    def get_user_from_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from Supabase access token
        
        Args:
            access_token: Supabase access token
            
        Returns:
            User data dictionary or None
        """
        if not self.client:
            return None
        
        try:
            # Set the session with the access token
            self.client.auth.set_session(access_token=access_token)
            
            # Get current user
            user = self.client.auth.get_user(access_token)
            
            if user and user.user:
                return {
                    "id": user.user.id,
                    "email": user.user.email,
                    "full_name": user.user.user_metadata.get("full_name") or user.user.user_metadata.get("name"),
                    "avatar_url": user.user.user_metadata.get("avatar_url"),
                    "provider": "google" if "google" in str(user.user.app_metadata.get("provider", "")).lower() else "email"
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user from token: {str(e)}")
            return None
    
    def verify_oauth_callback(self, code: str, redirect_to: str) -> Optional[Dict[str, Any]]:
        """
        Verify OAuth callback and exchange code for session
        
        Args:
            code: OAuth authorization code
            redirect_to: Redirect URL used in OAuth flow
            
        Returns:
            Session data with access_token and user info, or None
        """
        if not self.client:
            return None
        
        try:
            # Exchange code for session using Supabase
            # The code is exchanged via the frontend, but we can verify the token
            # For backend verification, we'll use the service key to get user info
            import httpx
            base_url = settings.SUPABASE_PROJECT_URL.rstrip('/')
            
            # Exchange code for session
            exchange_response = httpx.post(
                f"{base_url}/auth/v1/token?grant_type=authorization_code&code={code}&redirect_to={redirect_to}",
                headers={
                    "apikey": settings.SUPABASE_ANON_KEY,
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            
            if exchange_response.status_code == 200:
                session_data = exchange_response.json()
                access_token = session_data.get("access_token")
                
                # Get user info
                user_response = httpx.get(
                    f"{base_url}/auth/v1/user",
                    headers={
                        "apikey": settings.SUPABASE_ANON_KEY,
                        "Authorization": f"Bearer {access_token}"
                    }
                )
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    return {
                        "access_token": access_token,
                        "refresh_token": session_data.get("refresh_token"),
                        "user": {
                            "id": user_data.get("id"),
                            "email": user_data.get("email"),
                            "full_name": user_data.get("user_metadata", {}).get("full_name") or user_data.get("user_metadata", {}).get("name"),
                            "avatar_url": user_data.get("user_metadata", {}).get("avatar_url"),
                            "provider": "google"
                        }
                    }
            return None
        except Exception as e:
            logger.error(f"Error verifying OAuth callback: {str(e)}")
            return None
    
    def is_configured(self) -> bool:
        """Check if Supabase is properly configured"""
        # We don't need the client to be initialized, just the credentials
        return (
            settings.SUPABASE_PROJECT_URL and
            settings.SUPABASE_ANON_KEY
        )


# Global instance
supabase_auth = SupabaseAuthService()
