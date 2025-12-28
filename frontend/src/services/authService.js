/**
 * Authentication API service
 * Mock authentication until Hassan implements backend
 */

import apiClient from './api'

// Mock user storage
const MOCK_USERS_KEY = 'instaintelli_mock_users'

// Initialize mock users if not exists
const initMockUsers = () => {
  if (!localStorage.getItem(MOCK_USERS_KEY)) {
    const mockUsers = [
      {
        user_id: 'user_1',
        email: 'demo@instaintelli.com',
        password: 'demo123',
        username: 'demo_user',
        full_name: 'Demo User',
        avatar_url: null
      }
    ]
    localStorage.setItem(MOCK_USERS_KEY, JSON.stringify(mockUsers))
  }
}

initMockUsers()

export const authService = {
  // Registration (Mock)
  register: async (userData) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const mockUsers = JSON.parse(localStorage.getItem(MOCK_USERS_KEY) || '[]')
    
    // Check if user exists
    if (mockUsers.find(u => u.email === userData.email)) {
      throw new Error('User with this email already exists')
    }
    
    // Create new user
    const newUser = {
      user_id: `user_${Date.now()}`,
      email: userData.email,
      password: userData.password, // In real app, this would be hashed
      username: userData.username || userData.email.split('@')[0],
      full_name: userData.full_name || userData.username || 'User',
      avatar_url: null,
      created_at: new Date().toISOString()
    }
    
    mockUsers.push(newUser)
    localStorage.setItem(MOCK_USERS_KEY, JSON.stringify(mockUsers))
    
    // Return mock response
    return {
      user: {
        user_id: newUser.user_id,
        email: newUser.email,
        username: newUser.username,
        full_name: newUser.full_name
      },
      access_token: `mock_token_${Date.now()}`,
      refresh_token: `mock_refresh_${Date.now()}`
    }
  },

  // Login (Mock)
  login: async (credentials) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const mockUsers = JSON.parse(localStorage.getItem(MOCK_USERS_KEY) || '[]')
    const user = mockUsers.find(
      u => u.email === credentials.email && u.password === credentials.password
    )
    
    if (!user) {
      throw new Error('Invalid email or password')
    }
    
    // Return mock response
    return {
      user: {
        user_id: user.user_id,
        email: user.email,
        username: user.username,
        full_name: user.full_name,
        avatar_url: user.avatar_url
      },
      access_token: `mock_token_${Date.now()}`,
      refresh_token: `mock_refresh_${Date.now()}`
    }
  },

  // Logout (Mock)
  logout: async () => {
    // Just clear local storage
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    return { message: 'Logged out successfully' }
  },

  // Get current user (Mock)
  getCurrentUser: async () => {
    const userStr = localStorage.getItem('user')
    if (!userStr) {
      throw new Error('Not authenticated')
    }
    return JSON.parse(userStr)
  },

  // Refresh token (Mock)
  refreshToken: async (refreshToken) => {
    await new Promise(resolve => setTimeout(resolve, 300))
    return {
      access_token: `mock_token_${Date.now()}`,
      refresh_token: `mock_refresh_${Date.now()}`
    }
  }
}


