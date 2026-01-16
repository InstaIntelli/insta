"""
FAISS client for vector database operations.
Fallback for when ChromaDB is not available (e.g., Python 3.14).
"""

import os
import faiss
import numpy as np
import pickle
from typing import List, Optional, Dict, Any
from app.services.ai.config import settings
from app.services.ai.utils import logger

class FAISSClient:
    """Client for interacting with FAISS for vector search."""
    
    def __init__(self):
        """Initialize FAISS client."""
        self.index = None
        self.post_ids = []  # To map FAISS index to post_ids
        self.metadatas = []  # To store metadata
        self.index_path = os.path.join(settings.chroma_persist_path, "faiss_index.bin")
        self.meta_path = os.path.join(settings.chroma_persist_path, "faiss_metadata.pkl")
        self.dimension = 1536  # text-embedding-3-small dimension
        self._load_index()

    def _load_index(self):
        """Load index from disk or create a new one."""
        try:
            if not os.path.exists(settings.chroma_persist_path):
                os.makedirs(settings.chroma_persist_path)

            if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
                self.index = faiss.read_index(self.index_path)
                with open(self.meta_path, 'rb') as f:
                    data = pickle.load(f)
                    self.post_ids = data['post_ids']
                    self.metadatas = data['metadatas']
                logger.info(f"Loaded FAISS index with {len(self.post_ids)} items")
            else:
                # FlatL2 index for simple similarity search
                self.index = faiss.IndexFlatL2(self.dimension)
                logger.info("Created new FAISS index")
        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            self.index = faiss.IndexFlatL2(self.dimension)

    def _save_index(self):
        """Persist index and metadata to disk."""
        try:
            faiss.write_index(self.index, self.index_path)
            with open(self.meta_path, 'wb') as f:
                pickle.dump({
                    'post_ids': self.post_ids,
                    'metadatas': self.metadatas
                }, f)
            logger.info("Saved FAISS index to disk")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")

    def add_embedding(self, post_id: str, embedding: List[float], metadata: Dict[str, Any]) -> bool:
        """Add a single embedding to the index."""
        try:
            # Check if post already exists (simple version: find and update would require rebuilding)
            # For now, we'll just check if it's already there and skip or append
            if post_id in self.post_ids:
                # Update existing (FAISS doesn't support easy updates, so we'll just skip for now
                # In a real app, we'd remove and re-add or rebuild)
                logger.info(f"Post {post_id} already in FAISS, skipping")
                return True

            emb_np = np.array([embedding]).astype('float32')
            self.index.add(emb_np)
            self.post_ids.append(post_id)
            self.metadatas.append(metadata)
            self._save_index()
            return True
        except Exception as e:
            logger.error(f"Error adding to FAISS: {str(e)}")
            return False

    def get_embedding(self, post_id: str) -> Optional[List[float]]:
        """Retrieve embedding (FAISS doesn't store them easily, but we can manage)"""
        # FAISS IndexFlat doesn't allow random access by ID easily
        # We would need to store embeddings separately in the pickle for this
        return None

    def search_similar(self, query_embedding: List[float], n_results: int = 10, filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar embeddings."""
        if self.index is None or len(self.post_ids) == 0:
            return []

        try:
            emb_np = np.array([query_embedding]).astype('float32')
            distances, indices = self.index.search(emb_np, n_results * 2) # Search more to allow filtering

            results = []
            for d, idx in zip(distances[0], indices[0]):
                if idx == -1 or idx >= len(self.post_ids):
                    continue
                
                post_id = self.post_ids[idx]
                meta = self.metadatas[idx]

                # Apply metadata filter (e.g., user_id)
                if filter_metadata:
                    match = True
                    for k, v in filter_metadata.items():
                        if meta.get(k) != v:
                            match = False
                            break
                    if not match:
                        continue

                results.append({
                    "post_id": post_id,
                    "metadata": meta,
                    "distance": float(d)
                })
                
                if len(results) >= n_results:
                    break
            
            return results
        except Exception as e:
            logger.error(f"Error searching FAISS: {str(e)}")
            return []

# Global FAISS client instance
faiss_client = FAISSClient()
