/**
 * Upload Page - Instagram-like with Drag & Drop
 */

import React, { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { postService } from '../services/postService'
import { aiService } from '../services/aiService'
import './Upload.css'

function UploadPage() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef(null)
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  const handleFileChange = (selectedFile) => {
    if (selectedFile && selectedFile.type.startsWith('image/')) {
      setFile(selectedFile)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(selectedFile)
      setError('')
    } else {
      setError('Please select a valid image file')
    }
  }

  const handleInputChange = (e) => {
    if (e.target.files[0]) {
      handleFileChange(e.target.files[0])
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    if (e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0])
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    if (!file) {
      setError('Please select an image')
      setLoading(false)
      return
    }

    if (!user.user_id) {
      setError('Please login to upload posts')
      setLoading(false)
      return
    }

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('user_id', user.user_id)
      if (text) formData.append('text', text)

      // Upload post
      const response = await postService.uploadPost(formData)
      const postId = response.post_id

      setSuccess('Post uploaded successfully! Processing with AI...')

      // Trigger AI processing (background)
      if (postId) {
        try {
          await aiService.processPost({
            post_id: postId,
            user_id: user.user_id
          })
        } catch (aiErr) {
          console.log('AI processing error (non-critical):', aiErr)
        }
      }

      // Redirect after short delay
      setTimeout(() => {
        navigate('/feed')
      }, 1500)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="upload-container">
      <div className="upload-card">
        <h2>Create New Post</h2>
        
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        
        <form onSubmit={handleSubmit}>
          <div 
            className={`upload-preview ${isDragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => !preview && fileInputRef.current?.click()}
          >
            {preview ? (
              <div className="preview-container">
                <img src={preview} alt="Preview" className="preview-image" />
                <button
                  type="button"
                  className="change-image-btn"
                  onClick={(e) => {
                    e.stopPropagation()
                    fileInputRef.current?.click()
                  }}
                >
                  Change Image
                </button>
              </div>
            ) : (
              <div className="upload-placeholder">
                <div className="upload-icon">📷</div>
                <p className="upload-text">Drag and drop an image here</p>
                <p className="upload-subtext">or click to browse</p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleInputChange}
                  style={{ display: 'none' }}
                />
              </div>
            )}
          </div>

          {file && (
            <div className="upload-form-fields">
              <div className="form-group">
                <label>Caption (optional)</label>
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Write a caption..."
                  rows={4}
                  maxLength={500}
                />
                <span className="char-count">{text.length}/500</span>
              </div>
            </div>
          )}

          <div className="upload-actions">
            <button 
              type="button" 
              onClick={() => navigate('/feed')} 
              className="btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              disabled={loading || !file} 
              className="btn-primary"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Uploading...
                </>
              ) : (
                'Share Post'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default UploadPage


