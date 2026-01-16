"""
Seed script to add fake posts for testing
Run this to populate the feed with sample posts like Instagram does for new users
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.posts.mongodb_client import posts_mongodb_client
from app.services.posts.schemas import PostMetadata
from app.services.posts.utils import generate_post_id
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample posts data - using Unsplash placeholder images
SAMPLE_POSTS = [
    {
        "text": "Beautiful sunset at the beach! 🌅 #sunset #beach #nature",
        "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
        "user_id": "demo_user_1",
        "topics": "nature, sunset, beach, photography"
    },
    {
        "text": "Morning coffee and coding session ☕️💻 #coding #developer #coffee",
        "image_url": "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=400&h=400&fit=crop",
        "user_id": "demo_user_2",
        "topics": "coding, coffee, technology, lifestyle"
    },
    {
        "text": "Exploring the city streets 🏙️ #urban #city #explore",
        "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=400&fit=crop",
        "user_id": "demo_user_3",
        "topics": "city, urban, travel, architecture"
    },
    {
        "text": "Delicious homemade pasta! 🍝 #food #cooking #italian",
        "image_url": "https://images.unsplash.com/photo-1551462147-895e2e0b3a8e?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1551462147-895e2e0b3a8e?w=400&h=400&fit=crop",
        "user_id": "demo_user_4",
        "topics": "food, cooking, italian, recipe"
    },
    {
        "text": "Mountain hiking adventure! ⛰️ #hiking #mountains #adventure",
        "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
        "user_id": "demo_user_5",
        "topics": "hiking, mountains, adventure, nature"
    },
    {
        "text": "Working on a new project! Excited to share it soon 🚀 #project #work #excited",
        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=400&fit=crop",
        "user_id": "demo_user_6",
        "topics": "work, project, business, productivity"
    },
    {
        "text": "Beautiful flowers in the garden 🌸 #flowers #garden #spring",
        "image_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=400&fit=crop",
        "user_id": "demo_user_7",
        "topics": "flowers, garden, spring, nature"
    },
    {
        "text": "Weekend vibes! 🎉 #weekend #fun #friends",
        "image_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=400&h=400&fit=crop",
        "user_id": "demo_user_8",
        "topics": "weekend, fun, friends, lifestyle"
    },
    {
        "text": "New book I'm reading 📚 #books #reading #learning",
        "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop",
        "user_id": "demo_user_9",
        "topics": "books, reading, learning, education"
    },
    {
        "text": "Amazing concert last night! 🎵 #music #concert #live",
        "image_url": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800&h=800&fit=crop",
        "thumbnail_url": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400&h=400&fit=crop",
        "user_id": "demo_user_10",
        "topics": "music, concert, live, entertainment"
    }
]


def seed_posts():
    """Seed the database with sample posts"""
    logger.info("Starting to seed posts...")
    
    try:
        # Check if posts already exist
        existing_posts = posts_mongodb_client.get_all_posts(limit=1)
        if existing_posts:
            logger.info(f"Found {len(existing_posts)} existing posts. Skipping seed.")
            return
        
        # Generate posts with random timestamps (within last 7 days)
        now = datetime.utcnow()
        seeded_count = 0
        
        for post_data in SAMPLE_POSTS:
            # Generate random timestamp within last 7 days
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            created_at = now - timedelta(days=days_ago, hours=hours_ago)
            
            post_id = generate_post_id()
            
            metadata = PostMetadata(
                post_id=post_id,
                user_id=post_data["user_id"],
                text=post_data["text"],
                image_url=post_data["image_url"],
                thumbnail_url=post_data["thumbnail_url"],
                created_at=created_at.isoformat(),
                topics=post_data.get("topics", "")
            )
            
            # Insert into MongoDB
            result = posts_mongodb_client.create_post(metadata)
            
            if result:
                seeded_count += 1
                logger.info(f"✓ Seeded post {post_id} by {post_data['user_id']}")
            else:
                logger.warning(f"✗ Failed to seed post {post_id}")
        
        logger.info(f"\n✅ Successfully seeded {seeded_count} posts!")
        logger.info("Your feed should now show sample posts!")
        
    except Exception as e:
        logger.error(f"Error seeding posts: {str(e)}")
        raise


if __name__ == "__main__":
    seed_posts()

