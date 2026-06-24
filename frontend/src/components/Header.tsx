import React from 'react'

export default function Header(): JSX.Element {
  return (
    <header className="header">
      <div>
        <div className="header-title">Welcome back, Aman! 👋</div>
        <div className="header-subtitle">Let's continue your interview preparation journey.</div>
      </div>
      <div className="header-right">
        <div className="search-wrap">
          <input className="search" placeholder="Search anything..." />
        </div>
        <button className="btn secondary">Upgrade</button>
        <div className="avatar small">AV</div>
      </div>
    </header>
  )
}
