import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import IdentityGraph from './components/IdentityGraph'
import IdentityList from './components/IdentityList'
import Navigation from './components/Navigation'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main>
          <Routes>
            <Route path="/" element={<IdentityGraph />} />
            <Route path="/identities" element={<IdentityList />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App