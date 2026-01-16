/**
 * Search Page - Modern Semantic Search UI
 * For Alisha - CUSTOMIZABLE to your liking!
 */

import React, { useState } from 'react'
import { searchService } from '../services/searchService'
import { formatApiError } from '../services/api'
import PostCard from '../components/PostCard'
import './Search.css'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [searched, setSearched] = useState(false)
  const [searchType, setSearchType] = useState('semantic') // 'semantic' | 'keyword'
  const [searchScope, setSearchScope] = useState('global') // 'my' | 'global'

  const handleSearch = async (e) => {
    if (e) e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError('')
    setSearched(true)

    try {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      const data = await searchService.search(
        query,
        user.user_id,
        searchType,
        searchScope === 'global',
        20
      )
      setResults(data.results || [])
    } catch (err) {
      setError(formatApiError(err))
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="search-page">
      <div className="search-hero">
        <h1>Semantic Search</h1>
        <p>Harness the power of AI to find exactly what you're looking for using natural language.</p>
      </div>

      <div className="search-container">
        {/* Modern Segmented Toggles */}
        <div className="search-controls">
          <div className="control-group" title="Choose search method">
            <button
              type="button"
              className={`control-btn ${searchType === 'semantic' ? 'active' : ''}`}
              onClick={() => setSearchType('semantic')}
            >
              <span>✨</span> Semantic
            </button>
            <button
              type="button"
              className={`control-btn ${searchType === 'keyword' ? 'active' : ''}`}
              onClick={() => setSearchType('keyword')}
            >
              <span>⌨️</span> Keyword
            </button>
          </div>

          <div className="control-group" title="Limit search scope">
            <button
              type="button"
              className={`control-btn ${searchScope === 'global' ? 'active' : ''}`}
              onClick={() => setSearchScope('global')}
            >
              <span>🌎</span> Global
            </button>
            <button
              type="button"
              className={`control-btn ${searchScope === 'my' ? 'active' : ''}`}
              onClick={() => setSearchScope('my')}
            >
              <span>👤</span> My Posts
            </button>
          </div>
        </div>

        <form onSubmit={handleSearch} className="search-form-modern">
          <div className="search-input-wrapper">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={searchType === 'semantic'
                ? "Try: 'Show me posts about AI' or 'Find posts with dogs'..."
                : "Enter keywords to match exactly..."
              }
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
                aria-label="Clear Search"
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
            <p>Scanning vectors and analyzing meaning...</p>
          </div>
        )}

        {searched && !loading && (
          <div className="search-results-section animate-fade-in">
            <div className="results-header">
              <h2>
                {results.length > 0 ? (
                  <>
                    Discovered <span className="results-count">{results.length}</span> {results.length === 1 ? 'match' : 'matches'}
                  </>
                ) : (
                  'No exact matches discovered'
                )}
              </h2>
            </div>

            {results.length === 0 ? (
              <div className="no-results-modern card-glass">
                <span className="no-results-icon">🔎</span>
                <h3>We couldn't find what you're looking for</h3>
                <p>Try rephrasing your search or explore these popular topics:</p>
                <div className="suggestion-tags">
                  <button onClick={() => { setQuery('AI and machine learning'); handleSearch(); }} className="suggestion-tag">AI & ML</button>
                  <button onClick={() => { setQuery('beautiful nature photography'); handleSearch(); }} className="suggestion-tag">Nature</button>
                  <button onClick={() => { setQuery('delicious food recipes'); handleSearch(); }} className="suggestion-tag">Food</button>
                  <button onClick={() => { setQuery('exciting travel adventures'); handleSearch(); }} className="suggestion-tag">Travel</button>
                </div>
              </div>
            ) : (
              <div className="results-feed">
                {results.map((result, index) => {
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
                        <div className="similarity-badge" title="AI Confidence Score">
                          <span>✨</span>
                          <span>{(result.similarity_score * 100).toFixed(0)}% Match</span>
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
            <h3>💡 Master Your Search</h3>
            <div className="tips-grid">
              <div className="tip-card">
                <div className="tip-icon">🧠</div>
                <h4>Semantic Power</h4>
                <p>Use natural sentences. Instead of "dog", try "Show me cute golden retriever puppies".</p>
              </div>
              <div className="tip-card">
                <div className="tip-icon">❓</div>
                <h4>Ask Questions</h4>
                <p>Curious about your history? Try "What did I post about our summer trip?"</p>
              </div>
              <div className="tip-card">
                <div className="tip-icon">🌍</div>
                <h4>Scope Control</h4>
                <p>Switch to Global to discover inspiration from the entire community.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchPage

