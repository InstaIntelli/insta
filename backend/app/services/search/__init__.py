"""
Search and RAG service layer
Implemented by Alisha (Semantic Search & RAG)
"""

from typing import List, Dict, Optional, Any
from app.services.ai.vector_store import vector_store
from app.services.ai.embedding_generator import EmbeddingGenerator
from app.db.redis import cache_get, cache_set, cache_key_search, cache_key_chat
from app.core.config import settings
from openai import OpenAI
import logging

logger = logging.getLogger("search_service")

# Initialize embedding generator
embedding_generator = EmbeddingGenerator()

# Initialize OpenAI client for RAG
def get_llm_client():
    """Get LLM client (OpenAI or Grok compatible)"""
    provider = getattr(settings, 'LLM_PROVIDER', 'openai').lower()
    
    if provider == 'grok':
        api_key = getattr(settings, 'GROK_API_KEY', '')
        base_url = getattr(settings, 'GROK_API_BASE_URL', 'https://api.x.ai/v1')
    else:
        api_key = settings.OPENAI_API_KEY
        base_url = getattr(settings, 'OPENAI_API_BASE_URL', 'https://api.openai.com/v1')
    
    return OpenAI(api_key=api_key, base_url=base_url)


def semantic_search(
    query: str,
    user_id: Optional[str] = None,
    n_results: int = 10,
    use_cache: bool = True
) -> Dict[str, Any]:
    """
    Perform semantic search using vector database.
    
    Args:
        query: Search query text
        user_id: Optional user ID to filter results
        n_results: Number of results to return
        use_cache: Whether to use Redis cache
        
    Returns:
        Dictionary with search results
    """
    try:
        # Check cache first
        if use_cache:
            cache_key = cache_key_search(query, user_id)
            cached_result = cache_get(cache_key)
            if cached_result:
                logger.info(f"Returning cached search results for: {query}")
                return cached_result
        
        # Generate embedding for query
        logger.info(f"Generating embedding for query: {query}")
        query_embedding = embedding_generator.generate_embedding(query)
        
        if not query_embedding:
            return {
                "query": query,
                "results": [],
                "count": 0,
                "error": "Failed to generate embedding"
            }
        
        # Search vector database
        logger.info(f"Searching vector database for: {query}")
        similar_posts = vector_store.search_similar_posts(
            query_embedding=query_embedding,
            n_results=n_results,
            user_id=user_id
        )
        
        # Format results
        results = []
        for post in similar_posts:
            results.append({
                "post_id": post.get("post_id"),
                "metadata": post.get("metadata", {}),
                "similarity_score": 1 - post.get("distance", 1.0) if post.get("distance") else None
            })
        
        response = {
            "query": query,
            "results": results,
            "count": len(results)
        }
        
        # Cache results (1 hour)
        if use_cache:
            cache_set(cache_key, response, expire_seconds=3600)
        
        return response
        
    except Exception as e:
        logger.error(f"Error in semantic search: {str(e)}")
        return {
            "query": query,
            "results": [],
            "count": 0,
            "error": str(e)
        }


