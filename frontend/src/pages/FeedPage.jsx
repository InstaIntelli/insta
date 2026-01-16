/**
 * Feed Page - Instagram-like Feed with Stories and Sidebar
 */

import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { postService } from '../services/postService'
import { formatApiError } from '../services/api'
import PostCard from '../components/PostCard'
import Stories from '../components/Stories'
import RightSidebar from '../components/RightSidebar'
import './Feed.css'

function FeedPage() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadFeed()
  }, [])

  const loadFeed = async () => {
    try {
      const data = await postService.getFeed()
      setPosts(data.posts || [])
    } catch (err) {
      setError(formatApiError(err))
      // Add mock posts for demo if API fails
      setPosts([
        {
          post_id: 'mock1',
          user_id: 'user1',
          username: 'demo_user',
          image_url: null,
          caption: 'This is a demo post to show the feed layout!',
          like_count: 42,
          comment_count: 5,
          created_at: new Date().toISOString()
        },
        {
          post_id: 'mock2',
          user_id: 'user2',
          username: 'another_user',
          image_url: null,
          caption: 'Another post in the feed!',
          like_count: 128,
          comment_count: 12,
          created_at: new Date().toISOString()
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="feed-page-container">
        <div className="feed-main-content">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading your feed...</p>
          </div>
        </div>
        <RightSidebar />
      </div>
    )
  }

  return (
    <div className="feed-page-container">
      <div className="feed-main-content">
        {/* Posts Feed */}
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
            <button onClick={loadFeed} className="retry-btn">Retry</button>
          </div>
        )}

        {posts.length === 0 ? (
          <div className="empty-feed">
            <div className="empty-feed-icon">📸</div>
            <h2>Your feed is empty</h2>
            <p>Start sharing your moments with the world!</p>
            <Link to="/upload" className="btn-primary btn-large">
              <span>➕</span> Create Your First Post
            </Link>
          </div>
        ) : (
          <div className="posts-feed">
            {posts.map((post, index) => (
              <PostCard
                key={post.post_id || index}
                post={post}
              />
            ))}
          </div>
        )}
      </div>

      {/* Right Sidebar */}
      <RightSidebar />
    </div>
  )
}

export default FeedPage

