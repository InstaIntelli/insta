/**
 * Upload Page
 * For Sami - Post Upload & Storage
 */

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { postService } from '../services/postService'
import { aiService } from '../services/aiService'
import { formatApiError } from '../services/api'
import './Upload.css'

function UploadPage() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [caption, setCaption] = useState('')
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
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
    setSuccess('')
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

      if (!file) {
        setError('Please select an image file.')
        setLoading(false)
        return
      }

      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file (JPG, PNG, etc.)')
        setLoading(false)
        return
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB')
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

      if (!postId) {
        throw new Error('Upload succeeded but no post ID returned')
      }

      // Show success message
      setSuccess('Post uploaded successfully!')

      // Delay navigation so user sees success message
      setTimeout(() => {
        navigate('/feed', { replace: true })
      }, 1500)

    } catch (err) {
      setError(formatApiError(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upload-container">
      <div className="upload-card">
        <h2>Create New Post</h2>

        {error && <div className="error-message">{error}</div>}
        {success && (
          <div className="success-message">
            {success}
          </div>
        )}

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


