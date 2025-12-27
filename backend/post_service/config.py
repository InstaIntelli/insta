"""
Configuration management for Post Upload + Storage Service.

Reads environment variables and provides configuration settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # MongoDB Configuration
    mongodb_uri: str
    mongodb_db_name: str = "instaintelli"
    mongodb_posts_collection: str = "posts"
    
    # MinIO Configuration
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    minio_use_ssl: bool = False
    minio_region: str = "us-east-1"
    
    # Upload Configuration
    max_upload_size_mb: int = 10
    allowed_image_types: list = ["image/jpeg", "image/jpg", "image/png"]
    thumbnail_size: tuple = (300, 300)
    
    # API Configuration
    api_title: str = "InstaIntelli Post Upload + Storage Service"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Convert max upload size from MB to bytes."""
        return self.max_upload_size_mb * 1024 * 1024


def get_settings() -> Settings:
    """
    Get application settings.
    
    Raises:
        ValueError: If required environment variables are missing.
    
    Returns:
        Settings: Application configuration object.
    """
    try:
        settings = Settings()
        
        # Validate required settings
        if not settings.mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is required")
        if not settings.minio_endpoint:
            raise ValueError("MINIO_ENDPOINT environment variable is required")
        if not settings.minio_access_key:
            raise ValueError("MINIO_ACCESS_KEY environment variable is required")
        if not settings.minio_secret_key:
            raise ValueError("MINIO_SECRET_KEY environment variable is required")
        if not settings.minio_bucket_name:
            raise ValueError("MINIO_BUCKET_NAME environment variable is required")
        
        return settings
    except Exception as e:
        raise ValueError(f"Failed to load configuration: {str(e)}")


# Global settings instance
settings = get_settings()

