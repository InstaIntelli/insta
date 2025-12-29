/**
 * Profile Page with MFA Management
 */

import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { userService } from '../services/userService'
import { mfaService } from '../services/mfaService'
import './Profile.css'

function ProfilePage() {
  const { userId } = useParams()
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [mfaStatus, setMfaStatus] = useState({ mfa_enabled: false, has_recovery_codes: false })
  const [showDisableMFA, setShowDisableMFA] = useState(false)
  const [disableCode, setDisableCode] = useState('')
  const [mfaError, setMfaError] = useState('')

  useEffect(() => {
    loadUser()
    loadMFAStatus()
  }, [userId])

  const loadUser = async () => {
    try {
      const data = await userService.getUser(userId)
      setUser(data)
    } catch (err) {
      setError('Failed to load user profile')
    } finally {
      setLoading(false)
    }
  }

  const loadMFAStatus = async () => {
    try {
      const status = await mfaService.getMFAStatus()
      setMfaStatus(status)
    } catch (err) {
      console.error('Failed to load MFA status:', err)
    }
  }

  const handleEnableMFA = () => {
    navigate('/mfa/setup')
  }

  const handleDisableMFA = async () => {
    if (!disableCode) {
      setMfaError('Please enter verification code')
      return
    }

    try {
      await mfaService.disableMFA(disableCode)
      setMfaStatus({ mfa_enabled: false, has_recovery_codes: false })
      setShowDisableMFA(false)
      setDisableCode('')
      setMfaError('')
      alert('MFA disabled successfully')
    } catch (err) {
      setMfaError(err.response?.data?.detail || 'Failed to disable MFA')
    }
  }

  if (loading) return <div className="loading">Loading profile...</div>
  if (error) return <div className="error">{error}</div>
  if (!user) return <div className="error">User not found</div>

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="profile-avatar">
          {user.profile_picture ? (
            <img src={user.profile_picture} alt={user.username} />
          ) : (
            <div className="avatar-placeholder">{user.username[0].toUpperCase()}</div>
          )}
        </div>
        <div className="profile-info">
          <h1>{user.username}</h1>
          <p>{user.bio || 'No bio yet'}</p>
          <div className="profile-stats">
            <span><strong>{user.posts_count || 0}</strong> posts</span>
            <span><strong>{user.followers_count || 0}</strong> followers</span>
            <span><strong>{user.following_count || 0}</strong> following</span>
          </div>
        </div>
      </div>

      {/* MFA Section */}
      <div className="profile-section mfa-section">
        <h2>🔐 Two-Factor Authentication</h2>
        <div className="mfa-status-card">
          {mfaStatus.mfa_enabled ? (
            <>
              <div className="mfa-enabled">
                <span className="status-badge enabled">✓ Enabled</span>
                <p>Your account is protected with two-factor authentication</p>
              </div>
              
              {!showDisableMFA ? (
                <button 
                  onClick={() => setShowDisableMFA(true)}
                  className="btn-danger"
                >
                  Disable MFA
                </button>
              ) : (
                <div className="disable-mfa-form">
                  {mfaError && <div className="error-message">{mfaError}</div>}
                  <p>Enter your authenticator code or recovery code to disable MFA:</p>
                  <input
                    type="text"
                    value={disableCode}
                    onChange={(e) => setDisableCode(e.target.value)}
                    placeholder="000000 or XXXX-XXXX"
                    className="code-input"
                  />
                  <div className="button-group">
                    <button onClick={() => {
                      setShowDisableMFA(false)
                      setDisableCode('')
                      setMfaError('')
                    }} className="btn-secondary">
                      Cancel
                    </button>
                    <button onClick={handleDisableMFA} className="btn-danger">
                      Confirm Disable
                    </button>
                  </div>
                </div>
              )}
            </>
          ) : (
            <>
              <div className="mfa-disabled">
                <span className="status-badge disabled">✗ Disabled</span>
                <p>Add an extra layer of security to your account with Google Authenticator</p>
              </div>
              <button onClick={handleEnableMFA} className="btn-primary">
                Enable Two-Factor Authentication
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
