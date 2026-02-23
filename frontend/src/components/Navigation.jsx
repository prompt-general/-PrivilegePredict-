import React from 'react'
import { Link } from 'react-router-dom'

const Navigation = () => {
  return (
    <nav className="main-nav">
      <div className="nav-brand">PrivilegePredict <span className="beta-tag">PRO</span></div>
      <ul className="nav-links">
        <li><Link to="/">Dashboard</Link></li>
        <li><Link to="/graph">Identity Graph</Link></li>
        <li><Link to="/identities">Identities</Link></li>
        <li><Link to="/settings">Guard Policy</Link></li>
      </ul>
    </nav>
  )
}

export default Navigation