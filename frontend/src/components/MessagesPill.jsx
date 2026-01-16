/**
 * Messages Pill - Floating bottom-right navigation
 * Instagram-inspired quick access
 */

import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { socialService } from '../services/socialService'
import './MessagesPill.css'

function MessagesPill() {
    const [unreadCount, setUnreadCount] = useState(0)
    const navigate = useNavigate()
    const location = useLocation()
    const user = JSON.parse(localStorage.getItem('user') || '{}')

    useEffect(() => {
        const fetchUnread = async () => {
            try {
                const data = await socialService.getUnreadCount()
                setUnreadCount(data.unread_count || 0)
            } catch (err) {
                // Silently fails for background polling
            }
        }

        fetchUnread()
        const timer = setInterval(fetchUnread, 10000)
        return () => clearInterval(timer)
    }, [])

    // Don't show on login/landing or if on messages page
    const hideOnPaths = ['/login', '/register', '/', '/messages']
    if (hideOnPaths.includes(location.pathname) || !user.user_id) {
        return null
    }

    return (
        <div className="messages-pill-container" onClick={() => navigate('/messages')}>
            <div className="messages-pill">
                <div className="pill-icon-wrapper">
                    <span className="pill-icon">✉️</span>
                    {unreadCount > 0 && (
                        <span className="pill-badge">{unreadCount}</span>
                    )}
                </div>
                <span className="pill-label">Messages</span>
                <div className="pill-avatar">
                    {user.profile_picture ? (
                        <img src={user.profile_picture} alt="Profile" />
                    ) : (
                        <span className="avatar-letter">{user.username?.[0]?.toUpperCase() || 'U'}</span>
                    )}
                </div>
            </div>
        </div>
    )
}

export default MessagesPill
