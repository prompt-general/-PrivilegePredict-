import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import IdentityGraph from './components/IdentityGraph'
import IdentityList from './components/IdentityList'
import Dashboard from './components/Dashboard'
import Settings from './components/Settings'
import AuditLog from './components/AuditLog'
import Navigation from './components/Navigation'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/graph" element={<IdentityGraph />} />
            <Route path="/identities" element={<IdentityList />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/audit" element={<AuditLog />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App