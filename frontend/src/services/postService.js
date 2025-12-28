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

  // Get feed
  getFeed: async () => {
    const response = await apiClient.get('/api/v1/posts/feed')
    return response.data
  }
}


