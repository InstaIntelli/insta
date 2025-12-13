"""
Application Configuration
Loads environment variables and provides settings
To be implemented by team
"""

from pydantic_settings import BaseSettings
from typing import List

# Placeholder - to be fully implemented
class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App settings
    APP_NAME: str = "InstaIntelli"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = ""
    ALLOWED_ORIGINS: List[str] = []
    
    # Database URLs - to be configured
    POSTGRES_URL: str = ""
    MONGODB_URL: str = ""
    REDIS_URL: str = ""
    
    # Storage
    MINIO_ENDPOINT: str = ""
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET_NAME: str = ""
    
    # Vector DB
    VECTOR_DB_TYPE: str = "chroma"
    CHROMA_HOST: str = ""
    CHROMA_PORT: int = 8000
    
    # LLM
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Placeholder - to be instantiated
# settings = Settings()

