/**
 * Profile Management Service
 */

import apiClient from './api'

export const profileService = {
  /**
   * Get current user's profile
   * @returns {Promise<Object>} User profile
   */
  getMyProfile: async () => {
    try {
      const response = await apiClient.get('/api/v1/profile/me')
      return response.data
    } catch (error) {
      console.error('Error getting profile:', error)
      throw error
    }
  },

  /**
   * Update profile
   * @param {Object} profileData - Profile data to update
   * @returns {Promise<Object>} Updated profile
   */
  updateProfile: async (profileData) => {
    try {
      const response = await apiClient.put('/api/v1/profile/me', profileData)
      return response.data
    } catch (error) {
      console.error('Error updating profile:', error)
      throw error
    }
  },

  /**
   * Upload profile picture
   * @param {File} file - Image file
   * @returns {Promise<Object>} Updated profile with new picture URL
   */
  uploadProfilePicture: async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await apiClient.post('/api/v1/profile/me/picture', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      console.error('Error uploading profile picture:', error)
      throw error
    }
  },

  /**
   * Change password
   * @param {string} currentPassword - Current password
   * @param {string} newPassword - New password
   * @returns {Promise<Object>} Success message
   */
  changePassword: async (currentPassword, newPassword) => {
    try {
      const response = await apiClient.post('/api/v1/profile/me/password', {
        current_password: currentPassword,
        new_password: newPassword
      })
      return response.data
    } catch (error) {
      console.error('Error changing password:', error)
      throw error
    }
  },

  /**
   * Get user profile by ID (public)
   * @param {string} userId - User ID
   * @returns {Promise<Object>} User profile
   */
  getUserProfile: async (userId) => {
    try {
      const response = await apiClient.get(`/api/v1/profile/${userId}`)
      return response.data
    } catch (error) {
      console.error('Error getting user profile:', error)
      throw error
    }
  }
}
