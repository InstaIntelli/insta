"""
Prompt templates for AI operations.

All prompts are designed to be:
- Short and deterministic
- Prevent hallucination
- Return structured output when required
"""

# System prompt for general AI operations
SYSTEM_PROMPT = """You are a helpful AI assistant for InstaIntelli, a social media platform.
Your role is to generate accurate, relevant content based on the provided information.
Always be factual and avoid making up information that isn't present in the input."""


# Caption generation prompt
CAPTION_GENERATION_PROMPT = """Generate a concise, engaging caption for a social media post.

Guidelines:
- Keep it under 150 characters
- Make it natural and engaging
- Do not add hashtags unless explicitly present in the original content
- Do not invent details not present in the input
- If the input is empty or unclear, return a generic but appropriate caption

Input text: {text}
Input image description: {image_description}

Generate only the caption, nothing else:"""


# Metadata extraction prompt for topics
TOPIC_EXTRACTION_PROMPT = """Extract 3-5 main topics or themes from the following content.
Return only a comma-separated list of topics, nothing else.
Each topic should be a single word or short phrase (2-3 words max).

Content: {content}

Topics:"""


# Embedding content preparation prompt
EMBEDDING_CONTENT_PROMPT = """Create a concise semantic summary of this social media post for embedding generation.

Include:
- Main topic or theme
- Key information or message
- Context if available

Post text: {text}
Post caption: {caption}
Image description: {image_description}

Semantic summary:"""


def get_caption_prompt(text: str = "", image_description: str = "") -> str:
    """
    Generate caption generation prompt.
    
    Args:
        text: Post text content
        image_description: Description of the image
        
    Returns:
        Formatted prompt string
    """
    return CAPTION_GENERATION_PROMPT.format(
        text=text or "No text provided",
        image_description=image_description or "No image description available"
    )


def get_topic_extraction_prompt(content: str) -> str:
    """
    Generate topic extraction prompt.
    
    Args:
        content: Combined content to extract topics from
        
    Returns:
        Formatted prompt string
    """
    return TOPIC_EXTRACTION_PROMPT.format(content=content)


def get_embedding_content_prompt(
    text: str = "",
    caption: str = "",
    image_description: str = ""
) -> str:
    """
    Generate embedding content preparation prompt.
    
    Args:
        text: Post text content
        caption: Post caption
        image_description: Description of the image
        
    Returns:
        Formatted prompt string
    """
    return EMBEDDING_CONTENT_PROMPT.format(
        text=text or "No text",
        caption=caption or "No caption",
        image_description=image_description or "No image"
    )

