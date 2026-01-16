/**
 * Messages Page - User-to-User Chat
 * Modern, high-end messaging interface
 */

import React, { useState, useEffect, useRef } from 'react'
import { socialService } from '../services/socialService'
import { getUser } from '../utils/auth'
import './Messages.css'

function MessagesPage() {
    const [conversations, setConversations] = useState([])
    const [activeConv, setActiveConv] = useState(null)
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [convLoading, setConvLoading] = useState(true)
    const messagesEndRef = useRef(null)
    const currentUser = getUser()

    useEffect(() => {
        loadConversations()

        // Poll for new messages every 5 seconds if a conversation is active
        const timer = setInterval(() => {
            if (activeConv) {
                loadMessages(activeConv.user_id, true)
            }
            loadConversations(true)
        }, 5000)

        return () => clearInterval(timer)
    }, [activeConv?.user_id])

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const loadConversations = async (silent = false) => {
        try {
            if (!silent) setConvLoading(true)
            const data = await socialService.getConversations()
            setConversations(data.conversations || [])
        } catch (err) {
            console.error('Error loading conversations:', err)
        } finally {
            if (!silent) setConvLoading(false)
        }
    }

    const loadMessages = async (userId, silent = false) => {
        try {
            if (!silent) setLoading(true)
            const data = await socialService.getMessages(userId)
            // Only update if message count changed to avoid flickering during polling
            if (data.messages?.length !== messages.length) {
                setMessages(data.messages || [])
            }
        } catch (err) {
            console.error('Error loading messages:', err)
        } finally {
            if (!silent) setLoading(false)
        }
    }

    const handleSelectConv = (conv) => {
        setActiveConv(conv)
        setMessages([])
        loadMessages(conv.user_id)
    }

    const handleSend = async (e) => {
        e.preventDefault()
        if (!input.trim() || !activeConv) return

        const messageText = input.trim()
        setInput('')

        // Optimistic update
        const tempMsg = {
            message_id: Date.now(),
            sender_id: currentUser.user_id,
            content: messageText,
            created_at: new Date().toISOString(),
            recipient_id: activeConv.user_id
        }
        setMessages(prev => [...prev, tempMsg])

        try {
            await socialService.sendMessage(activeConv.user_id, messageText)
            loadMessages(activeConv.user_id, true)
            loadConversations(true)
        } catch (err) {
            console.error('Error sending message:', err)
            alert('Failed to send message')
            // Rollback or show error
        }
    }

    const formatMessageTime = (dateStr) => {
        const date = new Date(dateStr)
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    return (
        <div className="messages-page">
            {/* Conversations List Sidebar */}
            <aside className={`conversations-sidebar ${activeConv ? 'hidden-mobile' : ''}`}>
                <div className="conversations-header">
                    <h2>Messages</h2>
                    <button className="new-message-btn" title="New Message">📝</button>
                </div>

                <div className="conversations-list">
                    {convLoading ? (
                        <div className="loading-state">Loading chats...</div>
                    ) : conversations.length === 0 ? (
                        <div className="empty-state">No conversations yet</div>
                    ) : (
                        conversations.map(conv => (
                            <div
                                key={conv.user_id}
                                className={`conversation-item ${activeConv?.user_id === conv.user_id ? 'active' : ''}`}
                                onClick={() => handleSelectConv(conv)}
                            >
                                <div className="conv-avatar">
                                    {conv.profile_picture ? (
                                        <img src={conv.profile_picture} alt={conv.username} />
                                    ) : (
                                        <div className="avatar-placeholder-small">
                                            {conv.username?.[0]?.toUpperCase() || 'U'}
                                        </div>
                                    )}
                                    <span className={`status-indicator ${conv.status || 'offline'}`}></span>
                                </div>
                                <div className="conv-info">
                                    <div className="conv-top">
                                        <span className="conv-name">{conv.username}</span>
                                        <span className="conv-time">
                                            {conv.last_message_time ? formatMessageTime(conv.last_message_time) : ''}
                                        </span>
                                    </div>
                                    <div className="conv-last-msg">
                                        {conv.last_message || 'Start a conversation'}
                                    </div>
                                </div>
                                {conv.unread_count > 0 && (
                                    <span className="unread-badge">{conv.unread_count}</span>
                                )}
                            </div>
                        ))
                    )}
                </div>
            </aside>

            {/* Main Chat Area */}
            <main className={`chat-main ${!activeConv ? 'hidden-mobile' : ''}`}>
                {activeConv ? (
                    <>
                        <header className="chat-active-header">
                            <button
                                className="back-btn-mobile"
                                onClick={() => setActiveConv(null)}
                            >←</button>
                            <div className="conv-avatar">
                                {activeConv.profile_picture ? (
                                    <img src={activeConv.profile_picture} alt={activeConv.username} />
                                ) : (
                                    <div className="avatar-placeholder-small">
                                        {activeConv.username?.[0]?.toUpperCase() || 'U'}
                                    </div>
                                )}
                            </div>
                            <div className="chat-header-info">
                                <h3>{activeConv.username}</h3>
                                <span className="user-status-text">{activeConv.status === 'online' ? 'Active now' : 'Offline'}</span>
                            </div>
                        </header>

                        <div className="chat-messages-container">
                            {loading && messages.length === 0 ? (
                                <div className="loading-messages">Loading messages...</div>
                            ) : messages.length === 0 ? (
                                <div className="no-messages">Say hello to @{activeConv.username}! 👋</div>
                            ) : (
                                messages.map(msg => (
                                    <div
                                        key={msg.message_id}
                                        className={`message-card ${msg.sender_id === currentUser.user_id ? 'sent' : 'received'}`}
                                    >
                                        {msg.content}
                                        <span className="message-meta">{formatMessageTime(msg.created_at)}</span>
                                    </div>
                                ))
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        <form onSubmit={handleSend} className="chat-input-area">
                            <div className="message-input-wrapper">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    placeholder="Type a message..."
                                />
                                <button
                                    type="submit"
                                    disabled={!input.trim()}
                                    className="btn-send-message"
                                >
                                    ➤
                                </button>
                            </div>
                        </form>
                    </>
                ) : (
                    <div className="empty-chat-state">
                        <div className="empty-chat-icon">✉️</div>
                        <h3>Your Messages</h3>
                        <p>Send private photos and messages to a friend or group.</p>
                        <button className="btn-primary" onClick={() => loadConversations()}>View Conversations</button>
                    </div>
                )}
            </main>
        </div>
    )
}

export default MessagesPage
