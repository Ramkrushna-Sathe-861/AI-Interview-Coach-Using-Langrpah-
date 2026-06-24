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
import React, { useState } from 'react'
import { chat } from './services/api'

export default function App(): JSX.Element {
  // Form fields: profile (resume text), the desired target role, and history
  const [profile, setProfile] = useState('')
  const [targetRole, setTargetRole] = useState('')
  const [history, setHistory] = useState('[]')

  // UI state: output text and a loading flag
  const [output, setOutput] = useState('No response yet')
  const [loading, setLoading] = useState(false)

  // Called when the user clicks the Send button.
  // It calls the backend via the `chat` service and updates the output area.
  async function handleSend() {
    setLoading(true)
    setOutput('Loading...')
    try {
      const res = await chat(profile, targetRole, history)
      // Pretty-print the JSON response for readability
      setOutput(JSON.stringify(res, null, 2))
    } catch (err: any) {
      setOutput('Error: ' + (err?.message || String(err)))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1>InterviewPilot — Chat</h1>

        <div className="form-row">
          <label>Profile (brief):</label>
          {/* This textarea holds the profile or resume summary */}
          <textarea rows={4} value={profile} onChange={e => setProfile(e.target.value)} placeholder="Paste resume summary or profile..." />
        </div>

        <div className="form-row">
          <label>Target role:</label>
          {/* Simple input for the role the user is targeting */}
          <input value={targetRole} onChange={e => setTargetRole(e.target.value)} placeholder="e.g. Senior Backend Engineer" />
        </div>

        <div className="form-row">
          <label>History (JSON array or leave blank):</label>
          {/* Optional previous questions/answers - kept as a JSON string for simplicity */}
          <textarea rows={3} value={history} onChange={e => setHistory(e.target.value)} placeholder='[{"question":"...","answer":"..."}]' />
        </div>

        <div className="controls">
          <button className="btn" onClick={handleSend} disabled={loading}>
            {loading ? <span className="spinner" aria-hidden /> : null}
            {loading ? 'Sending...' : 'Send Chat'}
          </button>
          <button className="btn secondary" onClick={() => { setProfile(''); setTargetRole(''); setHistory('[]'); setOutput('No response yet')}}>Clear</button>
          <div style={{marginLeft:'auto'}} className="meta">Tip: provide a short profile and a target role.</div>
        </div>

        <div className="output-wrap">
          <h2>Response</h2>
          {/* Output area shows the response (or errors) from the backend */}
          <pre id="output">{output}</pre>
        </div>
      </div>
    </div>
  )
}
