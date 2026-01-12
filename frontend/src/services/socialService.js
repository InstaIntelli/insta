/**
 * Social Features API Service
 * Follow/Unfollow, Likes, Comments, Messages
 */

import apiClient from './api'

export const socialService = {
  // Follow/Unfollow
  followUser: async (userId) => {
    const response = await apiClient.post('/api/v1/follow', { user_id: userId })
    return response.data
  },

  unfollowUser: async (userId) => {
    const response = await apiClient.post('/api/v1/unfollow', { user_id: userId })
    return response.data
  },

  getFollowers: async (userId) => {
    const response = await apiClient.get(`/api/v1/followers/${userId}`)
    return response.data
  },

  getFollowing: async (userId) => {
    const response = await apiClient.get(`/api/v1/following/${userId}`)
    return response.data
  },

  checkFollowing: async (userId) => {
    const response = await apiClient.get(`/api/v1/follow-status/${userId}`)
    return response.data
  },

  // Likes
  likePost: async (postId) => {
    const response = await apiClient.post('/api/v1/like', { post_id: postId })
    return response.data
  },

  unlikePost: async (postId) => {
    const response = await apiClient.post('/api/v1/unlike', { post_id: postId })
    return response.data
  },

  checkLikeStatus: async (postId) => {
    const response = await apiClient.get(`/api/v1/like-status/${postId}`)
    return response.data
  },

  getLikers: async (postId) => {
    const response = await apiClient.get(`/api/v1/likes/${postId}`)
    return response.data
  },

  // Comments
  addComment: async (postId, text, parentCommentId = null) => {
    const response = await apiClient.post('/api/v1/comment', {
      post_id: postId,
      text: text,
      parent_comment_id: parentCommentId
    })
    return response.data
  },

  getComments: async (postId) => {
    const response = await apiClient.get(`/api/v1/comments/${postId}`)
    return response.data
  },

  deleteComment: async (commentId) => {
    const response = await apiClient.delete(`/api/v1/comment/${commentId}`)
    return response.data
  },

  // Messages
  sendMessage: async (recipientId, text) => {
    const response = await apiClient.post('/api/v1/message', {
      recipient_id: recipientId,
      text: text
    })
    return response.data
  },

  getConversations: async () => {
    const response = await apiClient.get('/api/v1/conversations')
    return response.data
  },

  getMessages: async (userId) => {
    const response = await apiClient.get(`/api/v1/messages/${userId}`)
    return response.data
  },

  markMessagesRead: async (userId) => {
    const response = await apiClient.post(`/api/v1/messages/${userId}/read`)
    return response.data
  },

  getUnreadCount: async () => {
    const response = await apiClient.get('/api/v1/unread-count')
    return response.data
  },

  getUserStats: async (userId) => {
    const response = await apiClient.get(`/api/v1/stats/${userId}`)
    return response.data
  }
}

