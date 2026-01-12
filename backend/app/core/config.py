"""
Application Configuration
Loads environment variables and provides settings
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional, Union

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App settings
    APP_NAME: str = "InstaIntelli"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = ""
    ALLOWED_ORIGINS: Union[str, List[str]] = ""  # Can be string or list
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse comma-separated origins string into list, or return list as-is"""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            if not v or v.strip() == "":
                return []
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return []
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get ALLOWED_ORIGINS as a list"""
        if isinstance(self.ALLOWED_ORIGINS, list):
            return self.ALLOWED_ORIGINS
        if isinstance(self.ALLOWED_ORIGINS, str):
            if not self.ALLOWED_ORIGINS or self.ALLOWED_ORIGINS.strip() == "":
                return []
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
        return []
    
    # Database URLs
    POSTGRES_URL: str = ""
    
    # Cloud PostgreSQL (Supabase) - Primary
    SUPABASE_DB_URL: str = ""
    SUPABASE_PROJECT_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    
    # MongoDB
    MONGODB_URL: str = ""
    MONGODB_DATABASE: str = "instaintelli"
    MONGODB_POSTS_COLLECTION: str = "posts"
    
    # Cloud MongoDB (Atlas) - Primary
    MONGODB_ATLAS_URL: str = ""
    MONGODB_ATLAS_DATABASE: str = "instaintelli"
    
    # Redis
    REDIS_URL: str = ""
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    
    # Cloud Redis (Upstash) - Primary
    UPSTASH_REDIS_URL: str = ""
    UPSTASH_REDIS_REST_URL: str = ""
    UPSTASH_REDIS_REST_TOKEN: str = ""
    
    # Storage
    MINIO_ENDPOINT: str = ""
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET_NAME: str = ""
    
    # Vector DB (ChromaDB)
    VECTOR_DB_TYPE: str = "chroma"
    CHROMA_HOST: str = ""
    CHROMA_PORT: int = 8000
    CHROMA_PERSIST_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "post_embeddings"
    
    # Graph DB (Neo4j - Social Connections)
    NEO4J_URI: str = ""
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""
    
    # LLM Provider (openai or grok)
    LLM_PROVIDER: str = "openai"  # Options: "openai" or "grok"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_API_BASE_URL: str = "https://api.openai.com/v1"
    
    # Grok (xAI) Configuration
    GROK_API_KEY: str = ""
    GROK_MODEL: str = "grok-beta"
    GROK_EMBEDDING_MODEL: str = "text-embedding-3-small"  # Grok may use OpenAI embeddings
    GROK_API_BASE_URL: str = "https://api.x.ai/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

