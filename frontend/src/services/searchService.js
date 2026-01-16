/**
 * Search API service
 * For Alisha - Search & RAG Chat
 */

import apiClient from './api'

export const searchService = {
  // Flexible search (Semantic or Keyword)
  search: async (query, userId = null, searchType = 'semantic', isGlobal = false, nResults = 10) => {
    const response = await apiClient.post('/api/v1/search/semantic', {
      query,
      user_id: isGlobal ? null : userId,
      search_type: searchType,
      n_results: nResults,
      use_cache: true
    })
    return response.data
  },

  // Legacy alias for backward compatibility
  semanticSearch: async (query, userId = null, nResults = 10) => {
    return searchService.search(query, userId, 'semantic', false, nResults)
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


