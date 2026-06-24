import React from 'react'

export default function Header(): JSX.Element {
  return (
    <header className="header">
      <div className="search-wrap">
        <input className="search" placeholder="Search anything..." />
      </div>
      <div className="header-right">
        <button className="btn secondary">Upgrade</button>
        <div style={{width:12}} />
        <div className="avatar small">AV</div>
      </div>
    </header>
  )
}
