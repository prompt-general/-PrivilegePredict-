import React from 'react'
import { Link } from 'react-router-dom'

const Navigation = () => {
  return (
    <nav className="navigation">
      <h1>PrivilegePredict</h1>
      <ul>
        <li><Link to="/">Graph Visualization</Link></li>
        <li><Link to="/identities">Identities</Link></li>
      </ul>
    </nav>
  )
}

export default Navigation