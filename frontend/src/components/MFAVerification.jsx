/**
 * MFA Verification Component
 * For login flow
 */

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { mfaService } from '../services/mfaService'
import './MFAVerification.css'

function MFAVerification({ userId, email, onCancel }) {
  const [code, setCode] = useState('')
  const [useRecoveryCode, setUseRecoveryCode] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await mfaService.verifyMFALogin(userId, code)
      navigate('/feed')
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid verification code')
    } finally {
      setLoading(false)
    }
  }

  const handleCodeChange = (e) => {
    let value = e.target.value
    
    if (useRecoveryCode) {
      // Recovery code format: XXXX-XXXX
      value = value.toUpperCase().replace(/[^A-Z0-9-]/g, '')
      if (value.length > 9) value = value.slice(0, 9)
      // Auto-add hyphen
      if (value.length === 4 && !value.includes('-')) {
        value = value + '-'
      }
    } else {
      // TOTP code: 6 digits
      value = value.replace(/\D/g, '').slice(0, 6)
    }
    
    setCode(value)
  }

  return (
    <div className="mfa-verification-container">
      <div className="mfa-verification-card">
        <h2>Two-Factor Authentication</h2>
        <p className="mfa-email">Logging in as: <strong>{email}</strong></p>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>
              {useRecoveryCode ? 'Recovery Code' : 'Verification Code'}
            </label>
            <input
              type="text"
              value={code}
              onChange={handleCodeChange}
              placeholder={useRecoveryCode ? 'XXXX-XXXX' : '000000'}
              className="code-input"
              autoFocus
              required
            />
            <small className="help-text">
              {useRecoveryCode 
                ? 'Enter one of your recovery codes' 
                : 'Enter the 6-digit code from your authenticator app'
              }
            </small>
          </div>

          <button 
            type="submit" 
            className="btn-primary"
            disabled={loading || (useRecoveryCode ? code.length !== 9 : code.length !== 6)}
          >
            {loading ? 'Verifying...' : 'Verify'}
          </button>
        </form>

        <div className="mfa-options">
          <button 
            type="button"
            onClick={() => {
              setUseRecoveryCode(!useRecoveryCode)
              setCode('')
              setError('')
            }}
            className="link-button"
          >
            {useRecoveryCode ? 'Use authenticator code' : 'Use recovery code'}
          </button>
        </div>

        {onCancel && (
          <button 
            type="button"
            onClick={onCancel}
            className="btn-cancel"
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  )
}

export default MFAVerification


