"""
Update user emails to realistic Gmail addresses
"""

import sys
import os

# Add parent directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(backend_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from app.db.postgres.failover import postgres_failover
from app.services.auth import get_user_by_username
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Updated email mappings
EMAIL_UPDATES = {
    "alisha": "alishashahid77@gmail.com",
    "rabbiya": "rabbiyakhan23@gmail.com",
    "areeba": "areebamalik45@gmail.com",
    "eman": "emanahmed12@gmail.com",
    "fawad": "fawadali89@gmail.com",
    "shoaib": "shoaibhassan56@gmail.com",
    "raza": "razamalik34@gmail.com",
    "hassan": "hassanraza78@gmail.com",
    "sami": "samiusman91@gmail.com",
    "naeem": "naeemkhan67@gmail.com",
    "zalaid": "zalaidahmed45@gmail.com",
    "umer": "umerfarooq23@gmail.com",
    "hashir": "hashirali89@gmail.com",
    "zainab": "zainabkhan56@gmail.com",
    "usman": "usmanmalik34@gmail.com",
}


def update_emails():
    """Update user emails to realistic Gmail addresses"""
    logger.info("Updating user emails...")
    
    db = postgres_failover.get_session()
    updated_count = 0
    
    for username, new_email in EMAIL_UPDATES.items():
        try:
            user = get_user_by_username(db, username)
            if user:
                # Update email directly in database
                db.execute(
                    text("UPDATE users SET email = :email WHERE user_id = :user_id"),
                    {"email": new_email, "user_id": user.user_id}
                )
                db.commit()
                updated_count += 1
                logger.info(f"✓ Updated {username}: {new_email}")
            else:
                logger.warning(f"User {username} not found")
        except Exception as e:
            logger.error(f"Error updating {username}: {str(e)}")
            db.rollback()
            continue
    
    logger.info(f"✅ Updated {updated_count} user emails")
    return updated_count


if __name__ == "__main__":
    update_emails()
