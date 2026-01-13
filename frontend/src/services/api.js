/**
 * API service configuration
 * To be implemented by team
 */

import axios from 'axios'

// Placeholder - to be configured with environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout for big data operations
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 unauthorized - redirect to login (but not for profile updates)
    if (error.response?.status === 401) {
      // Don't redirect if we're on profile settings page (might be a validation error)
      const isProfileUpdate = error.config?.url?.includes('/profile/me')
      if (!isProfileUpdate) {
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        // Use navigate instead of window.location to avoid full page reload
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient

