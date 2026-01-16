/**
 * My Posts Page - Shows only the current user's posts
 */

import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { postService } from '../services/postService'
import { getUser } from '../utils/auth'
import { formatApiError } from '../services/api'
import PostCard from '../components/PostCard'
import RightSidebar from '../components/RightSidebar'
import './Feed.css'

function MyPostsPage() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const currentUser = getUser()

  useEffect(() => {
    if (currentUser?.user_id) {
      loadMyPosts()
    } else {
      setLoading(false)
      setError('Please log in to view your posts')
    }
  }, [currentUser?.user_id])

  const loadMyPosts = async () => {
    if (!currentUser) {
      setError('Please log in to view your posts')
      setLoading(false)
      return
    }

    try {
      setLoading(true)
      setError('') // Clear previous errors
      console.log('Loading posts for user:', currentUser.user_id)
      const data = await postService.getUserPosts(currentUser.user_id)
      console.log('Posts data received:', data)
      // Handle both response formats: {posts: [...]} or just array
      const postsArray = data?.posts || (Array.isArray(data) ? data : [])
      setPosts(postsArray)
      if (!data.posts && !data) {
        // No error, just empty state
        setError('')
      }
    } catch (err) {
      setError(formatApiError(err))
      setPosts([]) // Clear posts on error
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
            <p>Loading your posts...</p>
          </div>
        </div>
        <RightSidebar />
      </div>
    )
  }

  return (
    <div className="feed-page-container">
      <div className="feed-main-content">
        {/* Header */}
        <div className="my-posts-header">
          <h1>My Posts</h1>
          <p className="posts-count">{posts.length} {posts.length === 1 ? 'post' : 'posts'}</p>
        </div>

        {/* Error Banner - Only show if there's an actual error */}
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
            <button onClick={loadMyPosts} className="retry-btn">Retry</button>
          </div>
        )}

        {/* Posts Grid */}
        {!error && posts.length === 0 ? (
          <div className="empty-feed">
            <div className="empty-feed-icon">📸</div>
            <h2>You haven't posted anything yet</h2>
            <p>Start sharing your moments with the world!</p>
            <Link to="/upload" className="btn-primary btn-large">
              <span>➕</span> Create Your First Post
            </Link>
          </div>
        ) : !error ? (
          <div className="posts-feed">
            {posts.map((post, index) => (
              <PostCard
                key={post.post_id || index}
                post={post}
              />
            ))}
          </div>
        ) : null}
      </div>

      {/* Right Sidebar */}
      <RightSidebar />
    </div>
  )
}

export default MyPostsPage
