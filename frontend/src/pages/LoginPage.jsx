/**
 * Modern Login Page with enhanced UI
 */

import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authService } from '../services/authService'
import { googleAuthService } from '../services/googleAuthService'
import MFAVerification from '../components/MFAVerification'
import './Auth.css'

function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [mfaRequired, setMfaRequired] = useState(false)
  const [mfaUserId, setMfaUserId] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await authService.login({ email, password })
      
      // Check if MFA is required
      if (response.mfa_required) {
        setMfaRequired(true)
        setMfaUserId(response.user_id)
        setLoading(false)
        return
      }
      
      // No MFA - proceed with login
      if (response.access_token) {
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('user', JSON.stringify(response.user))
      }

      navigate('/feed')
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  const handleMFACancel = () => {
    setMfaRequired(false)
    setMfaUserId('')
    setPassword('')
  }

  const handleGoogleSignIn = async () => {
    setError('')
    setLoading(true)
    try {
      console.log('🔄 Initiating Google OAuth...')
      const oauthUrl = await googleAuthService.getOAuthUrl()
      
      if (!oauthUrl) {
        throw new Error('Failed to get OAuth URL from server')
      }
      
      console.log('✅ Got OAuth URL, redirecting...')
      // Redirect to Google OAuth page
      window.location.href = oauthUrl
      // Note: setLoading(false) won't execute because page is redirecting
    } catch (err) {
      console.error('❌ Google sign-in error:', err)
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to sign in with Google'
      setError(errorMsg)
      setLoading(false)
    }
  }

  // Show MFA verification if required
  if (mfaRequired) {
    return <MFAVerification userId={mfaUserId} email={email} onCancel={handleMFACancel} />
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card modern-card">
          <div className="auth-header">
            <h1 className="brand-logo">InstaIntelli</h1>
            <p className="auth-subtitle">Welcome back! Please login to your account.</p>
          </div>

          {error && (
            <div className="error-message animate-shake">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group modern">
              <div className="input-wrapper">
                <span className="input-icon">📧</span>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="Email address"
                  className="modern-input"
                />
              </div>
            </div>

            <div className="form-group modern">
              <div className="input-wrapper">
                <span className="input-icon">🔒</span>
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="Password"
                  className="modern-input"
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
            </div>

            <button 
              type="submit" 
              disabled={loading} 
              className="btn-primary modern-btn"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <div className="auth-divider">
            <span>OR</span>
          </div>

          <button
            type="button"
            onClick={handleGoogleSignIn}
            disabled={loading}
            className="btn-google modern-btn"
          >
            <span className="google-icon">🔍</span>
            Continue with Google
          </button>

          <div className="auth-footer">
            <p>
              Don't have an account?{' '}
              <Link to="/register" className="auth-link">
                Sign up now
              </Link>
            </p>
            <p className="back-home">
              <Link to="/" className="auth-link">
                ← Back to home
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
