"""
Neo4j Graph Database Connection
Handles user relationships, likes, comments, and messages
"""

from neo4j import GraphDatabase
from typing import Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Global driver instance
driver: Optional[GraphDatabase.driver] = None


def init_neo4j():
    """Initialize Neo4j connection"""
    global driver
    
    try:
        if not settings.NEO4J_URI:
            logger.warning("Neo4j URI not configured. Social features will be disabled.")
            return
        
        driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        
        # Test connection
        with driver.session() as session:
            session.run("RETURN 1")
        
        logger.info("Neo4j database initialized successfully")
        
        # Create constraints and indexes
        create_constraints()
        
    except Exception as e:
        logger.error(f"Failed to initialize Neo4j: {str(e)}")
        raise


def create_constraints():
    """Create constraints and indexes for better performance"""
    global driver
    
    if not driver:
        return
    
    try:
        with driver.session() as session:
            # Create unique constraint on User nodes
            session.run("""
                CREATE CONSTRAINT user_id_unique IF NOT EXISTS
                FOR (u:User) REQUIRE u.user_id IS UNIQUE
            """)
            
            # Create indexes for better query performance
            session.run("""
                CREATE INDEX user_id_index IF NOT EXISTS
                FOR (u:User) ON (u.user_id)
            """)
            
            # Create index on Post nodes
            session.run("""
                CREATE INDEX post_id_index IF NOT EXISTS
                FOR (p:Post) ON (p.post_id)
            """)
            
            # Create index on Comment nodes
            session.run("""
                CREATE INDEX comment_id_index IF NOT EXISTS
                FOR (c:Comment) ON (c.comment_id)
            """)
            
            logger.info("Neo4j constraints and indexes created")
    except Exception as e:
        logger.warning(f"Could not create Neo4j constraints (may already exist): {str(e)}")


def get_driver():
    """Get Neo4j driver instance"""
    return driver


def close_neo4j():
    """Close Neo4j connection"""
    global driver
    if driver:
        driver.close()
        logger.info("Neo4j connection closed")


