import React from 'react'

const NAV_ITEMS = [
  'Dashboard', 'Learning Plan', 'Skill Gap Analyzer', 'Mock Interviews', 'Question Bank',
  'Resume Review', 'Progress Tracker', 'Analytics', 'AI Feedback', 'Bookmarks'
]

export default function Sidebar(): JSX.Element {
  return (
    <aside className="sidebar card">
      <div className="brand">InterviewPilot AI</div>

      <ul className="nav">
        {NAV_ITEMS.map((it) => (
          <li key={it} className="nav-item"> 
            <span className="nav-icon">•</span>
            <span className="nav-label">{it}</span>
          </li>
        ))}
      </ul>

      <div className="cta-upgrade">
        <button className="btn">Upgrade Now</button>
      </div>

      <div className="sidebar-footer">
        <div className="avatar">AV</div>
        <div style={{marginLeft:10}}>
          <div style={{fontWeight:700}}>Aman Verma</div>
          <div className="meta">aman.verma@email.com</div>
        </div>
      </div>
    </aside>
  )
}
