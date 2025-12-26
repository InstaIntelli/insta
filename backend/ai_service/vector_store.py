"""
Vector store operations for managing embeddings in ChromaDB.
"""

from typing import Optional, List
from datetime import datetime

from .chroma_client import chroma_client
from .schemas import PostMetadata
from .utils import logger


class VectorStore:
    """Manages vector storage operations."""
    
    def store_post_embedding(
        self,
        post_id: str,
        embedding: List[float],
        metadata: PostMetadata
    ) -> bool:
        """
        Store post embedding in ChromaDB.
        
        Args:
            post_id: Unique identifier for the post
            embedding: Embedding vector
            metadata: Post metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            metadata_dict = metadata.to_dict()
            
            success = chroma_client.add_embedding(
                post_id=post_id,
                embedding=embedding,
                metadata=metadata_dict
            )
            
            if success:
                logger.info(f"Stored embedding for post {post_id} in vector database")
            
            return success
            
        except Exception as e:
            logger.error(f"Error storing post embedding: {str(e)}")
            return False
    
    def get_post_embedding(self, post_id: str) -> Optional[List[float]]:
        """
        Retrieve post embedding from ChromaDB.
        
        Args:
            post_id: Unique identifier for the post
            
        Returns:
            Embedding vector if found, None otherwise
        """
        try:
            return chroma_client.get_embedding(post_id)
        except Exception as e:
            logger.error(f"Error retrieving post embedding: {str(e)}")
            return None
    
    def search_similar_posts(
        self,
        query_embedding: List[float],
        n_results: int = 10,
        user_id: Optional[str] = None
    ) -> List[dict]:
        """
        Search for similar posts using embedding similarity.
        
        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            user_id: Optional user ID to filter results
            
        Returns:
            List of similar posts with metadata
        """
        try:
            filter_metadata = None
            if user_id:
                filter_metadata = {"user_id": user_id}
            
            return chroma_client.search_similar(
                query_embedding=query_embedding,
                n_results=n_results,
                filter_metadata=filter_metadata
            )
        except Exception as e:
            logger.error(f"Error searching similar posts: {str(e)}")
            return []


# Global vector store instance
vector_store = VectorStore()

