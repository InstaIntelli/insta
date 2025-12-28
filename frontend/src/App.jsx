import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Profile from './pages/Profile'
import ProtectedRoute from './components/ProtectedRoute'
import { isAuthenticated } from './utils/auth'
import './index.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            isAuthenticated() ? <Navigate to="/profile" replace /> : <Navigate to="/login" replace />
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  )
}

export default App

