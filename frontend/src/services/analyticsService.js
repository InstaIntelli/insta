/**
 * Analytics API Service
 */

import apiClient from './api'

export const analyticsService = {
  getUserAnalytics: async () => {
    const response = await apiClient.get('/api/v1/analytics/user')
    return response.data
  },

  getUserAnalyticsById: async (userId) => {
    const response = await apiClient.get(`/api/v1/analytics/user/${userId}`)
    return response.data
  },

  getPlatformAnalytics: async () => {
    const response = await apiClient.get('/api/v1/analytics/platform')
    return response.data
  },

  getTopPosts: async (userId, limit = 5) => {
    const response = await apiClient.get(`/api/v1/analytics/top-posts/${userId}`, {
      params: { limit }
    })
    return response.data
  }
}

