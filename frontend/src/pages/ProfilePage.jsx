/**
 * Profile Page
 * For Hassan - User Profiles
 */

import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { userService } from '../services/userService'
import './Profile.css'

function ProfilePage() {
  const { userId } = useParams()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadUser()
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
    </div>
  )
}

export default ProfilePage


