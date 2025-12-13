/**
 * API service configuration
 * To be implemented by team
 */

import axios from 'axios'

// Placeholder - to be configured with environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - to be implemented (e.g., for auth tokens)
// apiClient.interceptors.request.use((config) => {
//   const token = localStorage.getItem('token')
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`
//   }
//   return config
// })

// Response interceptor - to be implemented (e.g., for error handling)
// apiClient.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     // Handle errors
//     return Promise.reject(error)
//   }
// )

export default apiClient

