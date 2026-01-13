/**
 * Profile Settings Page
 * Allows users to edit their profile, change password, upload picture
 */

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { profileService } from '../services/profileService'
import { getUser } from '../utils/auth'
import './ProfileSettings.css'

function ProfileSettingsPage() {
  const navigate = useNavigate()
  const currentUser = getUser()
  const [refreshing, setRefreshing] = useState(false) // Background refresh indicator
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  
  // Initialize from localStorage immediately for instant load
  const [username, setUsername] = useState(currentUser?.username || '')
  const [fullName, setFullName] = useState(currentUser?.full_name || '')
  const [bio, setBio] = useState(currentUser?.bio || '')
  const [profileImageUrl, setProfileImageUrl] = useState(currentUser?.profile_image_url || '')
  const [email, setEmail] = useState(currentUser?.email || '')
  
  // Password fields
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPasswordSection, setShowPasswordSection] = useState(false)
  
  // Picture upload
  const [uploadingPicture, setUploadingPicture] = useState(false)
  const [picturePreview, setPicturePreview] = useState(currentUser?.profile_image_url || '')

  useEffect(() => {
    if (!currentUser) {
      navigate('/login')
      return
    }
    
    // Load fresh data in background (non-blocking)
    loadProfileInBackground()
  }, [currentUser, navigate])

  // Load profile in background without blocking UI
  const loadProfileInBackground = async () => {
    try {
      setRefreshing(true)
      const profile = await profileService.getMyProfile()
      
      // Only update if data is different (avoid unnecessary re-renders)
      if (profile.username !== username) setUsername(profile.username || '')
      if (profile.full_name !== fullName) setFullName(profile.full_name || '')
      if (profile.bio !== bio) setBio(profile.bio || '')
      if (profile.profile_image_url !== profileImageUrl) {
        setProfileImageUrl(profile.profile_image_url || '')
        setPicturePreview(profile.profile_image_url || '')
      }
      if (profile.email !== email) setEmail(profile.email || '')
    } catch (err) {
      // Don't show error if we have localStorage data - just log it
      console.warn('Failed to refresh profile from server:', err)
      // Only show error if we have no data at all
      if (!currentUser) {
        setError(err.response?.data?.detail || 'Failed to load profile')
      }
    } finally {
      setRefreshing(false)
    }
  }

  const handleProfileUpdate = async (e) => {
    // Prevent form submission and page refresh
    if (e) {
      e.preventDefault()
      e.stopPropagation()
    }
    
    // Double-check: prevent any navigation
    if (e?.nativeEvent) {
      e.nativeEvent.preventDefault()
      e.nativeEvent.stopPropagation()
    }
    
    setError('')
    setSuccess('')
    setSaving(true)
    
    console.log('🔄 Starting profile update...', { username, fullName, bio })

    // Optimistic update - update UI immediately
    const user = getUser()
    const previousData = {
      username: user?.username,
      full_name: user?.full_name,
      bio: user?.bio
    }
    
    // Update localStorage immediately for instant feedback
    if (user) {
      user.username = username.trim()
      user.full_name = fullName.trim() || null
      user.bio = bio.trim() || null
      localStorage.setItem('user', JSON.stringify(user))
    }

    try {
      // Update backend (non-blocking)
      const updated = await profileService.updateProfile({
        username: username.trim(),
        full_name: fullName.trim() || null,
        bio: bio.trim() || null
      })
      
      // Sync with server response
      if (user && updated) {
        user.username = updated.username || user.username
        user.full_name = updated.full_name || user.full_name
        user.bio = updated.bio || user.bio
        localStorage.setItem('user', JSON.stringify(user))
      }
      
      console.log('✅ Profile updated successfully!', updated)
      setSuccess('Profile updated successfully!')
      setTimeout(() => setSuccess(''), 3000)
      
      // Notify profile page to refresh (non-blocking)
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('profileUpdated'))
      }, 100)
    } catch (err) {
      // Revert optimistic update on error
      if (user) {
        user.username = previousData.username
        user.full_name = previousData.full_name
        user.bio = previousData.bio
        localStorage.setItem('user', JSON.stringify(user))
        // Revert form fields
        setUsername(previousData.username || '')
        setFullName(previousData.full_name || '')
        setBio(previousData.bio || '')
      }
      
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to update profile'
      setError(errorMsg)
      console.error('Profile update error:', err)
    } finally {
      setSaving(false)
    }
  }

  const handlePictureUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    // Validate file
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB')
      return
    }

    // Preview immediately for better UX
    const reader = new FileReader()
    reader.onloadend = () => {
      setPicturePreview(reader.result)
    }
    reader.readAsDataURL(file)

    // Upload with loading indicator
    setUploadingPicture(true)
    setError('')
    setSuccess('')
    
    try {
      const updated = await profileService.uploadProfilePicture(file)
      setProfileImageUrl(updated.profile_image_url)
      setPicturePreview(updated.profile_image_url)
      
      // Update local storage
      const user = getUser()
      if (user) {
        user.profile_image_url = updated.profile_image_url
        localStorage.setItem('user', JSON.stringify(user))
      }
      
      setSuccess('Profile picture updated successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      console.error('Upload error:', err)
      setError(err.response?.data?.detail || 'Failed to upload picture')
      // Revert preview on error
      if (profileImageUrl) {
        setPicturePreview(profileImageUrl)
      } else {
        setPicturePreview('')
      }
    } finally {
      setUploadingPicture(false)
    }
  }

  const handlePasswordChange = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (newPassword !== confirmPassword) {
      setError('New passwords do not match')
      return
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    try {
      await profileService.changePassword(currentPassword, newPassword)
      setSuccess('Password changed successfully!')
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
      setShowPasswordSection(false)
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to change password')
    }
  }

  // Only show loading if we have no user data at all
  if (!currentUser) {
    return (
      <div className="profile-settings-container">
        <div className="profile-settings-card loading-state">
          <div className="loading-overlay">
            <div className="loading-content">
              <div className="spinner-large"></div>
              <p className="loading-text">Loading your profile...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="profile-settings-container">
      {saving && (
        <div className="saving-overlay">
          <div className="saving-indicator">
            <div className="spinner"></div>
            <span>Saving changes...</span>
          </div>
        </div>
      )}
      {refreshing && (
        <div className="refreshing-badge">
          <div className="spinner-tiny"></div>
          <span>Refreshing...</span>
        </div>
      )}
      <div className="profile-settings-card">
        <div className="settings-header">
          <h1>Edit Profile</h1>
          <button className="btn-back" onClick={() => navigate(-1)}>
            ← Back
          </button>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            {success}
          </div>
        )}

        {/* Profile Picture Section */}
        <div className="settings-section">
          <h2>Profile Picture</h2>
          <div className="picture-upload-section">
            <div className="picture-preview">
              {picturePreview ? (
                <img src={picturePreview} alt="Profile" />
              ) : (
                <div className="picture-placeholder">
                  {username[0]?.toUpperCase() || 'U'}
                </div>
              )}
            </div>
            <label className={`btn-upload ${uploadingPicture ? 'uploading' : ''}`}>
              {uploadingPicture ? (
                <>
                  <span className="spinner-small"></span>
                  <span>Uploading...</span>
                </>
              ) : (
                'Change Picture'
              )}
              <input
                type="file"
                accept="image/*"
                onChange={handlePictureUpload}
                disabled={uploadingPicture}
                style={{ display: 'none' }}
              />
            </label>
            <p className="help-text">JPG, PNG or GIF. Max size 5MB</p>
          </div>
        </div>

        {/* Profile Information Section */}
        <form onSubmit={handleProfileUpdate} className="settings-section" noValidate>
          <h2>Profile Information</h2>
          
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              disabled
              className="form-input disabled"
            />
            <p className="help-text">Email cannot be changed</p>
          </div>

          <div className="form-group">
            <label>Username *</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              minLength={3}
              maxLength={50}
              className="form-input"
            />
            <p className="help-text">3-50 characters, must be unique</p>
          </div>

          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              maxLength={100}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label>Bio</label>
            <textarea
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              maxLength={500}
              rows={4}
              className="form-textarea"
              placeholder="Tell us about yourself..."
            />
            <p className="help-text">{bio.length}/500 characters</p>
          </div>

          <button
            type="submit"
            className="btn-primary"
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </form>

        {/* Password Section */}
        <div className="settings-section">
          <h2>Password</h2>
          {!showPasswordSection ? (
            <button
              className="btn-secondary"
              onClick={() => setShowPasswordSection(true)}
            >
              Change Password
            </button>
          ) : (
            <form onSubmit={handlePasswordChange}>
              <div className="form-group">
                <label>Current Password</label>
                <input
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  required
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label>New Password</label>
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                  minLength={6}
                  className="form-input"
                />
                <p className="help-text">At least 6 characters</p>
              </div>

              <div className="form-group">
                <label>Confirm New Password</label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  minLength={6}
                  className="form-input"
                />
              </div>

              <div className="button-group">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => {
                    setShowPasswordSection(false)
                    setCurrentPassword('')
                    setNewPassword('')
                    setConfirmPassword('')
                    setError('')
                  }}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Change Password
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}

export default ProfileSettingsPage
