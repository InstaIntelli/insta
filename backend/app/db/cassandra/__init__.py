"""
Cassandra Database Client
Handles connection to Cassandra for time-series data (activity logs, analytics)
"""

from typing import Optional, List, Dict, Any
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Optional Cassandra imports
try:
    from cassandra.cluster import Cluster, Session
    from cassandra.auth import PlainTextAuthProvider
    from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy
    from cassandra.query import SimpleStatement, ConsistencyLevel
    CASSANDRA_AVAILABLE = True
except ImportError:
    CASSANDRA_AVAILABLE = False
    Cluster = None
    Session = None
    logger.warning("Cassandra driver not installed - Cassandra features will be disabled")

class CassandraClient:
    """Cassandra client with connection pooling and retry logic"""
    
    def __init__(self):
        self.cluster: Optional[Cluster] = None
        self.session: Optional[Session] = None
        self.keyspace: str = settings.CASSANDRA_KEYSPACE
        self._initialized = False
    
    def connect(self) -> bool:
        """Connect to Cassandra cluster"""
        if not CASSANDRA_AVAILABLE:
            logger.warning("Cassandra driver not available - cannot connect")
            return False
            
        try:
            if self._initialized and self.session:
                return True
            
            # Parse hosts (can be comma-separated)
            hosts = [h.strip() for h in settings.CASSANDRA_HOSTS.split(',')]
            
            # Configure connection
            contact_points = hosts if hosts else ['localhost']
            port = settings.CASSANDRA_PORT
            
            logger.info(f"Connecting to Cassandra at {contact_points}:{port}")
            
            # Build cluster configuration
            cluster_kwargs = {
                'contact_points': contact_points,
                'port': port,
                'load_balancing_policy': TokenAwarePolicy(DCAwareRoundRobinPolicy()),
                'default_retry_policy': None,  # Use default retry policy
            }
            
            # Add authentication if provided
            if settings.CASSANDRA_USERNAME and settings.CASSANDRA_PASSWORD:
                auth_provider = PlainTextAuthProvider(
                    username=settings.CASSANDRA_USERNAME,
                    password=settings.CASSANDRA_PASSWORD
                )
                cluster_kwargs['auth_provider'] = auth_provider
            
            # Create cluster
            self.cluster = Cluster(**cluster_kwargs)
            self.session = self.cluster.connect()
            
            # Create keyspace if it doesn't exist
            self._create_keyspace()
            
            # Use keyspace
            self.session.set_keyspace(self.keyspace)
            
            # Create tables
            self._create_tables()
            
            self._initialized = True
            logger.info(f"✅ Connected to Cassandra, using keyspace: {self.keyspace}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Cassandra: {str(e)}", exc_info=True)
            return False
    
    def _create_keyspace(self):
        """Create keyspace if it doesn't exist"""
        try:
            keyspace_query = f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH REPLICATION = {{
                'class': 'SimpleStrategy',
                'replication_factor': 1
            }};
            """
            self.session.execute(keyspace_query)
            logger.info(f"Keyspace '{self.keyspace}' ready")
        except Exception as e:
            logger.error(f"Error creating keyspace: {str(e)}")
            raise
    
    def _create_tables(self):
        """Create required tables"""
        try:
            # User Activity Logs Table
            # Partition by user_id, cluster by timestamp (descending for recent first)
            activity_table = """
            CREATE TABLE IF NOT EXISTS user_activities (
                user_id text,
                activity_id timeuuid,
                activity_type text,
                activity_data text,  -- JSON string
                timestamp timestamp,
                ip_address text,
                user_agent text,
                PRIMARY KEY (user_id, activity_id)
            ) WITH CLUSTERING ORDER BY (activity_id DESC);
            """
            
            # Create index on activity_type for filtering
            activity_type_index = """
            CREATE INDEX IF NOT EXISTS ON user_activities (activity_type);
            """
            
            # Analytics Events Table (for aggregated analytics)
            analytics_table = """
            CREATE TABLE IF NOT EXISTS analytics_events (
                event_date date,
                event_id timeuuid,
                event_type text,
                user_id text,
                event_data text,  -- JSON string
                timestamp timestamp,
                PRIMARY KEY ((event_date, event_type), event_id)
            ) WITH CLUSTERING ORDER BY (event_id DESC);
            """
            
            # Execute table creation
            self.session.execute(activity_table)
            self.session.execute(activity_type_index)
            self.session.execute(analytics_table)
            
            logger.info("✅ Cassandra tables created/verified")
            
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}", exc_info=True)
            # Don't raise - tables might already exist
    
    def get_session(self) -> Optional[Session]:
        """Get Cassandra session"""
        if not self._initialized:
            self.connect()
        return self.session
    
    def execute(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a CQL query"""
        if not CASSANDRA_AVAILABLE:
            raise Exception("Cassandra driver not available")
            
        if not self.session:
            if not self.connect():
                raise Exception("Cassandra not connected")
        
        try:
            statement = SimpleStatement(
                query,
                consistency_level=ConsistencyLevel.ONE  # Fast writes for time-series
            )
            if parameters:
                return self.session.execute(statement, parameters)
            else:
                return self.session.execute(statement)
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def close(self):
        """Close Cassandra connection"""
        try:
            if self.cluster:
                self.cluster.shutdown()
                logger.info("Cassandra connection closed")
        except Exception as e:
            logger.error(f"Error closing Cassandra connection: {str(e)}")
    
    def is_connected(self) -> bool:
        """Check if connected to Cassandra"""
        if not CASSANDRA_AVAILABLE:
            return False
        return self._initialized and self.session is not None


# Global instance
cassandra_client = CassandraClient()

def get_cassandra() -> Optional[Session]:
    """Get Cassandra session (dependency injection)"""
    return cassandra_client.get_session()
