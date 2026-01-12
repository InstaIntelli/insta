/**
 * Recommendation API Service
 */

import apiClient from './api'

export const recommendationService = {
  getTrending: async (limit = 20) => {
    const response = await apiClient.get('/api/v1/recommendations/trending', {
      params: { limit }
    })
    return response.data
  },

  getUserRecommendations: async (limit = 10) => {
    const response = await apiClient.get('/api/v1/recommendations/users', {
      params: { limit }
    })
    return response.data
  },

  getContentRecommendations: async (limit = 20) => {
    const response = await apiClient.get('/api/v1/recommendations/content', {
      params: { limit }
    })
    return response.data
  },

  getHybridRecommendations: async (limit = 20) => {
    const response = await apiClient.get('/api/v1/recommendations/hybrid', {
      params: { limit }
    })
    return response.data
  },

  getPopularUsers: async (limit = 10) => {
    const response = await apiClient.get('/api/v1/recommendations/popular-users', {
      params: { limit }
    })
    return response.data
  }
}

