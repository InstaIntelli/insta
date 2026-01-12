/**
 * Profile Page with MFA Management
 */

import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { userService } from '../services/userService'
import { mfaService } from '../services/mfaService'
import { socialService } from '../services/socialService'
import { getUser } from '../utils/auth'
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
  const [isFollowing, setIsFollowing] = useState(false)
  const [isFollowingLoading, setIsFollowingLoading] = useState(false)
  const [followersCount, setFollowersCount] = useState(0)
  const [followingCount, setFollowingCount] = useState(0)
  const currentUser = getUser()
  const isOwnProfile = currentUser && currentUser.user_id === userId

  useEffect(() => {
    loadUser()
    if (isOwnProfile) {
      loadMFAStatus()
    }
    if (!isOwnProfile && userId) {
      loadFollowStatus()
      loadSocialStats()
    }
  }, [userId, isOwnProfile])

  const loadUser = async () => {
    try {
      const data = await userService.getUser(userId)
      setUser(data)
      // Update counts from user data if available
      if (data.followers_count !== undefined) setFollowersCount(data.followers_count)
      if (data.following_count !== undefined) setFollowingCount(data.following_count)
    } catch (err) {
      setError('Failed to load user profile')
    } finally {
      setLoading(false)
    }
  }

  const loadFollowStatus = async () => {
    if (!currentUser) return
    try {
      const response = await socialService.checkFollowing(userId)
      setIsFollowing(response.is_following || false)
    } catch (err) {
      console.error('Error loading follow status:', err)
    }
  }

  const loadSocialStats = async () => {
    try {
      const response = await socialService.getUserStats?.(userId) || {}
      if (response.follower_count !== undefined) setFollowersCount(response.follower_count)
      if (response.following_count !== undefined) setFollowingCount(response.following_count)
    } catch (err) {
      // Try alternative endpoint
      try {
        const followers = await socialService.getFollowers(userId)
        const following = await socialService.getFollowing(userId)
        setFollowersCount(followers.count || followers.followers?.length || 0)
        setFollowingCount(following.count || following.following?.length || 0)
      } catch (e) {
        console.error('Error loading social stats:', e)
      }
    }
  }

  const handleFollow = async () => {
    if (!currentUser) {
      navigate('/login')
      return
    }

    if (isFollowingLoading) return
    setIsFollowingLoading(true)

    try {
      if (isFollowing) {
        await socialService.unfollowUser(userId)
        setIsFollowing(false)
        setFollowersCount(prev => Math.max(0, prev - 1))
      } else {
        await socialService.followUser(userId)
        setIsFollowing(true)
        setFollowersCount(prev => prev + 1)
      }
    } catch (err) {
      console.error('Error following user:', err)
      alert(err.response?.data?.detail || 'Failed to follow user')
    } finally {
      setIsFollowingLoading(false)
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
          <div className="profile-header-top">
            <h1>{user.username}</h1>
            {!isOwnProfile && currentUser && (
              <button
                className={`follow-btn ${isFollowing ? 'following' : ''}`}
                onClick={handleFollow}
                disabled={isFollowingLoading}
              >
                {isFollowingLoading ? '...' : isFollowing ? 'Following' : 'Follow'}
              </button>
            )}
          </div>
          <p>{user.bio || 'No bio yet'}</p>
          <div className="profile-stats">
            <span><strong>{user.posts_count || 0}</strong> posts</span>
            <span><strong>{followersCount}</strong> followers</span>
            <span><strong>{followingCount}</strong> following</span>
          </div>
        </div>
      </div>

      {/* MFA Section - Only show on own profile */}
      {isOwnProfile && (
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
      )}
    </div>
  )
}

export default ProfilePage
