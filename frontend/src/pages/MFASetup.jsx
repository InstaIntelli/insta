/**
 * MFA Setup Page
 * Setup Google Authenticator for account
 */

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { mfaService } from '../services/mfaService'
import './MFASetup.css'

function MFASetup() {
  const [step, setStep] = useState(1) // 1: QR Code, 2: Verify, 3: Recovery Codes
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [qrCode, setQrCode] = useState('')
  const [secret, setSecret] = useState('')
  const [recoveryCodes, setRecoveryCodes] = useState([])
  const [verificationCode, setVerificationCode] = useState('')
  const [showSecret, setShowSecret] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    setupMFA()
  }, [])

  const setupMFA = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await mfaService.setupMFA()
      setQrCode(response.qr_code)
      setSecret(response.secret)
      setRecoveryCodes(response.recovery_codes)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to setup MFA')
    } finally {
      setLoading(false)
    }
  }

  const handleVerify = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      await mfaService.enableMFA(verificationCode)
      setStep(3) // Show recovery codes
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid verification code')
    } finally {
      setLoading(false)
    }
  }

  const handleComplete = () => {
    navigate('/profile/' + JSON.parse(localStorage.getItem('user')).user_id)
  }

  const downloadRecoveryCodes = () => {
    const text = recoveryCodes.join('\n')
    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'instaintelli-recovery-codes.txt'
    a.click()
  }

  const copyRecoveryCodes = () => {
    navigator.clipboard.writeText(recoveryCodes.join('\n'))
    alert('Recovery codes copied to clipboard!')
  }

  if (loading && step === 1) {
    return (
      <div className="mfa-setup-container">
        <div className="mfa-setup-card">
          <div className="loading">Setting up MFA...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="mfa-setup-container">
      <div className="mfa-setup-card">
        <h1>Setup Two-Factor Authentication</h1>
        
        {/* Step 1: QR Code */}
        {step === 1 && (
          <div className="mfa-step">
            <h2>Step 1: Scan QR Code</h2>
            <p>Scan this QR code with Google Authenticator app</p>
            
            {qrCode && (
              <div className="qr-code-container">
                <img src={qrCode} alt="QR Code" className="qr-code" />
              </div>
            )}
            
            <div className="secret-key-section">
              <p>Can't scan? Enter this key manually:</p>
              <div className="secret-key">
                {showSecret ? secret : '••••••••••••••••••••••••••••••••'}
                <button 
                  type="button"
                  onClick={() => setShowSecret(!showSecret)}
                  className="toggle-secret-btn"
                >
                  {showSecret ? 'Hide' : 'Show'}
                </button>
                <button 
                  type="button"
                  onClick={() => {
                    navigator.clipboard.writeText(secret)
                    alert('Secret key copied!')
                  }}
                  className="copy-btn"
                >
                  Copy
                </button>
              </div>
            </div>

            <button 
              onClick={() => setStep(2)} 
              className="btn-primary"
            >
              Next: Verify Code
            </button>
          </div>
        )}

        {/* Step 2: Verify */}
        {step === 2 && (
          <div className="mfa-step">
            <h2>Step 2: Verify Code</h2>
            <p>Enter the 6-digit code from your authenticator app</p>
            
            {error && <div className="error-message">{error}</div>}
            
            <form onSubmit={handleVerify}>
              <div className="form-group">
                <input
                  type="text"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  placeholder="000000"
                  maxLength="6"
                  className="code-input"
                  required
                  autoFocus
                />
              </div>

              <div className="button-group">
                <button 
                  type="button"
                  onClick={() => setStep(1)} 
                  className="btn-secondary"
                  disabled={loading}
                >
                  Back
                </button>
                <button 
                  type="submit" 
                  className="btn-primary"
                  disabled={loading || verificationCode.length !== 6}
                >
                  {loading ? 'Verifying...' : 'Verify & Enable'}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Step 3: Recovery Codes */}
        {step === 3 && (
          <div className="mfa-step">
            <h2>✅ MFA Enabled Successfully!</h2>
            <p className="success-message">
              Two-factor authentication is now enabled for your account.
            </p>
            
            <div className="recovery-codes-section">
              <h3>⚠️ Save Your Recovery Codes</h3>
              <p>
                Store these codes in a safe place. You can use them to access your account 
                if you lose your authenticator device.
              </p>
              
              <div className="recovery-codes-list">
                {recoveryCodes.map((code, index) => (
                  <div key={index} className="recovery-code">
                    {code}
                  </div>
                ))}
              </div>

              <div className="button-group">
                <button 
                  onClick={downloadRecoveryCodes} 
                  className="btn-secondary"
                >
                  📥 Download
                </button>
                <button 
                  onClick={copyRecoveryCodes} 
                  className="btn-secondary"
                >
                  📋 Copy
                </button>
              </div>
            </div>

            <button 
              onClick={handleComplete} 
              className="btn-primary"
            >
              Complete Setup
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default MFASetup

