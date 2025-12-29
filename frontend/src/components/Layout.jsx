/**
 * Instagram-style Layout Component
 * Sidebar navigation with theme toggle
 */

import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useTheme } from '../contexts/ThemeContext'
import './Layout.css'

function Layout({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const { theme, toggleTheme, isDark } = useTheme()
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  const [showMenu, setShowMenu] = useState(false)

  const isActive = (path) => location.pathname === path || location.pathname.startsWith(path)

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      navigate('/login')
    }
  }

  const navItems = [
    { path: '/feed', icon: '🏠', label: 'Home', activeIcon: '🏠' },
    { path: '/search', icon: '🔍', label: 'Search', activeIcon: '🔎' },
    { path: '/upload', icon: '➕', label: 'Create', activeIcon: '✨' },
    { path: '/chat', icon: '💬', label: 'Chat', activeIcon: '💬' },
    { path: `/profile/${user.user_id}`, icon: '👤', label: 'Profile', activeIcon: '👤' }
  ]

  return (
    <div className="app-layout" data-theme={theme}>
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-content">
          {/* Logo */}
          <Link to="/feed" className="sidebar-logo">
            <h1>InstaIntelli</h1>
          </Link>

          {/* Navigation Links */}
          <nav className="sidebar-nav">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`sidebar-nav-item ${isActive(item.path) ? 'active' : ''}`}
              >
                <span className="nav-item-icon">
                  {isActive(item.path) ? item.activeIcon : item.icon}
                </span>
                <span className="nav-item-label">{item.label}</span>
              </Link>
            ))}
          </nav>

          {/* Bottom Actions */}
          <div className="sidebar-bottom">
            {/* Theme Toggle */}
            <button 
              onClick={toggleTheme} 
              className="sidebar-nav-item theme-toggle"
              title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
            >
              <span className="nav-item-icon">{isDark ? '☀️' : '🌙'}</span>
              <span className="nav-item-label">{isDark ? 'Light' : 'Dark'}</span>
            </button>

            {/* More Menu */}
            <div className="more-menu">
              <button 
                onClick={() => setShowMenu(!showMenu)} 
                className="sidebar-nav-item"
              >
                <span className="nav-item-icon">☰</span>
                <span className="nav-item-label">More</span>
              </button>

              {showMenu && (
                <div className="dropdown-menu">
                  <button onClick={handleLogout} className="dropdown-item">
                    <span>🚪</span>
                    <span>Logout</span>
                  </button>
                  <Link to="/mfa/setup" className="dropdown-item">
                    <span>🔐</span>
                    <span>Security</span>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content-area">
        <div className="content-wrapper">
          {children}
        </div>
      </main>

      {/* Mobile Bottom Navigation */}
      <nav className="mobile-bottom-nav">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`mobile-nav-item ${isActive(item.path) ? 'active' : ''}`}
          >
            <span className="mobile-nav-icon">
              {isActive(item.path) ? item.activeIcon : item.icon}
            </span>
          </Link>
        ))}
        <button onClick={() => setShowMenu(!showMenu)} className="mobile-nav-item">
          <span className="mobile-nav-icon">☰</span>
        </button>
      </nav>
    </div>
  )
}

export default Layout
