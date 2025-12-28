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
      const formData = new FormData()
      formData.append('image', file)
      if (caption) formData.append('caption', caption)
      if (text) formData.append('text', text)

      // Upload post
      const response = await postService.uploadPost(formData)
      const postId = response.post_id

      // Trigger AI processing (background)
      if (postId) {
        await aiService.processPost({
          post_id: postId,
          user_id: response.user_id,
          text: text,
          image_url: response.image_url
        })
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


