"""
Embedding generation using OpenAI API.
"""

from typing import List, Optional
from openai import OpenAI

from .config import settings
from .prompts import SYSTEM_PROMPT, get_embedding_content_prompt, get_topic_extraction_prompt
from .utils import logger, parse_topics


class EmbeddingGenerator:
    """Generates embeddings for posts using OpenAI."""
    
    def __init__(self):
        """Initialize OpenAI-compatible client (supports OpenAI and Grok)."""
        # Grok API is OpenAI-compatible, so we can use the same client
        import httpx
        self.client = OpenAI(
            api_key=settings.api_key,
            base_url=settings.api_base_url,
            timeout=httpx.Timeout(30.0, connect=10.0)  # 30s total, 10s connect timeout
        )
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding vector for text.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            Embedding vector or None if generation fails
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding generation")
                return None
            
            # Check if API key is configured
            if not settings.api_key:
                logger.error("OpenAI API key not configured. Please set OPENAI_API_KEY in environment variables.")
                return None
            
            logger.debug(f"Generating embedding for text (length: {len(text)})")
            response = self.client.embeddings.create(
                model=settings.embedding_model,
                input=text,
                timeout=30.0  # Explicit timeout in seconds
            )
            
            embedding = response.data[0].embedding
            logger.info("Embedding generated successfully")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def prepare_embedding_content(
        self,
        text: Optional[str] = None,
        caption: Optional[str] = None,
        image_description: Optional[str] = None
    ) -> str:
        """
        Prepare semantic summary for embedding generation.
        
        Args:
            text: Post text content
            caption: Post caption
            image_description: Description of the image
            
        Returns:
            Semantic summary string
        """
        try:
            prompt = get_embedding_content_prompt(
                text=text or "",
                caption=caption or "",
                image_description=image_description or ""
            )
            
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info("Semantic summary prepared for embedding")
            return summary
            
        except Exception as e:
            logger.error(f"Error preparing embedding content: {str(e)}")
            # Fallback to simple concatenation
            parts = []
            if text:
                parts.append(text)
            if caption:
                parts.append(caption)
            if image_description:
                parts.append(image_description)
            return " ".join(parts) if parts else "No content available"
    
    def extract_topics(
        self,
        text: Optional[str] = None,
        caption: Optional[str] = None,
        image_description: Optional[str] = None
    ) -> List[str]:
        """
        Extract topics from post content.
        
        Args:
            text: Post text content
            caption: Post caption
            image_description: Description of the image
            
        Returns:
            List of extracted topics
        """
        try:
            # Combine all content
            content_parts = []
            if text:
                content_parts.append(text)
            if caption:
                content_parts.append(caption)
            if image_description:
                content_parts.append(image_description)
            
            combined_content = " ".join(content_parts)
            
            if not combined_content.strip():
                return []
            
            prompt = get_topic_extraction_prompt(combined_content)
            
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=100
            )
            
            topics_string = response.choices[0].message.content.strip()
            topics = parse_topics(topics_string)
            
            logger.info(f"Extracted {len(topics)} topics")
            return topics
            
        except Exception as e:
            logger.error(f"Error extracting topics: {str(e)}")
            return []


# Global embedding generator instance
embedding_generator = EmbeddingGenerator()

