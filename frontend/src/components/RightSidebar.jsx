/**
 * Right Sidebar Component - User profile and suggestions
 */

import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getUser } from '../utils/auth'
import { recommendationService } from '../services/recommendationService'
import './RightSidebar.css'

function RightSidebar() {
  const navigate = useNavigate()
  const currentUser = getUser()
  const [suggestions, setSuggestions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSuggestions()
  }, [])

  const loadSuggestions = async () => {
    try {
      // Try to get recommendations from recommendation service
      const data = await recommendationService.getUserRecommendations(5)
      setSuggestions(data.users || data || [])
    } catch (err) {
      console.error('Error loading suggestions:', err)
      // Mock suggestions if API fails
      setSuggestions([
        { user_id: '1', username: 'fawad_mughal', full_name: 'Fawad Mughal', followed_by: 'talha.ahmed33' },
        { user_id: '2', username: 'yashfa_arshad', full_name: 'Yashfa Arshad', followed_by: 'fatima_irshad.12' },
        { user_id: '3', username: 'fatima_user', full_name: 'فاطمہ', followed_by: 'aqsami15' },
        { user_id: '4', username: 'amima_khan', full_name: 'Amima Khan', followed_by: 'hassaan633', more_followers: 3 },
        { user_id: '5', username: 'aree_banoor15', full_name: 'Aree Banoor', followed_by: 'abeeha_shahh' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleFollow = async (userId) => {
    try {
      // TODO: Implement follow functionality
      console.log('Follow user:', userId)
    } catch (err) {
      console.error('Error following user:', err)
    }
  }

  const handleSwitchAccount = () => {
    // Clear session and redirect to login
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  if (!currentUser) return null

  return (
    <aside className="right-sidebar">
      {/* Current User Profile */}
      <div className="sidebar-user-profile">
        <Link to={`/profile/${currentUser.user_id}`} className="user-profile-link">
          <div className="user-profile-avatar">
            {currentUser.profile_image_url ? (
              <img src={currentUser.profile_image_url} alt={currentUser.username} />
            ) : (
              <div className="user-profile-avatar-placeholder">
                {currentUser.username?.[0]?.toUpperCase() || 'U'}
              </div>
            )}
          </div>
          <div className="user-profile-info">
            <div className="user-profile-username">{currentUser.username}</div>
            <div className="user-profile-name">{currentUser.full_name || 'InstaIntelli User'}</div>
          </div>
        </Link>
        <button 
          className="switch-btn" 
          onClick={handleSwitchAccount}
          type="button"
        >
          Switch
        </button>
      </div>

      {/* Suggestions */}
      <div className="suggestions-section">
        <div className="suggestions-header">
          <span className="suggestions-title">Suggested for you</span>
          <Link to="/recommendations" className="see-all-link">See All</Link>
        </div>

        {loading ? (
          <div className="suggestions-loading">Loading...</div>
        ) : (
          <div className="suggestions-list">
            {suggestions.map((user) => (
              <div key={user.user_id} className="suggestion-item">
                <Link to={`/profile/${user.user_id}`} className="suggestion-user">
                  <div className="suggestion-avatar">
                    {user.profile_image_url ? (
                      <img src={user.profile_image_url} alt={user.username} />
                    ) : (
                      <div className="suggestion-avatar-placeholder">
                        {user.username?.[0]?.toUpperCase() || 'U'}
                      </div>
                    )}
                  </div>
                  <div className="suggestion-info">
                    <div className="suggestion-username">{user.username}</div>
                    <div className="suggestion-followed-by">
                      Followed by {user.followed_by || 'someone'} + {user.more_followers || '3'}
                    </div>
                  </div>
                </Link>
                <button 
                  className="follow-btn"
                  onClick={() => handleFollow(user.user_id)}
                >
                  Follow
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer Links */}
      <div className="sidebar-footer">
        <div className="footer-links">
          <a href="#" className="footer-link">About</a>
          <a href="#" className="footer-link">Help</a>
          <a href="#" className="footer-link">Press</a>
          <a href="#" className="footer-link">API</a>
          <a href="#" className="footer-link">Jobs</a>
          <a href="#" className="footer-link">Privacy</a>
          <a href="#" className="footer-link">Terms</a>
          <a href="#" className="footer-link">Locations</a>
          <a href="#" className="footer-link">Language</a>
          <a href="#" className="footer-link">Meta Verified</a>
        </div>
        <div className="footer-copyright">
          © 2026 INSTAINTELLI
        </div>
      </div>
    </aside>
  )
}

export default RightSidebar
