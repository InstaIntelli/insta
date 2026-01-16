/**
 * Chat Page - Modern RAG Chat Interface
 * For Alisha - CUSTOMIZABLE to your liking!
 */

import React, { useState, useRef, useEffect } from 'react'
import { searchService } from '../services/searchService'
import { formatApiError } from '../services/api'
import './Assistant.css'

function ChatPage() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    const currentInput = input
    setInput('')
    setLoading(true)
    setError('')

    try {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      const response = await searchService.chatWithPosts(
        currentInput,
        user.user_id || 'default_user'
      )

      const aiMessage = {
        type: 'ai',
        content: response.answer,
        referencedPosts: response.referenced_posts || [],
        timestamp: new Date()
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (err) {
      setError(formatApiError(err))
      const errorMessage = {
        type: 'error',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const exampleQuestions = [
    "What posts did I upload about AI?",
    "Show me my travel posts",
    "Find posts with nature photos",
    "What topics do my posts cover?"
  ]

  return (
    <div className="chat-page">
      <div className="chat-hero">
        <div className="chat-hero-content">
          <div className="chat-icon-large">🤖</div>
          <h1>Chat with AI</h1>
          <p>Ask questions about your posts using natural language</p>
        </div>
      </div>

      <div className="chat-container">
        <div className="chat-messages-wrapper">
          {messages.length === 0 && (
            <div className="chat-welcome-modern">
              <div className="welcome-icon">👋</div>
              <h2>Hi! I'm your AI assistant</h2>
              <p>I can help you find and understand your posts.</p>
              <div className="example-questions">
                <p className="examples-title">Try asking:</p>
                <div className="example-grid">
                  {exampleQuestions.map((question, index) => (
                    <button
                      key={index}
                      onClick={() => setInput(question)}
                      className="example-question"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          <div className="chat-messages">
            {messages.map((message, index) => (
              <div key={index} className={`message-bubble ${message.type}`}>
                <div className="message-avatar">
                  {message.type === 'user' ? (
                    JSON.parse(localStorage.getItem('user') || '{}').avatar ? (
                      <img src={JSON.parse(localStorage.getItem('user') || '{}').avatar} alt="User" />
                    ) : '👤'
                  ) : '🤖'}
                </div>
                <div className="message-content-wrapper">
                  <div className="message-header">
                    <span className="message-sender">
                      {message.type === 'user' ? 'You' : 'AI Assistant'}
                    </span>
                    <span className="message-time">
                      {message.timestamp.toLocaleTimeString('en-US', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>
                  <div className="message-text">
                    {message.content}
                  </div>

                  {message.referencedPosts && message.referencedPosts.length > 0 && (
                    <div className="referenced-posts-modern">
                      <div className="referenced-header">
                        <span className="referenced-icon">📎</span>
                        <span>Referenced {message.referencedPosts.length} {message.referencedPosts.length === 1 ? 'post' : 'posts'}</span>
                      </div>
                      <div className="referenced-grid">
                        {message.referencedPosts.slice(0, 3).map((post, i) => (
                          <div key={i} className="referenced-post-card">
                            {post.metadata?.image_url && (
                              <img src={post.metadata.image_url} alt="Post" />
                            )}
                            <div className="referenced-post-content">
                              <p className="referenced-caption">
                                {post.metadata?.caption || post.metadata?.text || 'Post'}
                              </p>
                              {post.relevance_score && (
                                <span className="relevance-badge">
                                  {(post.relevance_score * 100).toFixed(0)}% relevant
                                </span>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-bubble ai loading-message">
                <div className="message-avatar">🤖</div>
                <div className="message-content-wrapper">
                  <div className="typing-indicator-modern">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {error && (
          <div className="error-banner-chat">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSend} className="chat-input-wrapper">
          <div className="chat-input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about your posts..."
              className="chat-input-modern"
              disabled={loading}
              autoFocus
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="send-button-modern"
              aria-label="Send message"
            >
              {loading ? (
                <span className="button-spinner-small"></span>
              ) : (
                <span>➤</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ChatPage
