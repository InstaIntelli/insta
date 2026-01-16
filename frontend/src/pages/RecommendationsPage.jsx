/**
 * Recommendations Page
 * Shows trending posts, user recommendations, and personalized content
 */

import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { recommendationService } from '../services/recommendationService'
import { socialService } from '../services/socialService'
import PostCard from '../components/PostCard'
import './RecommendationsPage.css'

function RecommendationsPage() {
  const [trending, setTrending] = useState([])
  const [userRecs, setUserRecs] = useState([])
  const [contentRecs, setContentRecs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('trending')

  useEffect(() => {
    loadRecommendations()
  }, [])

  const loadRecommendations = async () => {
    try {
      setLoading(true)
      const [trendingData, userData, contentData] = await Promise.all([
        recommendationService.getTrending(20),
        recommendationService.getUserRecommendations(10),
        recommendationService.getContentRecommendations(20)
      ])
      setTrending(trendingData.posts || [])
      setUserRecs(userData.users || [])
      setContentRecs(contentData.posts || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load recommendations')
    } finally {
      setLoading(false)
    }
  }

  const handleFollow = async (userId) => {
    try {
      await socialService.followUser(userId)
      // Update the user in the list
      setUserRecs(prev => prev.map(user =>
        user.user_id === userId ? { ...user, following: true } : user
      ))
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to follow user')
    }
  }

  if (loading) {
    return (
      <div className="recommendations-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading recommendations...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="recommendations-container">
        <div className="error-container">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
          <button onClick={loadRecommendations} className="btn-primary">Try Again</button>
        </div>
      </div>
    )
  }

  return (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <h1><span>✨</span> Discover</h1>
        <p className="subtitle">AI-powered recommendations tailored for you</p>
      </div>

      {/* Tabs */}
      <div className="recommendations-tabs">
        <button
          className={`tab ${activeTab === 'trending' ? 'active' : ''}`}
          onClick={() => setActiveTab('trending')}
        >
          🔥 Trending
        </button>
        <button
          className={`tab ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          👥 People
        </button>
        <button
          className={`tab ${activeTab === 'content' ? 'active' : ''}`}
          onClick={() => setActiveTab('content')}
        >
          ✨ For You
        </button>
      </div>

      {/* Trending Tab */}
      {activeTab === 'trending' && (
        <div className="recommendations-content">
          <div className="section-header">
            <h2>🔥 Trending Posts</h2>
            <p>Most engaging content right now</p>
          </div>
          {trending.length > 0 ? (
            <div className="posts-grid">
              {trending.map((post) => (
                <PostCard key={post.post_id} post={post} />
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No trending posts at the moment</p>
            </div>
          )}
        </div>
      )}

      {/* Users Tab */}
      {activeTab === 'users' && (
        <div className="recommendations-content">
          <div className="section-header">
            <h2>👥 People You May Know</h2>
            <p>Based on who you follow</p>
          </div>
          {userRecs.length > 0 ? (
            <div className="users-grid">
              {userRecs.map((user) => (
                <div key={user.user_id} className="user-card">
                  <Link to={`/profile/${user.user_id}`} className="user-link">
                    <div className="user-avatar-large">
                      {user.username?.[0]?.toUpperCase() || 'U'}
                    </div>
                    <div className="user-info">
                      <div className="user-username">@{user.username || user.user_id}</div>
                      {user.reason && (
                        <div className="user-reason">{user.reason}</div>
                      )}
                      <div className="user-stats">
                        {user.follower_count !== undefined ? `${user.follower_count} followers` : 'Popular user'}
                      </div>
                    </div>
                  </Link>
                  <button
                    className="follow-btn-small"
                    onClick={() => handleFollow(user.user_id)}
                    disabled={user.following}
                  >
                    {user.following ? 'Following' : 'Follow'}
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No user recommendations available</p>
            </div>
          )}
        </div>
      )}

      {/* Content Tab */}
      {activeTab === 'content' && (
        <div className="recommendations-content">
          <div className="section-header">
            <h2>✨ Recommended For You</h2>
            <p>Based on your interests and activity</p>
          </div>
          {contentRecs.length > 0 ? (
            <div className="posts-grid">
              {contentRecs.map((post) => (
                <PostCard key={post.post_id} post={post} />
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No content recommendations available</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RecommendationsPage

