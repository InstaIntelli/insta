"""
Semantic search and RAG-based chat endpoints
Implemented by Alisha (Semantic Search & RAG)
"""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.search import semantic_search, rag_chat, get_similar_posts
import logging

logger = logging.getLogger("search_endpoints")

router = APIRouter(prefix="/search", tags=["Search & RAG"])


# Request/Response Models
class SemanticSearchRequest(BaseModel):
    """Request model for semantic search"""
    query: str = Field(..., description="Search query text")
    user_id: Optional[str] = Field(None, description="Optional user ID to filter results")
    n_results: int = Field(10, ge=1, le=50, description="Number of results to return")
    use_cache: bool = Field(True, description="Whether to use Redis cache")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Show me posts about AI",
                "user_id": "user_123",
                "n_results": 10,
                "use_cache": True
            }
        }


class SemanticSearchResponse(BaseModel):
    """Response model for semantic search"""
    query: str
    results: List[Dict[str, Any]]
    count: int
    error: Optional[str] = None


class RAGChatRequest(BaseModel):
    """Request model for RAG chat"""
    question: str = Field(..., description="User's question")
    user_id: str = Field(..., description="User ID")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for context")
    n_context_posts: int = Field(5, ge=1, le=20, description="Number of relevant posts to retrieve")
    use_cache: bool = Field(True, description="Whether to use Redis cache")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What posts did I upload about AI last week?",
                "user_id": "user_123",
                "conversation_id": "conv_456",
                "n_context_posts": 5,
                "use_cache": True
            }
        }


class RAGChatResponse(BaseModel):
    """Response model for RAG chat"""
    question: str
    answer: str
    referenced_posts: List[Dict[str, Any]]
    count: int
    error: Optional[str] = None


class SimilarPostsResponse(BaseModel):
    """Response model for similar posts"""
    post_id: str
    similar_posts: List[Dict[str, Any]]
    count: int
    error: Optional[str] = None


@router.post(
    "/semantic",
    response_model=SemanticSearchResponse,
    summary="Semantic search for posts",
    description="Search for posts using natural language. Uses vector embeddings for semantic similarity."
)
async def search_semantic(request: SemanticSearchRequest) -> SemanticSearchResponse:
    """
    Perform semantic search on posts.
    
    This endpoint:
    - Converts query to embedding
    - Searches vector database for similar posts
    - Returns ranked results
    - Caches results in Redis
    
    Args:
        request: SemanticSearchRequest with query and options
        
    Returns:
        SemanticSearchResponse with search results
        
    Raises:
        HTTPException: If search fails
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )
        
        logger.info(f"Semantic search request: {request.query}")
        
        result = semantic_search(
            query=request.query,
            user_id=request.user_id,
            n_results=request.n_results,
            use_cache=request.use_cache
        )
        
        return SemanticSearchResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in semantic search endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.post(
    "/chat",
    response_model=RAGChatResponse,
    summary="RAG-based chat about posts",
    description="Ask questions about your posts. Uses RAG (Retrieval Augmented Generation) to provide intelligent answers."
)
async def chat_with_posts(request: RAGChatRequest) -> RAGChatResponse:
    """
    RAG-based chat endpoint.
    
    This endpoint:
    - Retrieves relevant posts based on question
    - Generates context-aware answer using LLM
    - Returns answer with referenced posts
    
    Args:
        request: RAGChatRequest with question and user info
        
    Returns:
        RAGChatResponse with answer and referenced posts
        
    Raises:
        HTTPException: If chat fails
    """
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )
        
        if not request.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is required"
            )
        
        logger.info(f"RAG chat request from user {request.user_id}: {request.question}")
        
        result = rag_chat(
            question=request.question,
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            n_context_posts=request.n_context_posts,
            use_cache=request.use_cache
        )
        
        return RAGChatResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in RAG chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )


@router.get(
    "/similar/{post_id}",
    response_model=SimilarPostsResponse,
    summary="Get similar posts",
    description="Find posts similar to a given post using vector similarity."
)
async def get_similar(
    post_id: str,
    n_results: int = Query(5, ge=1, le=20, description="Number of similar posts to return"),
    user_id: Optional[str] = Query(None, description="Optional user ID to filter results")
) -> SimilarPostsResponse:
    """
    Get similar posts to a given post.
    
    Args:
        post_id: Post ID to find similar posts for
        n_results: Number of similar posts to return
        user_id: Optional user ID to filter results
        
    Returns:
        SimilarPostsResponse with similar posts
        
    Raises:
        HTTPException: If request fails
    """
    try:
        if not post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post ID is required"
            )
        
        logger.info(f"Getting similar posts for: {post_id}")
        
        result = get_similar_posts(
            post_id=post_id,
            n_results=n_results,
            user_id=user_id
        )
        
        return SimilarPostsResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting similar posts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get similar posts: {str(e)}"
        )


@router.get(
    "/health",
    summary="Search service health check",
    description="Check if the search service is running"
)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        Status dictionary
    """
    return {
        "status": "healthy",
        "service": "Search & RAG Service"
    }
