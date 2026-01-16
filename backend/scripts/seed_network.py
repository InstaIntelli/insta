"""
Seed script to create a realistic social network
Creates users, follow relationships, posts, and likes
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(backend_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from app.db.postgres.failover import postgres_failover
from app.services.auth import create_user, get_user_by_email
from app.services.social import (
    create_user_node, follow_user, like_post
)
from app.services.posts.mongodb_client import posts_mongodb_client
from app.services.posts.schemas import PostMetadata
from app.services.posts.utils import generate_post_id
from app.db.neo4j import get_driver, init_neo4j
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User data - realistic names, usernames, and email addresses
USERS = [
    {"name": "Alisha", "username": "alisha", "email": "alishashahid77@gmail.com"},
    {"name": "Rabbiya", "username": "rabbiya", "email": "rabbiyakhan23@gmail.com"},
    {"name": "Areeba", "username": "areeba", "email": "areebamalik45@gmail.com"},
    {"name": "Eman", "username": "eman", "email": "emanahmed12@gmail.com"},
    {"name": "Fawad", "username": "fawad", "email": "fawadali89@gmail.com"},
    {"name": "Shoaib", "username": "shoaib", "email": "shoaibhassan56@gmail.com"},
    {"name": "Raza", "username": "raza", "email": "razamalik34@gmail.com"},
    {"name": "Hassan", "username": "hassan", "email": "hassanraza78@gmail.com"},
    {"name": "Sami", "username": "sami", "email": "samiusman91@gmail.com"},
    {"name": "Naeem", "username": "naeem", "email": "naeemkhan67@gmail.com"},
    {"name": "Zalaid", "username": "zalaid", "email": "zalaidahmed45@gmail.com"},
    {"name": "Umer", "username": "umer", "email": "umerfarooq23@gmail.com"},
    {"name": "Hashir", "username": "hashir", "email": "hashirali89@gmail.com"},
    {"name": "Zainab", "username": "zainab", "email": "zainabkhan56@gmail.com"},
    {"name": "Usman", "username": "usman", "email": "usmanmalik34@gmail.com"},
]

# Sample posts with variety
SAMPLE_POSTS = [
    {"text": "Beautiful sunset at the beach! 🌅 #sunset #beach #nature", "topics": "nature, sunset, beach, photography"},
    {"text": "Morning coffee and coding session ☕️💻 #coding #developer #coffee", "topics": "coding, coffee, technology, lifestyle"},
    {"text": "Exploring the city streets 🏙️ #urban #city #explore", "topics": "city, urban, travel, architecture"},
    {"text": "Delicious homemade pasta! 🍝 #food #cooking #italian", "topics": "food, cooking, italian, recipe"},
    {"text": "Mountain hiking adventure! ⛰️ #hiking #mountains #adventure", "topics": "hiking, mountains, adventure, nature"},
    {"text": "Working on a new project! Excited to share it soon 🚀 #project #work #excited", "topics": "work, project, business, productivity"},
    {"text": "Beautiful flowers in the garden 🌸 #flowers #garden #spring", "topics": "flowers, garden, spring, nature"},
    {"text": "Weekend vibes! 🎉 #weekend #fun #friends", "topics": "weekend, fun, friends, lifestyle"},
    {"text": "New book I'm reading 📚 #books #reading #learning", "topics": "books, reading, learning, education"},
    {"text": "Amazing concert last night! 🎵 #music #concert #live", "topics": "music, concert, live, entertainment"},
    {"text": "Just finished a great workout! 💪 #fitness #health #motivation", "topics": "fitness, health, workout, motivation"},
    {"text": "Traveling to new places ✈️ #travel #adventure #wanderlust", "topics": "travel, adventure, wanderlust, exploration"},
    {"text": "Cooking experiment in the kitchen 👨‍🍳 #cooking #food #experiment", "topics": "cooking, food, experiment, kitchen"},
    {"text": "Art gallery visit today 🎨 #art #gallery #culture", "topics": "art, gallery, culture, inspiration"},
    {"text": "Late night coding session 🌙 #coding #developer #night", "topics": "coding, developer, night, programming"},
    {"text": "Beach day with friends 🏖️ #beach #friends #summer", "topics": "beach, friends, summer, fun"},
    {"text": "New recipe I tried today 🍳 #recipe #cooking #food", "topics": "recipe, cooking, food, homemade"},
    {"text": "Photography session 📸 #photography #art #creative", "topics": "photography, art, creative, visual"},
    {"text": "Gaming night with the squad 🎮 #gaming #friends #fun", "topics": "gaming, friends, fun, entertainment"},
    {"text": "Learning something new every day 📖 #learning #growth #education", "topics": "learning, growth, education, self-improvement"},
]

# Follow relationships - creating a realistic network
# Format: (follower, following)
FOLLOW_RELATIONSHIPS = [
    # Alisha follows several people
    ("alisha", "rabbiya"), ("alisha", "areeba"), ("alisha", "hassan"), ("alisha", "raza"),
    # Rabbiya follows
    ("rabbiya", "alisha"), ("rabbiya", "zainab"), ("rabbiya", "eman"), ("rabbiya", "sami"),
    # Areeba follows
    ("areeba", "alisha"), ("areeba", "fawad"), ("areeba", "shoaib"), ("areeba", "naeem"),
    # Eman follows
    ("eman", "rabbiya"), ("eman", "zainab"), ("eman", "usman"), ("eman", "umer"),
    # Fawad follows
    ("fawad", "areeba"), ("fawad", "hassan"), ("fawad", "raza"), ("fawad", "sami"),
    # Shoaib follows
    ("shoaib", "areeba"), ("shoaib", "fawad"), ("shoaib", "naeem"), ("shoaib", "zalaid"),
    # Raza follows
    ("raza", "alisha"), ("raza", "hassan"), ("raza", "fawad"), ("raza", "sami"),
    # Hassan follows
    ("hassan", "alisha"), ("hassan", "raza"), ("hassan", "fawad"), ("hassan", "usman"),
    # Sami follows
    ("sami", "rabbiya"), ("sami", "raza"), ("sami", "hassan"), ("sami", "naeem"),
    # Naeem follows
    ("naeem", "areeba"), ("naeem", "shoaib"), ("naeem", "sami"), ("naeem", "zalaid"),
    # Zalaid follows
    ("zalaid", "shoaib"), ("zalaid", "naeem"), ("zalaid", "umer"), ("zalaid", "hashir"),
    # Umer follows
    ("umer", "eman"), ("umer", "zalaid"), ("umer", "hashir"), ("umer", "usman"),
    # Hashir follows
    ("hashir", "zalaid"), ("hashir", "umer"), ("hashir", "usman"), ("hashir", "zainab"),
    # Zainab follows
    ("zainab", "rabbiya"), ("zainab", "eman"), ("zainab", "hashir"), ("zainab", "usman"),
    # Usman follows
    ("usman", "eman"), ("usman", "umer"), ("usman", "hashir"), ("usman", "zainab"),
]


def seed_users(db):
    """Create users in PostgreSQL and Neo4j"""
    logger.info("Creating users...")
    user_map = {}  # username -> user_id
    
    for user_data in USERS:
        try:
            # Check if user already exists
            existing = get_user_by_email(db, user_data["email"])
            if existing:
                logger.info(f"User {user_data['username']} already exists, skipping...")
                user_map[user_data["username"]] = existing.user_id
                # Create Neo4j node if not exists
                create_user_node(existing.user_id, existing.username)
                continue
            
            # Create user in PostgreSQL
            user = create_user(
                db=db,
                email=user_data["email"],
                username=user_data["username"],
                password="demo123",  # Demo password for all users
                full_name=user_data["name"]
            )
            
            user_map[user_data["username"]] = user.user_id
            
            # Create user node in Neo4j
            create_user_node(user.user_id, user.username)
            
            logger.info(f"✓ Created user: {user_data['name']} (@{user_data['username']})")
            
        except Exception as e:
            logger.error(f"✗ Error creating user {user_data['username']}: {str(e)}")
            continue
    
    logger.info(f"✅ Created {len(user_map)} users")
    return user_map


def seed_follows(user_map):
    """Create follow relationships in Neo4j"""
    logger.info("Creating follow relationships...")
    follow_count = 0
    
    for follower_username, following_username in FOLLOW_RELATIONSHIPS:
        try:
            follower_id = user_map.get(follower_username)
            following_id = user_map.get(following_username)
            
            if not follower_id or not following_id:
                logger.warning(f"User not found: {follower_username} or {following_username}")
                continue
            
            if follow_user(follower_id, following_id):
                follow_count += 1
                logger.debug(f"✓ {follower_username} follows {following_username}")
            else:
                logger.warning(f"✗ Failed: {follower_username} -> {following_username}")
                
        except Exception as e:
            logger.error(f"Error creating follow relationship: {str(e)}")
            continue
    
    logger.info(f"✅ Created {follow_count} follow relationships")


def seed_posts(user_map):
    """Create posts in MongoDB and Neo4j - 2-3 posts per user"""
    logger.info("Creating posts for all users...")
    post_ids = []
    now = datetime.utcnow()
    
    # Get all users
    user_ids = list(user_map.values())
    user_count = len(user_ids)
    
    # Create 3 posts per user
    posts_per_user = 3
    total_posts_needed = user_count * posts_per_user
    
    # Create posts for each user
    post_index = 0
    for user_id in user_ids:
        username = [k for k, v in user_map.items() if v == user_id][0]
        
        # Create 3 posts for this user
        for post_num in range(posts_per_user):
            try:
                # Select a post template (cycle through SAMPLE_POSTS)
                post_data = SAMPLE_POSTS[post_index % len(SAMPLE_POSTS)]
                post_index += 1
                
                # Generate random timestamp (within last 14 days)
                days_ago = random.randint(0, 14)
                hours_ago = random.randint(0, 23)
                created_at = now - timedelta(days=days_ago, hours=hours_ago)
                
                post_id = generate_post_id()
                
                # Use realistic Unsplash images based on post content
                image_ids = [
                    "1506905925346-21bda4d32df4",  # Sunset/beach
                    "1517487881594-2787fef5ebf7",  # Coffee/coding
                    "1449824913935-59a10b8d2000",  # City/urban
                    "1551462147-895e2e2b3a8e",     # Food/pasta
                    "1506905925346-21bda4d32df4",  # Mountains
                    "1460925895917-afdab827c52f",  # Work/project
                    "1490750967868-88aa4486c946",  # Flowers
                    "1511632765486-a01980e01a18",  # Weekend/fun
                    "1544947950-fa07a98d237f",     # Books
                    "1470229722913-7c0e2dbbafd3",  # Music/concert
                    "1571019613454-1cb2f99b2d8b",  # Fitness
                    "1469854523086-cc02fe5d8800",  # Travel
                    "1556911220-bff31c812e09",     # Cooking
                    "1541961017774-22349e4a1262",  # Art
                    "1516321318427-fad04b421e7f",  # Coding night
                    "1507525428034-714724f3985d",  # Beach
                    "1556911220-bff31c812e09",     # Recipe
                    "1502920914264-2d1ef7e0b1c4",  # Photography
                    "1542751371-487b845f8f6e",      # Gaming
                    "1503676260728-1c00da094a0b",  # Learning
                ]
                image_id = image_ids[post_index % len(image_ids)]
                
                # Create post in MongoDB
                metadata = PostMetadata(
                    post_id=post_id,
                    user_id=user_id,
                    text=post_data["text"],
                    image_url=f"https://images.unsplash.com/photo-{image_id}?w=800&h=800&fit=crop",
                    thumbnail_url=f"https://images.unsplash.com/photo-{image_id}?w=400&h=400&fit=crop",
                    created_at=created_at.isoformat(),
                    topics=post_data.get("topics", "")
                )
                
                result = posts_mongodb_client.create_post(metadata)
                
                if result:
                    # Create Post node in Neo4j
                    driver = get_driver()
                    if driver:
                        with driver.session() as session:
                            session.run("""
                                MERGE (user:User {user_id: $user_id})
                                MERGE (post:Post {post_id: $post_id})
                                MERGE (user)-[:CREATED]->(post)
                                SET post.created_at = datetime($created_at)
                            """, user_id=user_id, post_id=post_id, created_at=created_at.isoformat())
                    
                    post_ids.append((post_id, user_id))
                    logger.info(f"✓ Created post {post_id} by @{username}")
                else:
                    logger.warning(f"✗ Failed to create post {post_id}")
                    
            except Exception as e:
                logger.error(f"Error creating post: {str(e)}")
                continue
    
    logger.info(f"✅ Created {len(post_ids)} posts")
    return post_ids


def seed_likes(user_map, post_ids):
    """Create likes on posts"""
    logger.info("Creating likes...")
    like_count = 0
    
    for post_id, post_author_id in post_ids:
        # Get random users to like this post (3-8 likes per post)
        num_likes = random.randint(3, 8)
        likers = random.sample(list(user_map.values()), min(num_likes, len(user_map)))
        
        # Don't let author like their own post (usually)
        likers = [uid for uid in likers if uid != post_author_id]
        
        for liker_id in likers:
            try:
                if like_post(liker_id, post_id):
                    like_count += 1
                    logger.debug(f"✓ User {liker_id} liked post {post_id}")
            except Exception as e:
                logger.error(f"Error creating like: {str(e)}")
                continue
    
    logger.info(f"✅ Created {like_count} likes")


def main():
    """Main seeding function"""
    logger.info("=" * 60)
    logger.info("Starting social network seeding...")
    logger.info("=" * 60)
    
    try:
        # Initialize Neo4j
        logger.info("Initializing Neo4j...")
        try:
            init_neo4j()
            logger.info("✅ Neo4j initialized")
        except Exception as e:
            logger.warning(f"⚠️ Neo4j initialization failed: {str(e)}")
            logger.warning("Continuing without Neo4j (follow relationships and likes will be skipped)")
        
        # Get database session
        db = postgres_failover.get_session()
        
        # 1. Create users
        user_map = seed_users(db)
        
        if not user_map:
            logger.error("No users created. Exiting.")
            return
        
        # 2. Create follow relationships (only if Neo4j is available)
        driver = get_driver()
        if driver:
            seed_follows(user_map)
        else:
            logger.warning("⚠️ Neo4j not available - skipping follow relationships")
        
        # 3. Create posts
        post_ids = seed_posts(user_map)
        
        # 4. Create likes (only if Neo4j is available)
        if post_ids and driver:
            seed_likes(user_map, post_ids)
        elif post_ids:
            logger.warning("⚠️ Neo4j not available - skipping likes")
        
        logger.info("=" * 60)
        logger.info("✅ Social network seeding complete!")
        logger.info("=" * 60)
        logger.info(f"Users: {len(user_map)}")
        logger.info(f"Posts: {len(post_ids)}")
        logger.info("Check Neo4j browser to see the graph network!")
        
    except Exception as e:
        logger.error(f"Error during seeding: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
