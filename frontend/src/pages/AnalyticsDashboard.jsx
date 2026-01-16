/**
 * Analytics Dashboard
 * Comprehensive analytics and insights for users
 */

import React, { useState, useEffect } from 'react'
import { analyticsService } from '../services/analyticsService'
import { recommendationService } from '../services/recommendationService'
import './AnalyticsDashboard.css'

function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState(null)
  const [recommendations, setRecommendations] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [analyticsData, userRecs] = await Promise.all([
        analyticsService.getUserAnalytics(),
        recommendationService.getUserRecommendations(5)
      ])
      setAnalytics(analyticsData)
      setRecommendations(userRecs)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="analytics-container">
        <div className="error-container">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
          <button onClick={loadData} className="btn-primary">Try Again</button>
        </div>
      </div>
    )
  }

  if (!analytics) {
    return (
      <div className="analytics-container">
        <div className="empty-state">
          <h2>No analytics data available</h2>
          <p>Start posting to see your analytics!</p>
        </div>
      </div>
    )
  }

  const overview = analytics.overview || {}
  const engagementTimeline = analytics.engagement_timeline || {}
  const topPosts = analytics.top_posts || []
  const bestTimes = analytics.best_posting_times || {}

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h1>Analytics Dashboard</h1>
        <p className="subtitle">Real-time performance metrics & AI insights</p>
      </div>

      {/* Modern Tabs */}
      <div className="analytics-tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'engagement' ? 'active' : ''}`}
          onClick={() => setActiveTab('engagement')}
        >
          Engagement
        </button>
        <button
          className={`tab ${activeTab === 'top-posts' ? 'active' : ''}`}
          onClick={() => setActiveTab('top-posts')}
        >
          Top Posts
        </button>
        <button
          className={`tab ${activeTab === 'insights' ? 'active' : ''}`}
          onClick={() => setActiveTab('insights')}
        >
          Insights
        </button>
      </div>

      {/* Main Content Area */}
      <div className="analytics-main-content">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="analytics-content animate-fade-in">
            <div className="metrics-grid">
              <div className="metric-card" title="Total posts shared">
                <div className="metric-icon">📸</div>
                <div className="metric-value">{overview.total_posts || 0}</div>
                <div className="metric-label">Total Posts</div>
              </div>
              <div className="metric-card" title="Total likes received">
                <div className="metric-icon">❤️</div>
                <div className="metric-value">{overview.total_likes || 0}</div>
                <div className="metric-label">Total Likes</div>
              </div>
              <div className="metric-card" title="Total comments received">
                <div className="metric-icon">💬</div>
                <div className="metric-value">{overview.total_comments || 0}</div>
                <div className="metric-label">Comments</div>
              </div>
              <div className="metric-card" title="Your follower count">
                <div className="metric-icon">👥</div>
                <div className="metric-value">{overview.followers || 0}</div>
                <div className="metric-label">Followers</div>
              </div>
              <div className="metric-card" title="Engagement per interaction">
                <div className="metric-icon">📈</div>
                <div className="metric-value">{overview.engagement_rate || 0}%</div>
                <div className="metric-label">Engagement</div>
              </div>
              <div className="metric-card" title="Average likes per post">
                <div className="metric-icon">✨</div>
                <div className="metric-value">{overview.avg_likes_per_post || 0}</div>
                <div className="metric-label">Avg Likes</div>
              </div>
            </div>

            {recommendations && recommendations.users && recommendations.users.length > 0 && (
              <div className="recommendations-section card-glass">
                <h2><span>👥</span> People You May Know</h2>
                <div className="recommendations-list">
                  {recommendations.users.map((user) => (
                    <div key={user.user_id} className="recommendation-item">
                      <div className="rec-avatar">
                        {user.username?.[0]?.toUpperCase() || 'U'}
                      </div>
                      <div className="rec-info">
                        <div className="rec-username">@{user.username || user.user_id}</div>
                        <div className="rec-reason">{user.reason || 'Suggested for you'}</div>
                      </div>
                      <button className="btn-follow-mini">Follow</button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Engagement Tab */}
        {activeTab === 'engagement' && (
          <div className="analytics-content animate-fade-in">
            <div className="engagement-chart card-glass">
              <h2><span>📈</span> Engagement Timeline</h2>
              <div className="chart-container">
                {Object.keys(engagementTimeline).length > 0 ? (
                  <div className="timeline-bars">
                    {Object.entries(engagementTimeline).map(([date, data]) => {
                      const totalInteraction = data.likes + data.comments;
                      const maxEngagement = Math.max(
                        ...Object.values(engagementTimeline).map(d => d.likes + d.comments),
                        1 // Avoid division by zero
                      );
                      const height = (totalInteraction / maxEngagement) * 100;

                      return (
                        <div key={date} className="timeline-bar">
                          <div
                            className="bar-fill"
                            style={{ height: `${Math.max(height, 5)}%` }}
                            title={`${data.likes} likes, ${data.comments} comments`}
                          ></div>
                          <div className="bar-label">
                            {new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                ) : (
                  <div className="no-data">No activity detected in the last 30 days</div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Top Posts Tab */}
        {activeTab === 'top-posts' && (
          <div className="analytics-content animate-fade-in">
            <h2><span>🏆</span> Top Performing Content</h2>
            {topPosts.length > 0 ? (
              <div className="top-posts-grid">
                {topPosts.map((post, index) => (
                  <div key={post.post_id} className="top-post-card">
                    <div className="post-rank">#{index + 1}</div>
                    {post.image_url ? (
                      <img src={post.image_url} alt={post.caption || 'Post'} className="post-thumbnail" />
                    ) : (
                      <div className="post-thumbnail-placeholder">No Image</div>
                    )}
                    <div className="post-metrics">
                      <div className="metric-item">
                        <span className="icon">❤️</span>
                        <span>{post.likes || 0}</span>
                      </div>
                      <div className="metric-item">
                        <span className="icon">💬</span>
                        <span>{post.comments || 0}</span>
                      </div>
                      <div className="metric-item highlight">
                        <span className="icon">📊</span>
                        <span>{post.engagement_score || 0}%</span>
                      </div>
                    </div>
                    {post.caption && (
                      <div className="post-caption-preview">
                        {post.caption.length > 60
                          ? post.caption.substring(0, 60) + '...'
                          : post.caption}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data card-glass">No posts published yet</div>
            )}
          </div>
        )}

        {/* Insights Tab */}
        {activeTab === 'insights' && (
          <div className="analytics-content animate-fade-in">
            <h2><span>💡</span> AI Insights & Strategy</h2>
            <div className="insights-list">
              <div className="insight-card">
                <div className="insight-icon">⏰</div>
                <div className="insight-content">
                  <h3>Optimal Posting Schedule</h3>
                  <p>{bestTimes.recommendation || 'Analyzing your engagement patterns to find the best window...'}</p>
                  {bestTimes.best_hours && bestTimes.best_hours.length > 0 && (
                    <div className="best-hours">
                      {bestTimes.best_hours.map((hour) => (
                        <span key={hour} className="hour-badge">{hour}:00</span>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              <div className="insight-card">
                <div className="insight-icon">📈</div>
                <div className="insight-content">
                  <h3>Engagement Depth</h3>
                  <p>
                    Your community interactions average {overview.avg_likes_per_post || 0} likes and{' '}
                    {overview.avg_comments_per_post || 0} comments per post.
                  </p>
                  {overview.engagement_rate > 0 && (
                    <div className="engagement-status">
                      Current Reach: <strong>{overview.engagement_rate}%</strong>
                    </div>
                  )}
                </div>
              </div>

              <div className="insight-card">
                <div className="insight-icon">🚀</div>
                <div className="insight-content">
                  <h3>Growth Accelerators</h3>
                  <ul className="tips-list">
                    <li>Maintain consistency: Post at least 3 times weekly</li>
                    <li>Community First: Respond to comments within the first hour</li>
                    <li>Context Matters: Use semantic tags discovered in your search</li>
                    <li>Visual Quality: High-contrast images tend to perform 20% better</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AnalyticsDashboard

