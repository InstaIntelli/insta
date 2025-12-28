/**
 * Search Page - Modern Semantic Search UI
 * For Alisha - CUSTOMIZABLE to your liking!
 */

import React, { useState } from 'react'
import { searchService } from '../services/searchService'
import PostCard from '../components/PostCard'
import './Search.css'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [searched, setSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError('')
    setSearched(true)

    try {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      const data = await searchService.semanticSearch(
        query,
        user.user_id || null,
        10
      )
      setResults(data.results || [])
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed. Please try again.')
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="search-page">
      <div className="search-hero">
        <div className="search-hero-content">
          <div className="search-icon-large">🔍</div>
          <h1>Semantic Search</h1>
          <p>Find your posts using natural language</p>
        </div>
      </div>

      <div className="search-container">
        <form onSubmit={handleSearch} className="search-form-modern">
          <div className="search-input-wrapper">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Try: 'Show me posts about AI' or 'Find posts with dogs'..."
              className="search-input-modern"
              autoFocus
            />
            {query && (
              <button
                type="button"
                onClick={() => {
                  setQuery('')
                  setResults([])
                  setSearched(false)
                }}
                className="clear-button"
                aria-label="Clear"
              >
                ✕
              </button>
            )}
            <button type="submit" disabled={loading || !query.trim()} className="search-button-modern">
              {loading ? (
                <span className="button-spinner"></span>
              ) : (
                'Search'
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {loading && (
          <div className="search-loading">
            <div className="loading-spinner"></div>
            <p>Searching through your posts...</p>
          </div>
        )}

        {searched && !loading && (
          <div className="search-results-section">
            <div className="results-header">
              <h2>
                {results.length > 0 ? (
                  <>
                    Found <span className="results-count">{results.length}</span> {results.length === 1 ? 'post' : 'posts'}
                  </>
                ) : (
                  'No results found'
                )}
              </h2>
            </div>

            {results.length === 0 ? (
              <div className="no-results-modern">
                <div className="no-results-icon">🔎</div>
                <h3>No posts found</h3>
                <p>Try different keywords or upload more posts to search through!</p>
                <div className="suggestions">
                  <p className="suggestions-title">Try searching for:</p>
                  <div className="suggestion-tags">
                    <button onClick={() => setQuery('posts about technology')} className="suggestion-tag">technology</button>
                    <button onClick={() => setQuery('posts with nature')} className="suggestion-tag">nature</button>
                    <button onClick={() => setQuery('food posts')} className="suggestion-tag">food</button>
                    <button onClick={() => setQuery('travel posts')} className="suggestion-tag">travel</button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="results-feed">
                {results.map((result, index) => {
                  // Convert result to post format for PostCard
                  const post = {
                    post_id: result.post_id,
                    user_id: result.metadata?.user_id || 'unknown',
                    username: result.metadata?.user_id || 'user',
                    image_url: result.metadata?.image_url,
                    caption: result.metadata?.caption,
                    text: result.metadata?.text,
                    created_at: result.metadata?.created_at,
                    topics: result.metadata?.topics?.split(',').filter(t => t.trim()) || [],
                    similarity_score: result.similarity_score
                  }
                  return (
                    <div key={result.post_id || index} className="result-item">
                      <PostCard post={post} />
                      {result.similarity_score && (
                        <div className="similarity-badge">
                          <span className="similarity-icon">✨</span>
                          <span>{(result.similarity_score * 100).toFixed(0)}% match</span>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )}

        {!searched && (
          <div className="search-tips">
            <h3>💡 Search Tips</h3>
            <ul>
              <li>Use natural language: "Show me posts about AI"</li>
              <li>Search by topic: "Find posts with dogs"</li>
              <li>Ask questions: "What posts did I upload about travel?"</li>
              <li>Our AI understands context and meaning, not just keywords!</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchPage

