import React from 'react'
import { chat } from '../services/api'

// Dashboard contains the main card we had previously (chat UI)
export default function Dashboard(): JSX.Element {
  return (
    <main>
      <section className="card">
        <h1>Welcome to InterviewPilot</h1>
        <p className="meta">Your personal AI interview coach — quick chat demo</p>
        <div style={{height:12}} />
        <div className="grid" style={{gap:12}}>
          <div className="card">
            <h3>Skill Gap Overview</h3>
            <p className="meta">A quick summary of strengths and areas to improve.</p>
          </div>
          <div className="card">
            <h3>Mock Interview</h3>
            <p className="meta">Start a practice interview with AI and get feedback.</p>
          </div>
        </div>
      </section>
    </main>
  )
}
