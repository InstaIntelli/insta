/**
 * Profile Page with MFA Management
 */

import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { profileService } from '../services/profileService'
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
  const [refreshing, setRefreshing] = useState(false)
  const [mfaStatus, setMfaStatus] = useState({ mfa_enabled: false, has_recovery_codes: false })
  const [showDisableMFA, setShowDisableMFA] = useState(false)
  const [disableCode, setDisableCode] = useState('')
  const [mfaError, setMfaError] = useState('')
  const [isFollowing, setIsFollowing] = useState(false)
  const [isFollowingLoading, setIsFollowingLoading] = useState(false)
  const [followersCount, setFollowersCount] = useState(0)
  const [followingCount, setFollowingCount] = useState(0)
  const [modalType, setModalType] = useState(null) // 'followers' or 'following' or null
  const [modalData, setModalData] = useState([])
  const [modalLoading, setModalLoading] = useState(false)
  const [modalError, setModalError] = useState('')
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
  }, [userId])

  // Refresh profile when returning to page (e.g., after editing)
  useEffect(() => {
    let isMounted = true

    // Listen for profile updates from settings page (only once per event)
    const handleProfileUpdate = () => {
      if (isMounted && userId && !loading && !refreshing) {
        loadUser(true)
      }
    }

    window.addEventListener('profileUpdated', handleProfileUpdate)

    return () => {
      isMounted = false
      window.removeEventListener('profileUpdated', handleProfileUpdate)
    }
  }, [userId]) // Remove loading from dependencies to prevent loops

  const loadUser = async (showRefreshing = false) => {
    try {
      if (showRefreshing) {
        setRefreshing(true)
      } else {
        setLoading(true)
        setError('') // Clear previous errors
      }

      // Use profile service which has caching
      let data
      try {
        data = await profileService.getUserProfile(userId)
      } catch (profileErr) {
        // Fallback to user service if profile service fails
        console.warn('Profile service failed, trying user service:', profileErr)
        const { userService } = await import('../services/userService')
        data = await userService.getUser(userId)
      }

      if (!data) {
        throw new Error('No user data received')
      }

      // Map field names (profile_image_url -> profile_picture for compatibility)
      const mappedData = {
        ...data,
        profile_picture: data.profile_image_url || data.profile_picture,
        profile_image_url: data.profile_image_url || data.profile_picture
      }

      setUser(mappedData)
      // Update counts from user data if available
      if (data.posts_count !== undefined) {
        // Posts count is now in the response
      }
      if (data.followers_count !== undefined) setFollowersCount(data.followers_count)
      if (data.following_count !== undefined) setFollowingCount(data.following_count)
    } catch (err) {
      console.error('Error loading profile:', err)
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load user profile'
      setError(errorMessage)
      // Don't clear user data if we're just refreshing
      if (!showRefreshing) {
        setUser(null)
      }
    } finally {
      setLoading(false)
      setRefreshing(false)
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

  const refreshFollowCounts = async () => {
    await loadSocialStats()
  }

  const loadModalData = async (type) => {
    try {
      setModalType(type)
      setModalLoading(true)
      setModalError('')

      let data
      if (type === 'followers') {
        data = await socialService.getFollowers(userId)
      } else {
        data = await socialService.getFollowing(userId)
      }

      setModalData(data.followers || data.following || data.users || [])
    } catch (err) {
      console.error('Error loading list data:', err)
      setModalError('Failed to load list')
    } finally {
      setModalLoading(false)
    }
  }

  const handleModalFollow = async (itemUserId, e) => {
    e.preventDefault()
    if (!currentUser) {
      navigate('/login')
      return
    }

    try {
      const isCurrentlyFollowing = modalData.find(u => u.user_id === itemUserId)?.is_following

      // Update local modal data optimistically
      setModalData(prev => prev.map(u =>
        u.user_id === itemUserId ? { ...u, is_following: !isCurrentlyFollowing } : u
      ))

      if (isCurrentlyFollowing) {
        await socialService.unfollowUser(itemUserId)
      } else {
        await socialService.followUser(itemUserId)
      }

      // If we are looking at someone else's profile and follow/unfollow them from THEIR followers list
      if (itemUserId === userId) {
        setIsFollowing(!isCurrentlyFollowing)
      }

      refreshFollowCounts()
    } catch (err) {
      console.error('Error in modal follow:', err)
      // Revert optimistic update
      setModalData(prev => prev.map(u =>
        u.user_id === itemUserId ? { ...u, is_following: !u.is_following } : u
      ))
    }
  }

  const handleFollow = async () => {
    if (!currentUser) {
      navigate('/login')
      return
    }

    if (isFollowingLoading) return
    setIsFollowingLoading(true)

    const wasFollowing = isFollowing

    try {
      // Optimistic update - update UI immediately
      setIsFollowing(!wasFollowing)
      setFollowersCount(prev => wasFollowing ? Math.max(0, prev - 1) : prev + 1)

      if (wasFollowing) {
        await socialService.unfollowUser(userId)
      } else {
        await socialService.followUser(userId)
      }

      // Refresh counts to ensure accuracy
      refreshFollowCounts()
    } catch (err) {
      console.error('Error following user:', err)
      // Rollback optimistic update on error
      setIsFollowing(wasFollowing)
      setFollowersCount(prev => wasFollowing ? prev + 1 : Math.max(0, prev - 1))
      alert(err.response?.data?.detail || 'Failed to follow user')
    } finally {
      setIsFollowingLoading(false)
    }
  }

  // Listen for follow updates from other components (like RightSidebar)
  useEffect(() => {
    const handleFollowUpdate = (event) => {
      const { userId: updatedUserId, isFollowing: newFollowingState } = event.detail
      if (updatedUserId === userId) {
        setIsFollowing(newFollowingState)
        refreshFollowCounts()
      }
    }

    window.addEventListener('followUpdated', handleFollowUpdate)
    return () => window.removeEventListener('followUpdated', handleFollowUpdate)
  }, [userId])

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

  if (loading) {
    return (
      <div className="profile-container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading profile...</p>
        </div>
      </div>
    )
  }

  if (error && !user) {
    return (
      <div className="profile-container">
        <div className="error-container">
          <div className="error-icon">⚠️</div>
          <p>{error}</p>
          <button className="btn-retry" onClick={() => loadUser()}>
            Try Again
          </button>
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="profile-container">
        <div className="error-container">
          <div className="error-icon">👤</div>
          <p>User not found</p>
        </div>
      </div>
    )
  }

  return (
    <div className="profile-container">
      {refreshing && (
        <div className="refreshing-overlay">
          <div className="refreshing-indicator">
            <div className="spinner"></div>
            <span>Updating profile...</span>
          </div>
        </div>
      )}
      {error && user && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={() => loadUser(true)} className="btn-retry-small">Retry</button>
        </div>
      )}
      <div className="profile-header">
        <div className="profile-avatar">
          {user.profile_picture || user.profile_image_url ? (
            <img
              src={user.profile_picture || user.profile_image_url}
              alt={user.username}
              onError={(e) => {
                e.target.style.display = 'none'
                const placeholder = e.target.nextElementSibling
                if (placeholder) placeholder.style.display = 'flex'
              }}
            />
          ) : null}
          <div
            className="avatar-placeholder"
            style={{ display: (user.profile_picture || user.profile_image_url) ? 'none' : 'flex' }}
          >
            {user.username?.[0]?.toUpperCase() || 'U'}
          </div>
        </div>
        <div className="profile-info">
          <div className="profile-header-top">
            <h1>{user.username}</h1>
            <div className="profile-actions">
              {isOwnProfile ? (
                <button
                  className="btn-edit-profile"
                  onClick={() => navigate('/profile/settings')}
                >
                  Edit Profile
                </button>
              ) : currentUser && (
                <button
                  className={`follow-btn ${isFollowing ? 'following' : ''}`}
                  onClick={handleFollow}
                  disabled={isFollowingLoading}
                >
                  {isFollowingLoading ? '...' : isFollowing ? 'Following' : 'Follow'}
                </button>
              )}
            </div>
          </div>
          <p className="profile-bio">{user.bio || 'No bio yet'}</p>
          <div className="profile-stats">
            <div className="stat-item">
              <span className="stat-value">{user.posts_count ?? 0}</span>
              <span className="stat-label">Posts</span>
            </div>
            <div
              className="stat-item clickable"
              onClick={() => loadModalData('followers')}
            >
              <span className="stat-value">{user.followers_count ?? followersCount}</span>
              <span className="stat-label">Followers</span>
            </div>
            <div
              className="stat-item clickable"
              onClick={() => loadModalData('following')}
            >
              <span className="stat-value">{user.following_count ?? followingCount}</span>
              <span className="stat-label">Following</span>
            </div>
          </div>
        </div>
      </div>

      {/* MFA Section - Only show on own profile */}
      {isOwnProfile && (
        <div className="profile-section mfa-section">
          <h2>🔐 Security Center</h2>
          <div className="mfa-status-card">
            <div className="mfa-info-group">
              {mfaStatus.mfa_enabled ? (
                <>
                  <div className="mfa-text">
                    <span className="status-badge enabled">✓ MFA ENHANCED</span>
                    <p>Your account is protected with Two-Factor Authentication via Google Authenticator.</p>
                  </div>

                  {!showDisableMFA ? (
                    <button
                      onClick={() => setShowDisableMFA(true)}
                      className="btn-danger"
                    >
                      Disable Security
                    </button>
                  ) : (
                    <div className="disable-mfa-form">
                      {mfaError && <div className="error-message">{mfaError}</div>}
                      <p>Enter your 6-digit authenticator code to confirm:</p>
                      <input
                        type="text"
                        value={disableCode}
                        onChange={(e) => setDisableCode(e.target.value)}
                        placeholder="000 000"
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
                  <div className="mfa-text">
                    <span className="status-badge disabled">✗ MFA AT RISK</span>
                    <p>Enhance your account security by enabling Two-Factor Authentication.</p>
                  </div>
                  <button onClick={handleEnableMFA} className="btn-primary">
                    Enable Security Center
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* List Modal */}
      {modalType && (
        <div className="list-modal-overlay" onClick={() => setModalType(null)}>
          <div className="list-modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="list-modal-header">
              <h3>{modalType === 'followers' ? 'Followers' : 'Following'}</h3>
              <button className="btn-close-modal" onClick={() => setModalType(null)}>×</button>
            </div>
            <div className="list-modal-body">
              {modalLoading ? (
                <div className="modal-loading">
                  <div className="spinner-small"></div>
                  <p>Loading...</p>
                </div>
              ) : modalError ? (
                <div className="modal-error">{modalError}</div>
              ) : modalData.length > 0 ? (
                <div className="modal-list">
                  {modalData.map((item) => (
                    <div key={item.user_id} className="modal-list-item">
                      <div className="item-user-info" onClick={() => {
                        navigate(`/profile/${item.user_id}`)
                        setModalType(null)
                      }}>
                        <div className="item-avatar">
                          {item.profile_image_url || item.profile_picture ? (
                            <img src={item.profile_image_url || item.profile_picture} alt={item.username} />
                          ) : (
                            <div className="avatar-placeholder-small">
                              {item.username?.[0]?.toUpperCase() || 'U'}
                            </div>
                          )}
                        </div>
                        <div className="item-names">
                          <span className="item-username">{item.username}</span>
                          {item.full_name && <span className="item-full-name">{item.full_name}</span>}
                        </div>
                      </div>
                      {currentUser && currentUser.user_id !== item.user_id && (
                        <button
                          className={`btn-modal-follow ${item.is_following ? 'following' : ''}`}
                          onClick={(e) => handleModalFollow(item.user_id, e)}
                        >
                          {item.is_following ? 'Following' : 'Follow'}
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="modal-empty">
                  No {modalType} yet
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProfilePage
