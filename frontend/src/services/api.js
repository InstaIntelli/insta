/**
 * API service configuration
 * To be implemented by team
 */

import axios from 'axios'

// Placeholder - to be configured with environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // Increased timeout for big data operations and uploads
  headers: {},
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

/**
 * Format API error into a human-readable string
 * Handles strings, FastAPI validation objects, and arrays
 */
export const formatApiError = (err) => {
  if (!err) return 'An unknown error occurred';

  // Specific handling for FastAPI/Pydantic validation errors
  if (err.response?.data?.detail) {
    const detail = err.response.data.detail;

    if (typeof detail === 'string') return detail;

    if (Array.isArray(detail)) {
      return detail
        .map(d => {
          if (typeof d === 'string') return d;
          // Format loc and msg for human readability if available
          const location = d.loc ? `(${d.loc.join('.')}) ` : '';
          return `${location}${d.msg || JSON.stringify(d)}`;
        })
        .join(', ');
    }

    if (typeof detail === 'object') {
      return detail.msg || JSON.stringify(detail);
    }
  }

  // Fallback to message or generic error
  return (
    err.response?.data?.message ||
    err.response?.data?.error ||
    err.message ||
    'An unexpected error occurred'
  );
};

export default apiClient

