"""
Script to update post image URLs to use MinIO images
"""

import sys
import os

# Add parent directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(backend_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from app.services.posts.mongodb_client import posts_mongodb_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Available MinIO images
MINIO_IMAGES = [
    "originals/post_sample1.jpg",
    "originals/post_sample2.jpg",
    "originals/post_sample3.jpg",
    "originals/post_sample4.jpg",
    "originals/post_sample5.jpg",
]

def update_post_images():
    """Update post image URLs to use MinIO images"""
    logger.info("Updating post image URLs...")
    
    # Get all posts
    posts = posts_mongodb_client.get_all_posts(limit=100, skip=0)
    
    if not posts:
        logger.warning("No posts found")
        return
    
    updated_count = 0
    
    for i, post in enumerate(posts):
        try:
            post_id = post.get("post_id")
            if not post_id:
                continue
            
            # Select image based on post index
            image_path = MINIO_IMAGES[i % len(MINIO_IMAGES)]
            new_image_url = f"http://localhost:8000/api/v1/posts/images/{image_path}"
            
            # Update in MongoDB
            result = posts_mongodb_client.collection.update_one(
                {"post_id": post_id},
                {"$set": {"image_url": new_image_url}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                logger.info(f"✓ Updated post {post_id} with image {image_path}")
            
        except Exception as e:
            logger.error(f"Error updating post {post.get('post_id')}: {str(e)}")
            continue
    
    logger.info(f"✅ Updated {updated_count} posts with MinIO images")

if __name__ == "__main__":
    update_post_images()
