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
      // Cache OAuth URL for faster subsequent calls
      const cacheKey = `oauth_url_${redirectTo}`
      const cached = sessionStorage.getItem(cacheKey)
      if (cached) {
        return cached
      }
      
      const response = await apiClient.get('/api/v1/auth/oauth/google/url', {
        params: { redirect_to: redirectTo },
        timeout: 5000 // 5 second timeout for fast failure
      })
      const oauthUrl = response.data.oauth_url
      
      // Cache for 5 minutes
      sessionStorage.setItem(cacheKey, oauthUrl)
      setTimeout(() => sessionStorage.removeItem(cacheKey), 5 * 60 * 1000)
      
      return oauthUrl
    } catch (error) {
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
      // Optimized: Use fastest path available
      let response
      if (accessToken && user) {
        // Fastest path: Direct token + user data
        response = await apiClient.post('/api/v1/auth/oauth/google/callback', {
          access_token: accessToken,
          user: user,
          redirect_to: redirectTo
        }, { timeout: 8000 })
      } else if (code) {
        // Standard path: Exchange code
        response = await apiClient.post('/api/v1/auth/oauth/google/callback', {
          code: code,
          redirect_to: redirectTo
        }, { timeout: 8000 })
      } else {
        throw new Error('No code or access_token provided')
      }
      
      // Store immediately for instant login
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      } else {
        throw new Error('No access token received')
      }
      
      return response.data
    } catch (error) {
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
        // Immediate redirect - no delay
        window.location.href = oauthUrl
      } else {
        throw new Error('Failed to get OAuth URL')
      }
    } catch (error) {
      throw error
    }
  }
}
