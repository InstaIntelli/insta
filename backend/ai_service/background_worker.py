"""
Background worker for processing posts asynchronously.
"""

from typing import Optional
from datetime import datetime

from .mongodb_client import mongodb_client
from .caption_generator import caption_generator
from .embedding_generator import embedding_generator
from .vector_store import vector_store
from .schemas import PostMetadata, MongoDBPost
from .utils import logger


async def process_post_background(
    post_id: str,
    user_id: str,
    text: Optional[str] = None,
    image_url: Optional[str] = None
) -> None:
    """
    Background task to process a post:
    1. Fetch post data from MongoDB
    2. Generate caption if missing
    3. Generate embeddings
    4. Store embeddings in ChromaDB
    
    Args:
        post_id: Unique identifier for the post
        user_id: Unique identifier for the user
        text: Optional text content
        image_url: Optional image URL
    """
    try:
        logger.info(f"Starting background processing for post: {post_id}")
        
        # Step 1: Fetch post data from MongoDB
        post_data: Optional[MongoDBPost] = mongodb_client.get_post(post_id)
        
        # Use provided data or fallback to MongoDB data
        final_text = text or (post_data.text if post_data else None)
        final_image_url = image_url or (post_data.image_url if post_data else None)
        existing_caption = post_data.caption if post_data else None
        
        # Step 2: Generate image description if image URL is provided
        image_description: Optional[str] = None
        if final_image_url:
            logger.info(f"Generating image description for post: {post_id}")
            image_description = caption_generator.generate_image_description(final_image_url)
            logger.info("Image description generated")
        
        # Step 3: Generate caption if missing
        caption: Optional[str] = existing_caption
        if not caption:
            logger.info(f"Generating caption for post: {post_id}")
            caption = caption_generator.generate_caption(
                text=final_text,
                image_description=image_description
            )
            
            if caption:
                logger.info("Caption generated")
                # Update MongoDB with generated caption
                mongodb_client.update_post_caption(post_id, caption)
            else:
                logger.warning("Failed to generate caption")
        else:
            logger.info("Using existing caption")
        
        # Step 4: Extract topics
        logger.info(f"Extracting topics for post: {post_id}")
        topics = embedding_generator.extract_topics(
            text=final_text,
            caption=caption,
            image_description=image_description
        )
        logger.info(f"Extracted topics: {topics}")
        
        # Step 5: Prepare semantic summary for embedding
        logger.info(f"Preparing embedding content for post: {post_id}")
        embedding_content = embedding_generator.prepare_embedding_content(
            text=final_text,
            caption=caption,
            image_description=image_description
        )
        
        # Step 6: Generate embedding
        logger.info(f"Generating embedding for post: {post_id}")
        embedding = embedding_generator.generate_embedding(embedding_content)
        
        if not embedding:
            logger.error(f"Failed to generate embedding for post: {post_id}")
            return
        
        logger.info("Embedding generated")
        
        # Step 7: Create metadata
        metadata = PostMetadata(
            post_id=post_id,
            user_id=user_id,
            topics=topics,
            created_at=post_data.created_at if post_data and post_data.created_at else datetime.utcnow(),
            caption=caption,
            text=final_text,
            image_url=final_image_url
        )
        
        # Step 8: Store embedding in ChromaDB
        logger.info(f"Storing embedding in vector database for post: {post_id}")
        success = vector_store.store_post_embedding(
            post_id=post_id,
            embedding=embedding,
            metadata=metadata
        )
        
        if success:
            logger.info(f"Successfully completed processing for post: {post_id}")
        else:
            logger.error(f"Failed to store embedding for post: {post_id}")
            
    except Exception as e:
        logger.error(f"Error in background processing for post {post_id}: {str(e)}")
        raise

