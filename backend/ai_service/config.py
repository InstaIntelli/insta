"""
Configuration management for AI Processing Service.

Reads environment variables and provides configuration settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # MongoDB Configuration
    mongodb_uri: str
    mongodb_database: str = "instaintelli"
    mongodb_posts_collection: str = "posts"
    
    # ChromaDB Configuration
    chroma_persist_path: str
    chroma_collection_name: str = "post_embeddings"
    
    # API Configuration
    api_title: str = "InstaIntelli AI Processing Service"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


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
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not settings.mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is required")
        if not settings.chroma_persist_path:
            raise ValueError("CHROMA_PERSIST_PATH environment variable is required")
        
        return settings
    except Exception as e:
        raise ValueError(f"Failed to load configuration: {str(e)}")


# Global settings instance
settings = get_settings()

