"""
Robust Re-indexing Migration Script
Migrates all posts from MongoDB to FAISS/ChromaDB.
Specifically designed to work with Python 3.14 and existing app structure.
"""

import os
import sys
import asyncio
import logging

# Ensure project root is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

# Force environment variables for script if needed
os.environ["DEBUG"] = "True"

from dotenv import load_dotenv
# .env is in the project root, which is one level above backend_root
parent_root = os.path.abspath(os.path.join(project_root, '..'))
load_dotenv(os.path.join(parent_root, ".env"))

# Override for local execution (fallback to local MongoDB without auth if container name found)
if os.getenv("MONGODB_URL"):
    # Try a simple local connection without credentials first
    os.environ["MONGODB_URL"] = "mongodb://localhost:27017/instaintelli"
if os.getenv("REDIS_URL"):
    os.environ["REDIS_URL"] = "redis://localhost:6379/0" # Try default redis port first
if os.getenv("MINIO_ENDPOINT") == "minio":
    os.environ["MINIO_ENDPOINT"] = "localhost"

from app.services.posts.mongodb_client import posts_mongodb_client
from app.services.ai.background_worker import process_post_background
from app.services.ai.vector_store import vector_store

logger = logging.getLogger("reindex_migration")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def migrate_all_posts():
    """Fetch all posts from MongoDB and index them."""
    logger.info("🚀 Starting Search Migration...")
    
    # Check if we have any posts
    posts = posts_mongodb_client.get_all_posts(limit=2000)
    if not posts:
        logger.warning("⚠️ No posts found in MongoDB.")
        return

    logger.info(f"📁 Found {len(posts)} posts to process.")

    success_count = 0
    fail_count = 0

    for i, post in enumerate(posts):
        post_id = post.get("post_id")
        user_id = post.get("user_id")
        text = post.get("text")
        image_url = post.get("image_url")

        if not post_id or not user_id:
            logger.warning(f"⏩ Skipping invalid post at index {i}")
            continue

        try:
            logger.info(f"🔄 [{i+1}/{len(posts)}] Processing post: {post_id}")
            
            # Use the existing background processor which handles:
            # - Caption generation (if missing)
            # - Topic extraction
            # - Embedding generation
            # - Storage in VectorStore (now supports FAISS)
            await process_post_background(
                post_id=post_id,
                user_id=user_id,
                text=text,
                image_url=image_url
            )
            success_count += 1
        except Exception as e:
            logger.error(f"❌ Failed to process post {post_id}: {str(e)}")
            fail_count += 1

    logger.info("-" * 30)
    logger.info(f"✅ Migration Complete!")
    logger.info(f"📊 Successfully indexed: {success_count}")
    logger.info(f"📊 Failed: {fail_count}")
    logger.info(f"📊 Total: {len(posts)}")
    logger.info("-" * 30)

if __name__ == "__main__":
    asyncio.run(migrate_all_posts())
