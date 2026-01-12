/**
 * OAuth Callback Handler
 * Handles Google OAuth callback and redirects user
 */

import React, { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { googleAuthService } from '../services/googleAuthService'
import './Auth.css'

function OAuthCallback() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const code = searchParams.get('code')
        const error = searchParams.get('error')

        if (error) {
          setError(`OAuth error: ${error}`)
          setLoading(false)
          setTimeout(() => navigate('/login'), 3000)
          return
        }

        if (!code) {
          setError('No authorization code received')
          setLoading(false)
          setTimeout(() => navigate('/login'), 3000)
          return
        }

        // Exchange code for token
        const redirectTo = `${window.location.origin}/auth/callback`
        await googleAuthService.handleCallback(code, redirectTo)

        // Redirect to feed
        navigate('/feed')
      } catch (err) {
        console.error('OAuth callback error:', err)
        setError(err.response?.data?.detail || 'Authentication failed. Please try again.')
        setLoading(false)
        setTimeout(() => navigate('/login'), 3000)
      }
    }

    handleCallback()
  }, [searchParams, navigate])

  if (loading) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="auth-card modern-card">
            <div className="auth-header">
              <h1 className="brand-logo">InstaIntelli</h1>
              <p className="auth-subtitle">Completing authentication...</p>
            </div>
            <div style={{ textAlign: 'center', padding: '40px 0' }}>
              <div className="spinner" style={{ margin: '0 auto' }}></div>
              <p style={{ marginTop: '20px', color: '#666' }}>Please wait while we sign you in...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="auth-card modern-card">
            <div className="auth-header">
              <h1 className="brand-logo">InstaIntelli</h1>
              <p className="auth-subtitle">Authentication Error</p>
            </div>
            <div className="error-message animate-shake">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
            <div className="auth-footer" style={{ marginTop: '20px' }}>
              <p>Redirecting to login page...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return null
}

export default OAuthCallback
