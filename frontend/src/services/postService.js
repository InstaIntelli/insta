/**
 * Post API service
 * For Sami - Post Upload & Storage
 */

import apiClient from './api'

export const postService = {
  // Upload post
  uploadPost: async (formData) => {
    // Don't set Content-Type - axios will set it automatically with boundary for FormData
    const response = await apiClient.post('/api/v1/posts/upload', formData, {
      headers: {
        // Let axios set Content-Type automatically with boundary for FormData
      },
      timeout: 60000, // 60 seconds for file uploads
      onUploadProgress: (progressEvent) => {
        // Optional: can add progress tracking here
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        console.log(`Upload progress: ${percentCompleted}%`)
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


