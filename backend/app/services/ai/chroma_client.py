"""
ChromaDB client for vector database operations.
"""

from typing import List, Optional, Dict, Any

# Make chromadb import optional to allow backend to start without it
try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    from chromadb import ClientAPI
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None
    ChromaSettings = None
    ClientAPI = None

from app.services.ai.config import settings
from app.services.ai.utils import logger


class ChromaDBClient:
    """Client for interacting with ChromaDB."""
    
    def __init__(self):
        """Initialize ChromaDB client."""
        self.client: Optional[ClientAPI] = None
        self.collection = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to ChromaDB and get/create collection."""
        if not CHROMADB_AVAILABLE:
            logger.warning("ChromaDB library not available. Vector search features will be disabled.")
            logger.warning("Install chromadb to enable vector search: pip install chromadb")
            return
        
        try:
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_path,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=settings.chroma_collection_name,
                metadata={"description": "Post embeddings for InstaIntelli"}
            )
            
            logger.info(f"Connected to ChromaDB: {settings.chroma_collection_name}")
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {str(e)}")
            logger.warning("Vector search features will be disabled.")
            self.client = None
            self.collection = None
    
    def add_embedding(
        self,
        post_id: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Add or update embedding in ChromaDB.
        
        Args:
            post_id: Unique identifier for the post (used as document ID)
            embedding: Vector embedding
            metadata: Metadata dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if not CHROMADB_AVAILABLE or not self.collection:
            logger.warning(f"Cannot store embedding for post {post_id}: ChromaDB not available")
            return False
        
        try:
            if not self.collection:
                raise RuntimeError("ChromaDB collection not initialized")
            
            # ChromaDB expects documents as list of strings
            # We'll use a placeholder document since we're storing embeddings
            self.collection.upsert(
                ids=[post_id],
                embeddings=[embedding],
                documents=[f"Post {post_id}"],
                metadatas=[metadata]
            )
            
            logger.info(f"Stored embedding for post: {post_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing embedding in ChromaDB: {str(e)}")
            return False
    
    def get_embedding(self, post_id: str) -> Optional[List[float]]:
        """
        Retrieve embedding from ChromaDB.
        
        Args:
            post_id: Unique identifier for the post
            
        Returns:
            Embedding vector if found, None otherwise
        """
        if not CHROMADB_AVAILABLE or not self.collection:
            return None
        
        try:
            if not self.collection:
                raise RuntimeError("ChromaDB collection not initialized")
            
            results = self.collection.get(ids=[post_id])
            
            if results["ids"]:
                embeddings = results["embeddings"]
                if embeddings:
                    return embeddings[0]
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving embedding from ChromaDB: {str(e)}")
            return None
    
    def search_similar(
        self,
        query_embedding: List[float],
        n_results: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar posts using embedding similarity.
        
        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of similar posts with metadata
        """
        if not CHROMADB_AVAILABLE or not self.collection:
            logger.warning("ChromaDB not available. Cannot perform similarity search.")
            return []
        
        try:
            if not self.collection:
                raise RuntimeError("ChromaDB collection not initialized")
            
            where = filter_metadata if filter_metadata else None
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where
            )
            
            # Format results
            similar_posts = []
            if results["ids"] and len(results["ids"]) > 0:
                for i in range(len(results["ids"][0])):
                    similar_posts.append({
                        "post_id": results["ids"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None
                    })
            
            return similar_posts
        except Exception as e:
            logger.error(f"Error searching similar posts: {str(e)}")
            return []


# Global ChromaDB client instance
chroma_client = ChromaDBClient()

