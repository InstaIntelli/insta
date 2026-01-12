/**
 * Upload Page
 * For Sami - Post Upload & Storage
 */

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { postService } from '../services/postService'
import { aiService } from '../services/aiService'
import './Upload.css'

function UploadPage() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [caption, setCaption] = useState('')
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(selectedFile)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // Get user_id from localStorage
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      const userId = user.user_id
      
      if (!userId) {
        setError('User not found. Please login again.')
        setLoading(false)
        return
      }

      const formData = new FormData()
      formData.append('file', file)  // Backend expects 'file', not 'image'
      formData.append('user_id', userId)  // Required by backend
      // Combine caption and text if both provided
      const combinedText = caption ? (text ? `${caption}\n\n${text}` : caption) : text
      if (combinedText) formData.append('text', combinedText)

      // Upload post
      const response = await postService.uploadPost(formData)
      const postId = response.post_id

      // Trigger AI processing (background) - optional, don't fail if it errors
      if (postId) {
        try {
          await aiService.processPost({
            post_id: postId,
            user_id: userId,
            text: combinedText || '',
            image_url: response.image_url
          })
        } catch (aiError) {
          console.warn('AI processing failed (non-critical):', aiError)
          // Don't fail the upload if AI processing fails
        }
      }

      navigate('/feed')
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upload-container">
      <div className="upload-card">
        <h2>Create New Post</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="upload-preview">
            {preview ? (
              <img src={preview} alt="Preview" />
            ) : (
              <div className="upload-placeholder">
                <label htmlFor="file-upload" className="upload-label">
                  <span>📷</span>
                  <p>Click to upload image</p>
                </label>
                <input
                  id="file-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  style={{ display: 'none' }}
                  required
                />
              </div>
            )}
          </div>

          {file && (
            <div className="upload-form-fields">
              <div className="form-group">
                <label>Caption</label>
                <textarea
                  value={caption}
                  onChange={(e) => setCaption(e.target.value)}
                  placeholder="Write a caption..."
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label>Text (optional)</label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Additional text..."
                  rows={2}
                />
              </div>
            </div>
          )}

          <div className="upload-actions">
            <button type="button" onClick={() => navigate('/feed')} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={loading || !file} className="btn-primary">
              {loading ? 'Uploading...' : 'Upload Post'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default UploadPage


