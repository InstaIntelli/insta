/**
 * User API service
 * For Hassan - User Profiles
 */

import apiClient from './api'

export const userService = {
  // Get user profile
  getUser: async (userId) => {
    const response = await apiClient.get(`/api/v1/users/${userId}`)
    return response.data
  },

  // Update user profile
  updateUser: async (userId, userData) => {
    const response = await apiClient.put(`/api/v1/users/${userId}`, userData)
    return response.data
  },

  // Get user followers
  getFollowers: async (userId) => {
    const response = await apiClient.get(`/api/v1/users/${userId}/followers`)
    return response.data
  },

  // Follow user
  followUser: async (userId) => {
    const response = await apiClient.post(`/api/v1/users/${userId}/follow`)
    return response.data
  },

  // Unfollow user
  unfollowUser: async (userId) => {
    const response = await apiClient.delete(`/api/v1/users/${userId}/follow`)
    return response.data
  }
}


