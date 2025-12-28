/**
 * Search API service
 * For Alisha - Search & RAG Chat
 */

import apiClient from './api'

export const searchService = {
  // Semantic search
  semanticSearch: async (query, userId = null, nResults = 10) => {
    const response = await apiClient.post('/api/v1/search/semantic', {
      query,
      user_id: userId,
      n_results: nResults,
      use_cache: true
    })
    return response.data
  },

  // RAG chat
  chatWithPosts: async (question, userId, conversationId = null) => {
    const response = await apiClient.post('/api/v1/search/chat', {
      question,
      user_id: userId,
      conversation_id: conversationId,
      n_context_posts: 5,
      use_cache: true
    })
    return response.data
  },

  // Get similar posts
  getSimilarPosts: async (postId, nResults = 5, userId = null) => {
    const params = { n_results: nResults }
    if (userId) params.user_id = userId
    
    const response = await apiClient.get(`/api/v1/search/similar/${postId}`, { params })
    return response.data
  },

  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/api/v1/search/health')
    return response.data
  }
}


