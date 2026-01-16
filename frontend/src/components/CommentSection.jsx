/**
 * Comment Section Component
 * Displays comments and allows adding new comments
 */

import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { socialService } from '../services/socialService'
import { getUser } from '../utils/auth'
import './CommentSection.css'

function CommentSection({ postId, onCommentAdded, onCommentDeleted }) {
  const [comments, setComments] = useState([])
  const [loading, setLoading] = useState(true)
  const [newComment, setNewComment] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [replyToId, setReplyToId] = useState(null)
  const [replyingToUsername, setReplyingToUsername] = useState('')
  const currentUser = getUser()

  useEffect(() => {
    loadComments()
  }, [postId])

  const loadComments = async () => {
    try {
      setLoading(true)
      const response = await socialService.getComments(postId)
      setComments(response.comments || [])
    } catch (err) {
      console.error('Error loading comments:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!newComment.trim() || isSubmitting) return

    setIsSubmitting(true)
    try {
      await socialService.addComment(postId, newComment.trim(), replyToId)
      setNewComment('')
      setReplyToId(null)
      setReplyingToUsername('')
      await loadComments() // Reload comments
      if (onCommentAdded) onCommentAdded()
    } catch (err) {
      console.error('Error adding comment:', err)
      alert(err.response?.data?.detail || 'Failed to add comment')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async (commentId) => {
    if (!window.confirm('Delete this comment?')) return

    try {
      await socialService.deleteComment(commentId)
      await loadComments() // Reload comments
      if (onCommentDeleted) onCommentDeleted()
    } catch (err) {
      console.error('Error deleting comment:', err)
      alert(err.response?.data?.detail || 'Failed to delete comment')
    }
  }

  const handleReplyClick = (commentId, username) => {
    setReplyToId(commentId)
    setReplyingToUsername(username)
    // Scroll to input if needed, or focus
    const input = document.querySelector('.comment-input')
    if (input) input.focus()
  }

  const cancelReply = () => {
    setReplyToId(null)
    setReplyingToUsername('')
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return 'just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  return (
    <div className="comment-section">
      {loading ? (
        <div className="comment-loading">Loading comments...</div>
      ) : (
        <>
          {/* Comments List */}
          <div className="comments-list">
            {comments.length === 0 ? (
              <div className="no-comments">No comments yet. Be the first to comment!</div>
            ) : (
              comments.map((comment) => (
                <div key={comment.comment_id} className="comment-item">
                  <div className="comment-header">
                    <span className="comment-username">@{comment.username || comment.user_id}</span>
                    <span className="comment-time">{formatDate(comment.created_at)}</span>
                  </div>
                  <div className="comment-text">{comment.text}</div>
                  <div className="comment-actions">
                    <button
                      className="comment-action-btn reply-btn"
                      onClick={() => handleReplyClick(comment.comment_id, comment.username || comment.user_id)}
                    >
                      Reply
                    </button>
                    {currentUser && currentUser.user_id === comment.user_id && (
                      <button
                        className="comment-action-btn delete-comment-btn"
                        onClick={() => handleDelete(comment.comment_id)}
                        aria-label="Delete comment"
                      >
                        Delete
                      </button>
                    )}
                  </div>
                  {/* Replies */}
                  {comment.replies && comment.replies.length > 0 && (
                    <div className="comment-replies">
                      {comment.replies.map((reply) => (
                        <div key={reply.comment_id} className="comment-item reply-item">
                          <div className="comment-header">
                            <span className="comment-username">@{reply.username || reply.user_id}</span>
                            <span className="comment-time">{formatDate(reply.created_at)}</span>
                          </div>
                          <div className="comment-text">{reply.text}</div>
                          <div className="comment-actions">
                            <button
                              className="comment-action-btn reply-btn"
                              onClick={() => handleReplyClick(comment.comment_id, reply.username || reply.user_id)}
                            >
                              Reply
                            </button>
                            {currentUser && currentUser.user_id === reply.user_id && (
                              <button
                                className="comment-action-btn delete-comment-btn"
                                onClick={() => handleDelete(reply.comment_id)}
                                aria-label="Delete reply"
                              >
                                Delete
                              </button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          {/* Add Comment Form */}
          {currentUser ? (
            <div className="comment-form-container">
              {replyToId && (
                <div className="reply-indicator">
                  <span>Replying to <strong>@{replyingToUsername}</strong></span>
                  <button className="cancel-reply-btn" onClick={cancelReply}>Cancel</button>
                </div>
              )}
              <form className="comment-form" onSubmit={handleSubmit}>
                <input
                  type="text"
                  className="comment-input"
                  placeholder={replyToId ? `Reply to @${replyingToUsername}...` : "Add a comment..."}
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  disabled={isSubmitting}
                  maxLength={500}
                />
                <button
                  type="submit"
                  className="comment-submit-btn"
                  disabled={!newComment.trim() || isSubmitting}
                >
                  {isSubmitting ? 'Posting...' : 'Post'}
                </button>
              </form>
            </div>
          ) : (
            <div className="comment-login-prompt">
              <Link to="/login">Log in</Link> to comment
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default CommentSection

