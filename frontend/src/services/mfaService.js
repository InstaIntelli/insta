/**
 * Multi-Factor Authentication API service
 */

import apiClient from './api'

export const mfaService = {
  // Setup MFA (get QR code and secret)
  setupMFA: async () => {
    try {
      const response = await apiClient.post('/api/v1/mfa/setup')
      return response.data
    } catch (error) {
      console.error('MFA setup error:', error)
      throw error
    }
  },

  // Enable MFA (verify TOTP code)
  enableMFA: async (code) => {
    try {
      const response = await apiClient.post('/api/v1/mfa/enable', { code })
      return response.data
    } catch (error) {
      console.error('MFA enable error:', error)
      throw error
    }
  },

  // Disable MFA
  disableMFA: async (code) => {
    try {
      const response = await apiClient.post('/api/v1/mfa/disable', { code })
      return response.data
    } catch (error) {
      console.error('MFA disable error:', error)
      throw error
    }
  },

  // Get MFA status
  getMFAStatus: async () => {
    try {
      const response = await apiClient.get('/api/v1/mfa/status')
      return response.data
    } catch (error) {
      console.error('MFA status error:', error)
      throw error
    }
  },

  // Regenerate recovery codes
  regenerateRecoveryCodes: async (code) => {
    try {
      const response = await apiClient.post('/api/v1/mfa/recovery-codes/regenerate', { code })
      return response.data
    } catch (error) {
      console.error('Recovery codes regeneration error:', error)
      throw error
    }
  },

  // Verify MFA during login
  verifyMFALogin: async (userId, code) => {
    try {
      const response = await apiClient.post('/api/v1/auth/mfa/verify', {
        user_id: userId,
        code
      })
      
      // Store token and user data
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      
      return response.data
    } catch (error) {
      console.error('MFA verification error:', error)
      throw error
    }
  }
}


