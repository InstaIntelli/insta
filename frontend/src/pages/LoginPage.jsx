/**
 * Login Page
 */

import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authService } from '../services/authService'
import MFAVerification from '../components/MFAVerification'
import './Auth.css'

function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [mfaRequired, setMfaRequired] = useState(false)
  const [mfaUserId, setMfaUserId] = useState('')
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
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleMFACancel = () => {
    setMfaRequired(false)
    setMfaUserId('')
    setPassword('')
  }

  // Show MFA verification if required
  if (mfaRequired) {
    return <MFAVerification userId={mfaUserId} email={email} onCancel={handleMFACancel} />
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>InstaIntelli</h1>
        <h2>Login</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="your@email.com"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="auth-link">
          Don't have an account? <Link to="/register">Sign up</Link>
        </p>
      </div>
    </div>
  )
}

export default LoginPage


