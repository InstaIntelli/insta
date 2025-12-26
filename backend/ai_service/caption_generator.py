"""
Caption generation using OpenAI API.
"""

from typing import Optional
from openai import OpenAI

from .config import settings
from .prompts import SYSTEM_PROMPT, get_caption_prompt
from .utils import logger


class CaptionGenerator:
    """Generates captions for posts using OpenAI."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def generate_caption(
        self,
        text: Optional[str] = None,
        image_description: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a caption for a post.
        
        Args:
            text: Post text content
            image_description: Description of the image (if available)
            
        Returns:
            Generated caption or None if generation fails
        """
        try:
            prompt = get_caption_prompt(
                text=text or "",
                image_description=image_description or ""
            )
            
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            caption = response.choices[0].message.content.strip()
            
            if caption:
                logger.info("Caption generated successfully")
                return caption
            else:
                logger.warning("Generated caption is empty")
                return None
                
        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}")
            return None
    
    def generate_image_description(self, image_url: Optional[str]) -> Optional[str]:
        """
        Generate description for an image using vision model.
        
        Args:
            image_url: URL of the image
            
        Returns:
            Image description or None if generation fails
        """
        if not image_url:
            return None
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this image in one sentence. Focus on the main subject and key details."
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                max_tokens=100
            )
            
            description = response.choices[0].message.content.strip()
            logger.info("Image description generated successfully")
            return description
            
        except Exception as e:
            logger.error(f"Error generating image description: {str(e)}")
            return None


# Global caption generator instance
caption_generator = CaptionGenerator()

