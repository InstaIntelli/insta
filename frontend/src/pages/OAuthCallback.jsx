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
        // Check both query parameters and hash fragments
        // Supabase may use hash fragments (#) instead of query params (?)
        const urlParams = new URLSearchParams(window.location.search)
        const hashParams = new URLSearchParams(window.location.hash.substring(1))
        
        // Try to get code from query params first, then hash
        const code = urlParams.get('code') || hashParams.get('code') || searchParams.get('code')
        const errorParam = urlParams.get('error') || hashParams.get('error') || searchParams.get('error')
        
        // Also check for access_token directly in hash (Supabase sometimes returns this)
        const accessToken = hashParams.get('access_token')
        
        console.log('OAuth Callback Debug:', {
          search: window.location.search,
          hash: window.location.hash,
          code,
          error: errorParam,
          accessToken: accessToken ? 'present' : 'not present'
        })

        if (errorParam) {
          setError(`OAuth error: ${errorParam}`)
          setLoading(false)
          setTimeout(() => navigate('/login'), 3000)
          return
        }

        // If we have an access_token directly, we can use it (Supabase redirect)
        if (accessToken && !code) {
          // Supabase redirected with token directly - we need to get user info
          try {
            const redirectTo = `${window.location.origin}/auth/callback`
            // Use the access_token to get user info from Supabase
            const supabaseUrl = 'https://mrnlqzxvlpjjrjnxngpk.supabase.co'
            const response = await fetch(`${supabaseUrl}/auth/v1/user`, {
              headers: {
                'Authorization': `Bearer ${accessToken}`,
                'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ybmxxenh2bHBqanJqbnhuZ3BrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgyNDEyMDIsImV4cCI6MjA4MzgxNzIwMn0.VJSBn87b7z5ixqUEKeIDZHKh2Ba3aVOcq5ejAu3aIEU'
              }
            })
            
            if (response.ok) {
              const userData = await response.json()
              // Use the service to handle callback
              await googleAuthService.handleCallback(null, redirectTo, accessToken, userData)
              navigate('/feed')
              return
            } else {
              throw new Error('Failed to get user info from Supabase')
            }
          } catch (err) {
            console.error('Error handling access_token:', err)
            setError(err.message || 'Failed to authenticate with access token')
            setLoading(false)
            setTimeout(() => navigate('/login'), 3000)
            return
          }
        }

        if (!code) {
          console.error('No authorization code or access_token received')
          console.error('Full URL:', window.location.href)
          setError('No authorization code received. Please try again.')
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
