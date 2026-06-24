import React from 'react'

const NAV_ITEMS = [
  { label: 'Dashboard', icon: '🏠' },
  { label: 'Resume Intelligence', icon: '📄' },
  { label: 'Skill Gap Analyzer', icon: '📊' },
  { label: 'Learning Roadmap', icon: '🗺️' },
  { label: 'Mock Interview', icon: '🎙️' },
  { label: 'Feedback Center', icon: '💬' },
  { label: 'Agent Activity', icon: '🤖' },
  { label: 'Analytics & Reports', icon: '📈' },
  { label: 'Settings', icon: '⚙️' },
]

export default function Sidebar(): JSX.Element {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <div className="brand">
          <span className="brand-mark">IP</span>
          <div>
            <div>InterviewPilot AI</div>
            <div className="brand-subtitle">Your AI Interview Coach</div>
          </div>
        </div>

        <ul className="nav">
          {NAV_ITEMS.map((item) => (
            <li key={item.label} className={`nav-item ${item.label === 'Dashboard' ? 'active' : ''}`}>
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="sidebar-footer">
        <div className="promo-card">
          <div className="promo-title">Upgrade to Pro</div>
          <div className="meta">Unlock unlimited mock interviews, advanced analytics & more.</div>
          <button className="btn">Upgrade Now →</button>
        </div>
        <div className="user-info">
          <div className="avatar">AV</div>
          <div>
            <div className="user-name">Aman Verma</div>
            <div className="meta">aman.verma@email.com</div>
          </div>
        </div>
      </div>
    </aside>
  )
}
