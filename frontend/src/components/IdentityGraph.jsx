import React, { useState, useEffect, useRef } from 'react'
import cytoscape from 'cytoscape'
import { getIdentities, getPaths } from '../api'

const IdentityGraph = () => {
  const cyRef = useRef(null)
  const [cy, setCy] = useState(null)
  const [selectedIdentity, setSelectedIdentity] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(false)
  const [paths, setPaths] = useState([])

  useEffect(() => {
    const cyInstance = cytoscape({
      container: cyRef.current,
      elements: [],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#4a5568',
            'label': 'data(name)',
            'color': '#fff',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': '10px',
            'width': '40px',
            'height': '40px'
          }
        },
        {
          selector: 'node[provider = "aws"]',
          style: {
            'border-width': 2,
            'border-color': '#ff9900' // AWS Orange
          }
        },
        {
          selector: 'node[provider = "azure"]',
          style: {
            'border-width': 2,
            'border-color': '#0078d4' // Azure Blue
          }
        },
        {
          selector: 'node[type = "user"]',
          style: { 'background-color': '#3182ce' }
        },
        {
          selector: 'node[type = "role"]',
          style: { 'background-color': '#e53e3e' }
        },
        {
          selector: 'node[type = "group"]',
          style: { 'background-color': '#38a169' }
        },
        {
          selector: 'node[type = "service_principal"]',
          style: { 'background-color': '#d69e2e' }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#cbd5e0',
            'target-arrow-color': '#cbd5e0',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(type)',
            'font-size': '8px',
            'text-rotation': 'autorotate'
          }
        },
        {
          selector: '.highlighted',
          style: {
            'background-color': '#f56565',
            'line-color': '#f56565',
            'target-arrow-color': '#f56565',
            'transition-property': 'background-color, line-color, target-arrow-color',
            'transition-duration': '0.5s'
          }
        }
      ],
      layout: {
        name: 'cose',
        animate: true,
        padding: 50
      }
    })

    cyInstance.on('tap', 'node', (event) => {
      setSelectedIdentity(event.target.data())
    })

    setCy(cyInstance)
    loadGraphData(cyInstance)

    return () => {
      if (cyInstance) cyInstance.destroy()
    }
  }, [])

  const loadGraphData = async (cyInstance) => {
    setLoading(true)
    try {
      const response = await getIdentities()
      const nodes = response.data.map(id => ({
        data: { ...id }
      }))

      // For Phase 1, we might need to fetch relationships too if they aren't in identities
      // Assuming identities API returns a structured graph or we need a separate /graph endpoint
      // But for now, let's just add the nodes.
      cyInstance.add(nodes)
      cyInstance.layout({ name: 'cose' }).run()
      cyInstance.fit()
    } catch (error) {
      console.error('Error loading graph data:', error)
    } finally {
      setLoading(false)
    }
  }

  const findEscalation = async () => {
    if (!selectedIdentity) return
    setLoading(true)
    try {
      const response = await getPaths(selectedIdentity.id)
      setPaths(response.data)

      // Highlight paths in the graph
      if (cy && response.data.length > 0) {
        cy.elements().removeClass('highlighted')
        response.data.forEach(path => {
          path.nodes.forEach(node => {
            cy.getElementById(node.id).addClass('highlighted')
          })
          // We'd also need edge IDs here, but for now highlighting nodes is a start
        })
      }
    } catch (error) {
      console.error('Pathfinding error:', error)
    } finally {
      setLoading(false)
    }
  }

  const searchIdentities = () => {
    if (!cy || !searchTerm) return
    const results = cy.nodes().filter(node =>
      node.data('name').toLowerCase().includes(searchTerm.toLowerCase()) ||
      node.data('id').toLowerCase().includes(searchTerm.toLowerCase())
    )

    cy.nodes().removeClass('highlighted')
    results.addClass('highlighted')
    if (results.length > 0) {
      cy.animate({
        center: { eles: results },
        zoom: 2
      })
    }
  }

  return (
    <div className="identity-graph-container">
      <div className="identity-graph-main">
        <div className="controls-overlay">
          <input
            type="text"
            placeholder="Search identities (name or ID)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchIdentities()}
          />
          <button onClick={searchIdentities}>Search</button>
          {loading && <span className="loader">Loading...</span>}
        </div>

        <div ref={cyRef} className="cy-container" />
      </div>

      <div className="identity-sidebar">
        {selectedIdentity ? (
          <div className="details-panel">
            <h3>Identity Details</h3>
            <div className="info-grid">
              <strong>ID:</strong> <span>{selectedIdentity.id}</span>
              <strong>Name:</strong> <span>{selectedIdentity.name}</span>
              <strong>Type:</strong> <span className={`badge ${selectedIdentity.type}`}>{selectedIdentity.type}</span>
              <strong>Provider:</strong> <span className={`badge ${selectedIdentity.provider}`}>{selectedIdentity.provider}</span>
            </div>

            <button className="primary-btn" onClick={findEscalation}>
              Find Escalation Paths
            </button>

            {paths.length > 0 && (
              <div className="paths-list">
                <h4>Potential Paths ({paths.length})</h4>
                {paths.map((path, idx) => (
                  <div key={idx} className="path-item">
                    <p>Risk Score: {(path.risk_score * 100).toFixed(0)}%</p>
                    <div className="path-visual">
                      {path.nodes.map((n, i) => (
                        <span key={i}>
                          {n.name}
                          {i < path.nodes.length - 1 && ' → '}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="empty-state">
            <p>Select a node to view details and escalation paths</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default IdentityGraph

export default IdentityGraph