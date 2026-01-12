import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import InstagramIcon from '../components/InstagramIcon'
import './LandingPage.css'

function LandingPage() {
  const [activeSlide, setActiveSlide] = useState(0)
  const [likeCount, setLikeCount] = useState(0)
  const [isLiked, setIsLiked] = useState(false)
  const navigate = useNavigate()

  const screenshots = [
    { 
      id: 1, 
      caption: "Share your moments", 
      description: "Post photos and videos instantly",
      likes: 1247,
      comments: 89
    },
    { 
      id: 2, 
      caption: "AI-powered captions", 
      description: "Intelligent caption generation",
      likes: 2156,
      comments: 142
    },
    { 
      id: 3, 
      caption: "Discover with semantic search", 
      description: "Find posts by meaning, not keywords",
      likes: 3421,
      comments: 203
    },
    { 
      id: 4, 
      caption: "Chat with your memories", 
      description: "RAG-powered conversation with your posts",
      likes: 1890,
      comments: 156
    }
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveSlide((prev) => {
        const next = (prev + 1) % screenshots.length
        setIsLiked(false)
        setLikeCount(screenshots[next].likes)
        return next
      })
    }, 4000)
    return () => clearInterval(interval)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    setLikeCount(screenshots[activeSlide].likes)
    setIsLiked(false)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeSlide])

  const handleLike = () => {
    if (!isLiked) {
      setIsLiked(true)
      setLikeCount(prev => prev + 1)
    } else {
      setIsLiked(false)
      setLikeCount(prev => prev - 1)
    }
  }

  return (
    <div className="landing-page">
      <div className="landing-container">
        {/* Left Side - Phone Mockup with Carousel */}
        <div className="phone-mockup-section">
          <div className="phone-mockup">
            <div className="phone-frame">
              <div className="phone-notch"></div>
              <div className="phone-screen">
                {screenshots.map((screenshot, index) => (
                  <div
                    key={screenshot.id}
                    className={`screenshot-slide ${index === activeSlide ? 'active' : ''}`}
                  >
                    <div className="mock-content">
                      <div className="mock-header">
                        <div className="mock-logo-container">
                          <InstagramIcon size={28} className="header-icon" />
                          <span className="mock-logo">InstaIntelli</span>
                        </div>
                        <div className="mock-icons">
                          <span className="mock-icon">📤</span>
                        </div>
                      </div>
                      <div className="mock-feed">
                        <div className="mock-post-container">
                          <div className="mock-post-image">
                            <div className="post-gradient"></div>
                            <div className="post-overlay">
                              <InstagramIcon size={60} className="post-icon" />
                            </div>
                          </div>
                          <div className="mock-post-actions">
                            <button 
                              className={`action-btn like-btn ${isLiked && index === activeSlide ? 'liked' : ''}`}
                              onClick={handleLike}
                            >
                              <span className="heart-icon">❤️</span>
                            </button>
                            <button className="action-btn">
                              <span>💬</span>
                            </button>
                            <button className="action-btn">
                              <span>📤</span>
                            </button>
                            <button className="action-btn save-btn">
                              <span>🔖</span>
                            </button>
                          </div>
                          <div className="mock-post-stats">
                            <span className="likes-count">{likeCount.toLocaleString()} likes</span>
                            <span className="comments-count">{screenshot.comments} comments</span>
                          </div>
                          <div className="mock-post-caption">
                            <strong>instaintelli</strong> {screenshot.caption}
                          </div>
                          <div className="mock-post-description">{screenshot.description}</div>
                          <div className="mock-post-time">2 hours ago</div>
                        </div>
                      </div>
                      <div className="mock-nav-bar">
                        <span className="nav-icon active">🏠</span>
                        <span className="nav-icon">🔍</span>
                        <span className="nav-icon">➕</span>
                        <span className="nav-icon">💬</span>
                        <span className="nav-icon">👤</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="carousel-dots">
              {screenshots.map((_, index) => (
                <span
                  key={index}
                  className={`dot ${index === activeSlide ? 'active' : ''}`}
                  onClick={() => setActiveSlide(index)}
                ></span>
              ))}
            </div>
          </div>
        </div>

        {/* Right Side - Auth Forms */}
        <div className="auth-section">
          <div className="auth-card">
            <div className="logo-section">
              <div className="logo-container">
                <InstagramIcon size={56} className="main-logo-icon" />
                <h1 className="brand-logo">InstaIntelli</h1>
              </div>
              <p className="brand-tagline">Intelligent Instagram</p>
              <p className="brand-subtitle">AI-powered social media that understands context, meaning, and you</p>
            </div>

            <div className="auth-buttons">
              <button 
                className="btn-primary btn-large" 
                onClick={() => navigate('/login')}
              >
                Log In
              </button>
              <button 
                className="btn-secondary btn-large" 
                onClick={() => navigate('/register')}
              >
                Sign Up
              </button>
            </div>
          </div>

          {/* Features Section */}
          <div className="features-section">
            <div className="feature-item">
              <div className="feature-icon-wrapper">
                <div className="feature-icon">🤖</div>
                <div className="feature-badge">AI</div>
              </div>
              <div className="feature-text">
                <h3>AI Captions</h3>
                <p>Automatic intelligent caption generation</p>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon-wrapper">
                <div className="feature-icon">🔍</div>
                <div className="feature-badge">Agentic</div>
              </div>
              <div className="feature-text">
                <h3>Semantic Search</h3>
                <p>Find posts by meaning, not keywords</p>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon-wrapper">
                <div className="feature-icon">💬</div>
                <div className="feature-badge">RAG</div>
              </div>
              <div className="feature-text">
                <h3>RAG Chat</h3>
                <p>Chat with your memories intelligently</p>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon-wrapper">
                <div className="feature-icon">🔐</div>
                <div className="feature-badge">Secure</div>
              </div>
              <div className="feature-text">
                <h3>Secure MFA</h3>
                <p>Enterprise-grade security</p>
              </div>
            </div>
          </div>
          
          {/* Intelligence Badge */}
          <div className="intelligence-badge">
            <div className="badge-icon">✨</div>
            <div className="badge-text">
              <strong>Intelligent Platform</strong>
              <span>Powered by AI, Vector DBs, and Big Data Analytics</span>
            </div>
          </div>

          <div className="landing-footer">
            <p>© 2025 InstaIntelli. Built with ❤️ for Big Data Analytics</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LandingPage


