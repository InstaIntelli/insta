/**
 * Main Layout Component
 * Provides consistent navigation and structure
 */

import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import './Layout.css'

function Layout({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  const isActive = (path) => location.pathname === path

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  return (
    <div className="layout">
      {/* Top Navigation Bar */}
      <nav className="top-nav">
        <div className="nav-container">
          <Link to="/feed" className="nav-logo">
            <span className="logo-icon">✨</span>
            <span className="logo-text">InstaIntelli</span>
          </Link>

          <div className="nav-search">
            <input
              type="text"
              placeholder="Search posts..."
              onClick={() => navigate('/search')}
              readOnly
            />
            <span className="search-icon">🔍</span>
          </div>

          <div className="nav-links">
            <Link
              to="/feed"
              className={`nav-link ${isActive('/feed') ? 'active' : ''}`}
              title="Feed"
            >
              <span className="nav-icon">🏠</span>
            </Link>
            <Link
              to="/upload"
              className={`nav-link ${isActive('/upload') ? 'active' : ''}`}
              title="Upload"
            >
              <span className="nav-icon">➕</span>
            </Link>
            <Link
              to="/search"
              className={`nav-link ${isActive('/search') ? 'active' : ''}`}
              title="Search"
            >
              <span className="nav-icon">🔍</span>
            </Link>
            <Link
              to="/chat"
              className={`nav-link ${isActive('/chat') ? 'active' : ''}`}
              title="AI Chat"
            >
              <span className="nav-icon">💬</span>
            </Link>
            {user.user_id && (
              <Link
                to={`/profile/${user.user_id}`}
                className={`nav-link ${isActive(`/profile/${user.user_id}`) ? 'active' : ''}`}
                title="Profile"
              >
                <span className="nav-icon">👤</span>
              </Link>
            )}
            <button onClick={handleLogout} className="nav-link logout-btn" title="Logout">
              <span className="nav-icon">🚪</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

export default Layout


