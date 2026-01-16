/**
 * Authentication API service
 */

import apiClient from './api'

export const authService = {
  // Register new user
  register: async (userData) => {
    try {
      const response = await apiClient.post('/api/v1/auth/register', userData)
      
      // Store token and user data
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      
      return response.data
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      const response = await apiClient.post('/api/v1/auth/login', credentials)
      
      // Store token and user data
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      
      return response.data
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  },

  // Logout user
  logout: async () => {
    try {
      await apiClient.post('/api/v1/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Always clear local storage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
    
    return { message: 'Logged out successfully' }
  },

  // Get current user
  getCurrentUser: async () => {
    try {
      const response = await apiClient.get('/api/v1/auth/me')
      return response.data
    } catch (error) {
      console.error('Get current user error:', error)
      // If token is invalid, clear storage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      return null
    }
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('token')
  },

  // Get stored user data
  getStoredUser: () => {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  }
}


