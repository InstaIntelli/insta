/**
 * Stories Component - Instagram-like stories carousel
 */

import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import './Stories.css'

function Stories({ stories = [] }) {
  const [currentIndex, setCurrentIndex] = useState(0)

  // Mock stories if none provided
  const mockStories = stories.length > 0 ? stories : [
    { id: 1, username: 'user1', avatar: null, hasNew: true },
    { id: 2, username: 'user2', avatar: null, hasNew: true },
    { id: 3, username: 'user3', avatar: null, hasNew: false },
    { id: 4, username: 'user4', avatar: null, hasNew: true },
    { id: 5, username: 'user5', avatar: null, hasNew: false },
    { id: 6, username: 'user6', avatar: null, hasNew: true },
  ]

  const scrollLeft = () => {
    setCurrentIndex(Math.max(0, currentIndex - 1))
  }

  const scrollRight = () => {
    setCurrentIndex(Math.min(mockStories.length - 1, currentIndex + 1))
  }

  return (
    <div className="stories-container">
      <div className="stories-wrapper">
        {currentIndex > 0 && (
          <button className="stories-scroll-btn stories-scroll-left" onClick={scrollLeft}>
            ‹
          </button>
        )}
        
        <div className="stories-list">
          {mockStories.map((story, index) => (
            <Link
              key={story.id}
              to={`/stories/${story.username}`}
              className={`story-item ${story.hasNew ? 'has-new' : ''}`}
            >
              <div className="story-avatar-wrapper">
                <div className="story-avatar">
                  {story.avatar ? (
                    <img src={story.avatar} alt={story.username} />
                  ) : (
                    <div className="story-avatar-placeholder">
                      {story.username?.[0]?.toUpperCase() || 'U'}
                    </div>
                  )}
                </div>
              </div>
              <div className="story-username">{story.username}</div>
            </Link>
          ))}
        </div>

        {currentIndex < mockStories.length - 5 && (
          <button className="stories-scroll-btn stories-scroll-right" onClick={scrollRight}>
            ›
          </button>
        )}
      </div>
    </div>
  )
}

export default Stories
