/**
 * Post API service
 * For Sami - Post Upload & Storage
 */

import apiClient from './api'

export const postService = {
  // Upload post
  uploadPost: async (formData) => {
    const response = await apiClient.post('/api/v1/posts/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // Get post
  getPost: async (postId) => {
    const response = await apiClient.get(`/api/v1/posts/${postId}`)
    return response.data
  },

  // Delete post
  deletePost: async (postId) => {
    const response = await apiClient.delete(`/api/v1/posts/${postId}`)
    return response.data
  },

  // Get user posts
  getUserPosts: async (userId) => {
    const response = await apiClient.get(`/api/v1/posts/user/${userId}`)
    return response.data
  },

  // Get feed (fetch all posts for now - will be enhanced later)
  getFeed: async () => {
    // For now, we'll get posts from a user or create a feed endpoint
    // This is a placeholder - in production, this would fetch from a feed endpoint
    try {
      // Try to get feed endpoint first
      const response = await apiClient.get('/api/v1/posts/feed')
      return response.data
    } catch (err) {
      // If feed endpoint doesn't exist, return empty array
      // In production, this would fetch from a different endpoint
      return { posts: [] }
    }
  },

  // Get all posts (for development)
  getAllPosts: async () => {
    // This is a helper method - in production, use getFeed
    return { posts: [] }
  }
}


