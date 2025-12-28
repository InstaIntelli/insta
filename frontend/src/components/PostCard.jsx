/**
 * Post Card Component
 * Modern, Instagram-like post display
 */

import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import './PostCard.css'

function PostCard({ post }) {
  const [imageLoaded, setImageLoaded] = useState(false)
  const [imageError, setImageError] = useState(false)

  return (
    <article className="post-card fade-in">
      {/* Post Header */}
      <div className="post-header">
        <Link to={`/profile/${post.user_id}`} className="post-user">
          <div className="user-avatar">
            {post.user_avatar ? (
              <img src={post.user_avatar} alt={post.username} />
            ) : (
              <div className="avatar-placeholder">
                {post.username?.[0]?.toUpperCase() || 'U'}
              </div>
            )}
          </div>
          <span className="username">@{post.username || post.user_id}</span>
        </Link>
        <button className="post-menu" aria-label="More options">
          <span>⋯</span>
        </button>
      </div>

      {/* Post Image */}
      {post.image_url && (
        <div className="post-image-container">
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
        <button className="action-btn like-btn" aria-label="Like">
          <span>❤️</span>
        </button>
        <button className="action-btn comment-btn" aria-label="Comment">
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
        {post.likes_count > 0 && (
          <div className="post-likes">
            <strong>{post.likes_count}</strong> likes
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

        {post.topics && post.topics.length > 0 && (
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
            {new Date(post.created_at).toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric'
            })}
          </div>
        )}
      </div>
    </article>
  )
}

export default PostCard


