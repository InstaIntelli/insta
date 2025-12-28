/**
 * Login Page - Instagram-like Design
 */

import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authService } from '../services/authService'
import './Auth.css'

function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await authService.login({ email, password })
      
      // Store token
      if (response.access_token) {
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
        localStorage.setItem('user', JSON.stringify(response.user))
      }

      navigate('/feed')
    } catch (err) {
      setError(err.message || err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>InstaIntelli</h1>
        <h2>Welcome back</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Email"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Password"
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Logging in...' : 'Log In'}
          </button>
        </form>

        <p className="auth-link">
          Don't have an account? <Link to="/register">Sign up</Link>
        </p>

        <div className="demo-info">
          <strong>Demo Account:</strong>
          Email: demo@instaintelli.com<br />
          Password: demo123
        </div>
      </div>
    </div>
  )
}

export default LoginPage


