/**
 * Google OAuth Service using Supabase
 */

import apiClient from './api'

export const googleAuthService = {
  /**
   * Get Google OAuth URL
   * @param {string} redirectTo - URL to redirect after OAuth
   * @returns {Promise<string>} OAuth URL
   */
  getOAuthUrl: async (redirectTo = `${window.location.origin}/auth/callback`) => {
    try {
      const response = await apiClient.get('/api/v1/auth/oauth/google/url', {
        params: { redirect_to: redirectTo }
      })
      return response.data.oauth_url
    } catch (error) {
      console.error('Error getting OAuth URL:', error)
      throw error
    }
  },

  /**
   * Handle OAuth callback
   * @param {string} code - OAuth authorization code
   * @param {string} redirectTo - Redirect URL used in OAuth flow
   * @returns {Promise<Object>} User data and access token
   */
  handleCallback: async (code, redirectTo = `${window.location.origin}/auth/callback`) => {
    try {
      const response = await apiClient.post('/api/v1/auth/oauth/google/callback', null, {
        params: {
          code,
          redirect_to: redirectTo
        }
      })
      
      // Store token and user data
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      
      return response.data
    } catch (error) {
      console.error('OAuth callback error:', error)
      throw error
    }
  },

  /**
   * Initiate Google OAuth flow
   * Redirects user to Google OAuth page
   */
  signInWithGoogle: async () => {
    try {
      const redirectTo = `${window.location.origin}/auth/callback`
      const oauthUrl = await googleAuthService.getOAuthUrl(redirectTo)
      
      if (oauthUrl) {
        // Redirect to Google OAuth
        window.location.href = oauthUrl
      } else {
        throw new Error('Failed to get OAuth URL')
      }
    } catch (error) {
      console.error('Error initiating Google OAuth:', error)
      throw error
    }
  }
}
