/**
 * Feed Page - Instagram-like Feed
 */

import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { postService } from '../services/postService'
import PostCard from '../components/PostCard'
import './Feed.css'

function FeedPage() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  useEffect(() => {
    loadFeed()
  }, [])

  const loadFeed = async () => {
    try {
      // Try to get user's posts first
      if (user.user_id) {
        try {
          const userPosts = await postService.getUserPosts(user.user_id)
          setPosts(userPosts.posts || userPosts || [])
        } catch (err) {
          // If user posts endpoint fails, try feed
          const data = await postService.getFeed()
          setPosts(data.posts || [])
        }
      } else {
        const data = await postService.getFeed()
        setPosts(data.posts || [])
      }
    } catch (err) {
      // If all fails, show empty state
      setPosts([])
      console.log('Feed loading:', err.message || 'No posts available')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="feed-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading your feed...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="feed-container">
      <div className="feed-wrapper">
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
                key={post.post_id || post._id || index}
                post={post}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default FeedPage

