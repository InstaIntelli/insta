import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../services/api'
import { getUser, logout } from '../utils/auth'
import './Profile.css'

const Profile = () => {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editMode, setEditMode] = useState(false)
  const [formData, setFormData] = useState({ full_name: '', bio: '' })
  const [uploading, setUploading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const response = await apiClient.get('/api/v1/profile/me')
      setProfile(response.data)
      setFormData({ full_name: response.data.full_name || '', bio: response.data.bio || '' })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load profile')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleUpdate = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const response = await apiClient.put('/api/v1/profile/update', formData)
      setProfile(response.data)
      setEditMode(false)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB')
      return
    }
    setUploading(true)
    setError('')
    try {
      const formData = new FormData()
      formData.append('file', file)
      const response = await apiClient.post('/api/v1/profile/upload_picture', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setProfile(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload picture')
    } finally {
      setUploading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const user = getUser()

  if (loading && !profile) {
    return <div className="profile-container">Loading...</div>
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>My Profile</h1>
        <button onClick={handleLogout} className="btn-secondary">Logout</button>
      </div>
      {error && <div className="error-message">{error}</div>}
      <div className="profile-card">
        <div className="profile-picture-section">
          <div className="profile-picture">
            {profile?.profile_picture_url ? (
              <img src={profile.profile_picture_url} alt="Profile" />
            ) : (
              <div className="profile-placeholder">{user?.username?.[0]?.toUpperCase() || 'U'}</div>
            )}
          </div>
          <label htmlFor="file-upload" className="btn-upload">
            {uploading ? 'Uploading...' : 'Change Picture'}
          </label>
          <input id="file-upload" type="file" accept="image/*" onChange={handleFileUpload} style={{ display: 'none' }} disabled={uploading} />
        </div>
        <div className="profile-info">
          {!editMode ? (
            <>
              <div className="info-row">
                <label>Username:</label>
                <span>{user?.username || 'N/A'}</span>
              </div>
              <div className="info-row">
                <label>Email:</label>
                <span>{user?.email || 'N/A'}</span>
              </div>
              <div className="info-row">
                <label>Full Name:</label>
                <span>{profile?.full_name || 'Not set'}</span>
              </div>
              <div className="info-row">
                <label>Bio:</label>
                <span>{profile?.bio || 'No bio yet'}</span>
              </div>
              <button onClick={() => setEditMode(true)} className="btn-primary">Edit Profile</button>
            </>
          ) : (
            <form onSubmit={handleUpdate}>
              <div className="form-group">
                <label htmlFor="full_name">Full Name</label>
                <input type="text" id="full_name" name="full_name" value={formData.full_name} onChange={handleChange} placeholder="Enter your full name" />
              </div>
              <div className="form-group">
                <label htmlFor="bio">Bio</label>
                <textarea id="bio" name="bio" value={formData.bio} onChange={handleChange} placeholder="Tell us about yourself" rows="4" />
              </div>
              <div className="form-actions">
                <button type="submit" className="btn-primary" disabled={loading}>{loading ? 'Saving...' : 'Save Changes'}</button>
                <button type="button" onClick={() => { setEditMode(false); setFormData({ full_name: profile?.full_name || '', bio: profile?.bio || '' }) }} className="btn-secondary">Cancel</button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}

export default Profile

