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
  handleCallback: async (code, redirectTo = `${window.location.origin}/auth/callback`, accessToken = null, user = null) => {
    try {
      console.log('🔄 Handling OAuth callback:', { code: code ? 'present' : 'missing', accessToken: accessToken ? 'present' : 'missing', hasUser: !!user })
      
      // If we have access_token and user (from Supabase direct redirect), send as JSON body
      // Otherwise, send code as JSON body (not query params) for better reliability
      let response
      if (accessToken && user) {
        console.log('📤 Sending access_token and user to backend')
        response = await apiClient.post('/api/v1/auth/oauth/google/callback', {
          access_token: accessToken,
          user: user,
          redirect_to: redirectTo
        })
      } else if (code) {
        console.log('📤 Sending code to backend')
        response = await apiClient.post('/api/v1/auth/oauth/google/callback', {
          code: code,
          redirect_to: redirectTo
        })
      } else {
        throw new Error('No code or access_token provided')
      }
      
      console.log('✅ OAuth callback successful:', response.data)
      
      // Store token and user data
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        console.log('💾 Stored token and user data')
      } else {
        console.warn('⚠️ No access_token in response')
      }
      
      return response.data
    } catch (error) {
      console.error('❌ OAuth callback error:', error)
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      })
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
      console.log('🔄 Getting OAuth URL for:', redirectTo)
      const oauthUrl = await googleAuthService.getOAuthUrl(redirectTo)
      
      if (oauthUrl) {
        console.log('✅ Got OAuth URL, redirecting to:', oauthUrl.substring(0, 80) + '...')
        // Redirect to Google OAuth
        window.location.href = oauthUrl
      } else {
        throw new Error('Failed to get OAuth URL from server')
      }
    } catch (error) {
      console.error('❌ Error initiating Google OAuth:', error)
      throw error
    }
  }
}