def rag_chat(
    question: str,
    user_id: str,
    conversation_id: Optional[str] = None,
    n_context_posts: int = 5,
    use_cache: bool = True
) -> Dict[str, Any]:
    """
    RAG-based chat: Retrieve relevant posts and generate answer.
    
    Args:
        question: User's question
        user_id: User ID
        conversation_id: Optional conversation ID for context
        n_context_posts: Number of relevant posts to retrieve
        use_cache: Whether to use Redis cache
        
    Returns:
        Dictionary with answer and referenced posts
    """
    try:
        # Check cache for similar questions
        if use_cache:
            cache_key = cache_key_chat(user_id, conversation_id)
            # Note: We cache the conversation history, not the answer itself
            # as answers should be fresh
        
        # Step 1: Generate embedding for question
        logger.info(f"Generating embedding for question: {question}")
        question_embedding = embedding_generator.generate_embedding(question)
        
        if not question_embedding:
            return {
                "question": question,
                "answer": "I'm sorry, I couldn't process your question. Please try again.",
                "referenced_posts": [],
                "error": "Failed to generate embedding"
            }
        
        # Step 2: Retrieve relevant posts from vector database
        logger.info(f"Retrieving relevant posts for user: {user_id}")
        relevant_posts = vector_store.search_similar_posts(
            query_embedding=question_embedding,
            n_results=n_context_posts,
            user_id=user_id
        )
        
        if not relevant_posts:
            return {
                "question": question,
                "answer": "I couldn't find any relevant posts to answer your question. Try uploading some posts first!",
                "referenced_posts": []
            }
        
        # Step 3: Build context from retrieved posts
        context_parts = []
        for i, post in enumerate(relevant_posts, 1):
            metadata = post.get("metadata", {})
            caption = metadata.get("caption", "")
            text = metadata.get("text", "")
            topics = metadata.get("topics", "")
            
            post_context = f"Post {i}:\n"
            if caption:
                post_context += f"Caption: {caption}\n"
            if text:
                post_context += f"Text: {text}\n"
            if topics:
                post_context += f"Topics: {topics}\n"
            
            context_parts.append(post_context)
        
        context = "\n\n".join(context_parts)
        
        # Step 4: Generate answer using RAG
        logger.info("Generating RAG answer")
        llm_client = get_llm_client()
        
        # Get model name
        provider = getattr(settings, 'LLM_PROVIDER', 'openai').lower()
        model = getattr(settings, 'GROK_MODEL', 'grok-beta') if provider == 'grok' else settings.OPENAI_MODEL
        
        system_prompt = """You are a helpful assistant for InstaIntelli, a social media platform. 
You help users find and understand their posts. Based on the user's question and the relevant posts provided, 
give a helpful and accurate answer. Reference specific posts when relevant."""

        user_prompt = f"""Based on the following posts from the user's account, answer their question.

User's Question: {question}

Relevant Posts:
{context}

Please provide a helpful answer based on these posts. If the question can't be answered from these posts, say so."""

        response = llm_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        # Step 5: Format referenced posts
        referenced_posts = []
        for post in relevant_posts:
            referenced_posts.append({
                "post_id": post.get("post_id"),
                "metadata": post.get("metadata", {}),
                "relevance_score": 1 - post.get("distance", 1.0) if post.get("distance") else None
            })
        
        result = {
            "question": question,
            "answer": answer,
            "referenced_posts": referenced_posts,
            "count": len(referenced_posts)
        }
        
        # Cache conversation (optional - cache the question-answer pair)
        if use_cache and conversation_id:
            cache_key = f"chat_history:{user_id}:{conversation_id}"
            # Store in conversation history (implement if needed)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in RAG chat: {str(e)}")
        return {
            "question": question,
            "answer": "I'm sorry, I encountered an error processing your question. Please try again.",
            "referenced_posts": [],
            "error": str(e)
        }


def get_similar_posts(
    post_id: str,
    n_results: int = 5,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get similar posts to a given post.
    
    Args:
        post_id: Post ID to find similar posts for
        n_results: Number of similar posts to return
        user_id: Optional user ID to filter results
        
    Returns:
        Dictionary with similar posts
    """
    try:
        # Get embedding for the post
        post_embedding = vector_store.get_post_embedding(post_id)
        
        if not post_embedding:
            return {
                "post_id": post_id,
                "similar_posts": [],
                "count": 0,
                "error": "Post embedding not found"
            }
        
        # Search for similar posts
        similar_posts = vector_store.search_similar_posts(
            query_embedding=post_embedding,
            n_results=n_results + 1,  # +1 because the post itself will be included
            user_id=user_id
        )
        
        # Filter out the post itself
        filtered_posts = [
            post for post in similar_posts 
            if post.get("post_id") != post_id
        ][:n_results]
        
        results = []
        for post in filtered_posts:
            results.append({
                "post_id": post.get("post_id"),
                "metadata": post.get("metadata", {}),
                "similarity_score": 1 - post.get("distance", 1.0) if post.get("distance") else None
            })
        
        return {
            "post_id": post_id,
            "similar_posts": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error getting similar posts: {str(e)}")
        return {
            "post_id": post_id,
            "similar_posts": [],
            "count": 0,
            "error": str(e)
        }
