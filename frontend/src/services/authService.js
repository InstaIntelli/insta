/**
 * Authentication API service
 * For Hassan - Auth & Users
 */

import apiClient from './api'

export const authService = {
  // Registration
  register: async (userData) => {
    const response = await apiClient.post('/api/v1/auth/register', userData)
    return response.data
  },

  // Login
  login: async (credentials) => {
    const response = await apiClient.post('/api/v1/auth/login', credentials)
    return response.data
  },

  // Logout
  logout: async () => {
    const response = await apiClient.post('/api/v1/auth/logout')
    return response.data
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await apiClient.get('/api/v1/auth/me')
    return response.data
  },

  // Refresh token
  refreshToken: async (refreshToken) => {
    const response = await apiClient.post('/api/v1/auth/refresh', { refresh_token: refreshToken })
    return response.data
  }
}


