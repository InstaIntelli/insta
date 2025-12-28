/**
 * AI API service
 * For Raza - AI Processing
 */

import apiClient from './api'

export const aiService = {
  // Process post with AI
  processPost: async (postData) => {
    const response = await apiClient.post('/api/v1/ai/process_post', postData)
    return response.data
  },

  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/api/v1/ai/health')
    return response.data
  }
}


