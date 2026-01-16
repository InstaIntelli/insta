/**
 * Post Card Component
 * Modern, Instagram-like post display with social features
 */

import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { socialService } from '../services/socialService'
import { getUser } from '../utils/auth'
import CommentSection from './CommentSection'
import './PostCard.css'

function PostCard({ post }) {
  const [imageLoaded, setImageLoaded] = useState(false)
  const [imageError, setImageError] = useState(false)
  const [liked, setLiked] = useState(post.liked || false)
  const [likeCount, setLikeCount] = useState(post.like_count || 0)
  const [showComments, setShowComments] = useState(false)
  const [commentCount, setCommentCount] = useState(post.comment_count || 0)
  const [isLiking, setIsLiking] = useState(false)
  const currentUser = getUser()

  // Check like status on mount
  useEffect(() => {
    if (currentUser && post.post_id) {
      checkLikeStatus()
    }
  }, [post.post_id, currentUser])

  const checkLikeStatus = async () => {
    try {
      const response = await socialService.checkLikeStatus?.(post.post_id) ||
        { liked: post.liked || false }
      setLiked(response.liked || false)
    } catch (err) {
      console.error('Error checking like status:', err)
    }
  }

  const handleLike = async () => {
    if (!currentUser) {
      alert('Please log in to like posts')
      return
    }

    if (isLiking) return
    setIsLiking(true)

    try {
      if (liked) {
        await socialService.unlikePost(post.post_id)
        setLiked(false)
        setLikeCount(prev => Math.max(0, prev - 1))
      } else {
        await socialService.likePost(post.post_id)
        setLiked(true)
        setLikeCount(prev => prev + 1)
      }
    } catch (err) {
      console.error('Error liking post:', err)
      alert(err.response?.data?.detail || 'Failed to like post')
    } finally {
      setIsLiking(false)
    }
  }

  const handleCommentClick = () => {
    if (!currentUser) {
      alert('Please log in to comment')
      return
    }
    setShowComments(!showComments)
  }

  const handleCommentAdded = () => {
    setCommentCount(prev => prev + 1)
  }

  const handleCommentDeleted = () => {
    setCommentCount(prev => Math.max(0, prev - 1))
  }

  // Double-tap timer
  let lastTap = 0
  const handleDoubleTap = (e) => {
    const now = Date.now()
    if (now - lastTap < 300) {
      if (!liked) handleLike()
      // Show heart animation on image
      const heart = document.createElement('div')
      heart.className = 'center-heart-anim'
      heart.innerHTML = '❤️'
      e.currentTarget.appendChild(heart)
      setTimeout(() => heart.remove(), 1000)
    }
    lastTap = now
  }

  return (
    <article className="post-card fade-in">
      {/* Post Header */}
      <div className="post-header">
        <Link to={`/profile/${post.user_id}`} className="post-user" aria-label={`View profile of ${post.username || post.user_id}`}>
          <div className="user-avatar">
            {post.user_avatar ? (
              <img
                src={post.user_avatar}
                alt={post.username}
                onError={(e) => {
                  e.target.style.display = 'none'
                  const placeholder = e.target.nextElementSibling
                  if (placeholder) placeholder.style.display = 'flex'
                }}
              />
            ) : null}
            <div
              className="avatar-placeholder"
              style={{ display: post.user_avatar ? 'none' : 'flex' }}
            >
              {post.username?.[0]?.toUpperCase() || 'U'}
            </div>
          </div>
          <span className="username">@{post.username || post.user_id}</span>
        </Link>
        <button className="post-menu" aria-label="More options">
          <span>⋯</span>
        </button>
      </div>

      {/* Post Image */}
      {post.image_url && (
        <div
          className="post-image-container"
          onClick={handleDoubleTap}
          style={{ cursor: 'pointer' }}
        >
          {!imageLoaded && !imageError && (
            <div className="image-skeleton">
              <div className="skeleton-shimmer"></div>
            </div>
          )}
          {imageError ? (
            <div className="image-error">
              <span>📷</span>
              <p>Image not available</p>
            </div>
          ) : (
            <img
              src={post.image_url}
              alt={post.caption || 'Post'}
              className={`post-image ${imageLoaded ? 'loaded' : ''}`}
              onLoad={() => setImageLoaded(true)}
              onError={() => {
                setImageError(true)
                setImageLoaded(true)
              }}
            />
          )}
        </div>
      )}

      {/* Post Actions */}
      <div className="post-actions">
        <button
          className={`action-btn like-btn ${liked ? 'liked' : ''}`}
          aria-label="Like"
          onClick={handleLike}
          disabled={isLiking}
        >
          <span>{liked ? '❤️' : '🤍'}</span>
        </button>
        <button
          className="action-btn comment-btn"
          aria-label="Comment"
          onClick={handleCommentClick}
        >
          <span>💬</span>
        </button>
        <button className="action-btn share-btn" aria-label="Share">
          <span>📤</span>
        </button>
        <button className="action-btn save-btn" aria-label="Save">
          <span>🔖</span>
        </button>
      </div>

      {/* Post Content */}
      <div className="post-content">
        {likeCount > 0 && (
          <div className="post-likes">
            <strong>{likeCount}</strong> {likeCount === 1 ? 'like' : 'likes'}
          </div>
        )}

        {post.caption && (
          <div className="post-caption">
            <Link to={`/profile/${post.user_id}`} className="caption-username">
              @{post.username || post.user_id}
            </Link>
            <span className="caption-text">{post.caption}</span>
          </div>
        )}

        {post.text && post.text !== post.caption && (
          <div className="post-text">
            {post.text}
          </div>
        )}

        {Array.isArray(post.topics) && post.topics.length > 0 && (
          <div className="post-topics">
            {post.topics.map((topic, index) => (
              <span key={index} className="topic-tag">
                #{topic}
              </span>
            ))}
          </div>
        )}

        {post.created_at && (
          <div className="post-time">
            {(() => {
              try {
                return new Date(post.created_at).toLocaleDateString('en-US', {
                  month: 'short',
                  day: 'numeric'
                });
              } catch (e) {
                return '';
              }
            })()}
          </div>
        )}

        {/* View Comments Link */}
        {commentCount > 0 && !showComments && (
          <button
            className="view-comments-btn"
            onClick={handleCommentClick}
          >
            View all {commentCount} {commentCount === 1 ? 'comment' : 'comments'}
          </button>
        )}
      </div>

      {/* Comment Section */}
      {showComments && (
        <CommentSection
          postId={post.post_id}
          onCommentAdded={handleCommentAdded}
          onCommentDeleted={handleCommentDeleted}
        />
      )}
    </article>
  )
}

export default PostCard


