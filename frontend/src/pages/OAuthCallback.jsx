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
        // Fast parsing - check hash first (Supabase uses hash)
        const hashParams = new URLSearchParams(window.location.hash.substring(1))
        const urlParams = new URLSearchParams(window.location.search)
        
        const code = hashParams.get('code') || urlParams.get('code') || searchParams.get('code')
        const errorParam = hashParams.get('error') || urlParams.get('error') || searchParams.get('error')
        const accessToken = hashParams.get('access_token')

        if (errorParam) {
          setError(`Authentication error: ${errorParam}`)
          setLoading(false)
          setTimeout(() => navigate('/login'), 2000)
          return
        }

        const redirectTo = `${window.location.origin}/auth/callback`

        // Fastest path: Direct access token
        if (accessToken && !code) {
          try {
            const supabaseUrl = 'https://mrnlqzxvlpjjrjnxngpk.supabase.co'
            const response = await fetch(`${supabaseUrl}/auth/v1/user`, {
              headers: {
                'Authorization': `Bearer ${accessToken}`,
                'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ybmxxenh2bHBqanJqbnhuZ3BrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgyNDEyMDIsImV4cCI6MjA4MzgxNzIwMn0.VJSBn87b7z5ixqUEKeIDZHKh2Ba3aVOcq5ejAu3aIEU'
              }
            })
            
            if (response.ok) {
              const userData = await response.json()
              await googleAuthService.handleCallback(null, redirectTo, accessToken, userData)
              // Immediate redirect - no delay
              navigate('/feed', { replace: true })
              return
            }
          } catch (err) {
            setError('Authentication failed')
            setLoading(false)
            setTimeout(() => navigate('/login'), 2000)
            return
          }
        }

        if (!code) {
          setError('No authorization code received')
          setLoading(false)
          setTimeout(() => navigate('/login'), 2000)
          return
        }

        // Exchange code - optimized
        await googleAuthService.handleCallback(code, redirectTo)
        // Immediate redirect
        navigate('/feed', { replace: true })
      } catch (err) {
        setError(err.response?.data?.detail || err.message || 'Authentication failed')
        setLoading(false)
        setTimeout(() => navigate('/login'), 2000)
      }
    }

    // Execute immediately
    handleCallback()
  }, [searchParams, navigate])

  if (loading) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="auth-card modern-card">
            <div className="auth-header">
              <h1 className="brand-logo">InstaIntelli</h1>
              <p className="auth-subtitle">Signing you in...</p>
            </div>
            <div style={{ textAlign: 'center', padding: '40px 0' }}>
              <div className="spinner" style={{ margin: '0 auto', width: '50px', height: '50px', borderWidth: '4px' }}></div>
              <p style={{ marginTop: '24px', color: '#666', fontSize: '16px', fontWeight: '500' }}>Almost there!</p>
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
