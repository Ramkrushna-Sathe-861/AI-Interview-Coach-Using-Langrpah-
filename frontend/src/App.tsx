/*
  App.tsx

  Top-level React component for the small interview chat UI.

  Responsibilities:
  - Collect user input (profile, target role, optional question history)
  - Call `chat()` from src/services/api.ts to forward the data to the backend
  - Display the backend's response

  For beginners:
  - `useState` manages local component state (inputs, loading, and response).
  - `handleSend` is the event handler that runs when the Send button is clicked.
  - `chat()` returns the JSON response from the backend and may throw on error.
*/
import React from 'react'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './components/Dashboard'

export default function App(): JSX.Element {
  return (
    <div className="container layout">
      <Sidebar />
      <div className="main">
        <Header />
        <Dashboard />
      </div>
    </div>
  )
}
