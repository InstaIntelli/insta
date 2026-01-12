"""
Script to re-index all existing posts in ChromaDB for semantic search.
Run this after ChromaDB is set up to index all existing posts.
"""

import os
import sys
import asyncio
import logging

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from services.posts.mongodb_client import posts_mongodb_client
from services.ai.background_worker import process_post_background

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def reindex_all_posts():
    """Re-index all posts from MongoDB into ChromaDB."""
    logger.info("Starting to re-index all posts...")
    
    # Get all posts from MongoDB
    posts = posts_mongodb_client.get_all_posts(limit=1000, skip=0)
    
    if not posts:
        logger.warning("No posts found in MongoDB to index.")
        return
    
    logger.info(f"Found {len(posts)} posts to index.")
    
    indexed_count = 0
    failed_count = 0
    
    for post in posts:
        post_id = post.get("post_id")
        user_id = post.get("user_id")
        text = post.get("text")
        image_url = post.get("image_url")
        
        if not post_id or not user_id:
            logger.warning(f"Skipping post with missing post_id or user_id: {post}")
            failed_count += 1
            continue
        
        try:
            logger.info(f"Indexing post {post_id} by user {user_id}...")
            await process_post_background(
                post_id=post_id,
                user_id=user_id,
                text=text,
                image_url=image_url
            )
            indexed_count += 1
            logger.info(f"✓ Successfully indexed post {post_id}")
        except Exception as e:
            logger.error(f"✗ Failed to index post {post_id}: {str(e)}")
            failed_count += 1
    
    logger.info(f"\n✅ Re-indexing complete!")
    logger.info(f"   Successfully indexed: {indexed_count} posts")
    logger.info(f"   Failed: {failed_count} posts")
    logger.info(f"   Total: {len(posts)} posts")


if __name__ == "__main__":
    asyncio.run(reindex_all_posts())

