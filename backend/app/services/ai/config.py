"""
AI Service Configuration
Uses main app settings from app.core.config
Provides compatibility layer for AI service code
Supports both OpenAI and Grok APIs
"""

from app.core.config import settings as app_settings
from typing import Optional

class AISettings:
    """Compatibility wrapper for AI service settings"""
    
    @property
    def llm_provider(self) -> str:
        """LLM provider: 'openai' or 'grok'"""
        return app_settings.LLM_PROVIDER.lower()
    
    @property
    def api_key(self) -> str:
        """Get API key based on provider"""
        if self.llm_provider == "grok":
            return app_settings.GROK_API_KEY
        return app_settings.OPENAI_API_KEY
    
    @property
    def api_base_url(self) -> str:
        """Get API base URL based on provider"""
        if self.llm_provider == "grok":
            return app_settings.GROK_API_BASE_URL
        return app_settings.OPENAI_API_BASE_URL
    
    @property
    def model(self) -> str:
        """Get model name based on provider"""
        if self.llm_provider == "grok":
            return app_settings.GROK_MODEL
        return app_settings.OPENAI_MODEL
    
    @property
    def embedding_model(self) -> str:
        """Get embedding model (Grok may use OpenAI embeddings)"""
        if self.llm_provider == "grok":
            return app_settings.GROK_EMBEDDING_MODEL
        return app_settings.OPENAI_EMBEDDING_MODEL
    
    # Backward compatibility aliases
    @property
    def openai_api_key(self) -> str:
        return self.api_key
    
    @property
    def openai_model(self) -> str:
        return self.model
    
    @property
    def openai_embedding_model(self) -> str:
        return self.embedding_model
    
    @property
    def mongodb_uri(self) -> str:
        return app_settings.MONGODB_URL
    
    @property
    def mongodb_database(self) -> str:
        return app_settings.MONGODB_DATABASE
    
    @property
    def mongodb_posts_collection(self) -> str:
        return app_settings.MONGODB_POSTS_COLLECTION
    
    @property
    def chroma_persist_path(self) -> str:
        return app_settings.CHROMA_PERSIST_PATH
    
    @property
    def chroma_collection_name(self) -> str:
        return app_settings.CHROMA_COLLECTION_NAME

# Global settings instance (compatible with existing AI service code)
settings = AISettings()

