import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './LandingPage.css'

function LandingPage() {
  const [activeSlide, setActiveSlide] = useState(0)
  const navigate = useNavigate()

  const screenshots = [
    { id: 1, caption: "Share your moments" },
    { id: 2, caption: "AI-powered captions" },
    { id: 3, caption: "Discover with semantic search" },
    { id: 4, caption: "Chat with your memories" }
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveSlide((prev) => (prev + 1) % screenshots.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

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
                        <div className="mock-logo">InstaIntelli</div>
                        <div className="mock-icons">
                          <span>♥</span>
                          <span>💬</span>
                        </div>
                      </div>
                      <div className="mock-feed">
                        <div className="mock-post"></div>
                        <div className="mock-caption">{screenshot.caption}</div>
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
              <h1 className="brand-logo">InstaIntelli</h1>
              <p className="brand-tagline">AI-Powered Social Media for the Future</p>
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
              <div className="feature-icon">🤖</div>
              <div className="feature-text">
                <h3>AI Captions</h3>
                <p>Automatic caption generation</p>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon">🔍</div>
              <div className="feature-text">
                <h3>Semantic Search</h3>
                <p>Find posts by meaning</p>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon">💬</div>
              <div className="feature-text">
                <h3>RAG Chat</h3>
                <p>Chat with your memories</p>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon">🔐</div>
              <div className="feature-text">
                <h3>Secure MFA</h3>
                <p>Two-factor authentication</p>
              </div>
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

