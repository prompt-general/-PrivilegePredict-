import React, { useState, useEffect, useRef } from 'react'
import cytoscape from 'cytoscape'
import { getGraphData, getPaths, getLeastPrivilege } from '../api'

const IdentityGraph = () => {
  const cyRef = useRef(null)
  const [cy, setCy] = useState(null)
  const [selectedIdentity, setSelectedIdentity] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(false)
  const [paths, setPaths] = useState([])
  const [recommendation, setRecommendation] = useState(null)
  const [showPolicy, setShowPolicy] = useState(false)

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
            'border-color': '#ff9900'
          }
        },
        {
          selector: 'node[provider = "azure"]',
          style: {
            'border-width': 2,
            'border-color': '#0078d4'
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
          selector: 'node[type = "policy"]',
          style: {
            'background-color': '#805ad5',
            'shape': 'rectangle'
          }
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
            'transition-duration': '0.5s',
            'width': node => node.isNode() ? '50px' : '4px'
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
      const response = await getGraphData()
      const { nodes, edges } = response.data

      const elements = [
        ...nodes.map(n => ({ data: { ...n } })),
        ...edges.map(e => ({ data: { ...e } }))
      ]

      cyInstance.elements().remove()
      cyInstance.add(elements)
      cyInstance.layout({ name: 'cose', animate: true }).run()
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

      if (cy && response.data.length > 0) {
        cy.elements().removeClass('highlighted')
        response.data.forEach(path => {
          path.nodes.forEach(node => {
            cy.getElementById(node.id).addClass('highlighted')
          })
          path.relationships.forEach(rel => {
            cy.edges(`[source = "${rel.source}"][target = "${rel.target}"]`).addClass('highlighted')
          })
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
        zoom: 1.5,
        duration: 500
      })
    }
  }

  return (
    <div className="identity-graph-container">
      <div className="identity-graph-main">
        <div className="controls-overlay">
          <input
            type="text"
            placeholder="Search identities..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchIdentities()}
          />
          <button onClick={searchIdentities}>Search</button>
          <button onClick={() => loadGraphData(cy)} style={{ background: '#4a5568', color: 'white' }}>Refresh</button>
          {loading && <span className="loader">Processing...</span>}
        </div>

        <div ref={cyRef} className="cy-container" />
      </div>

      <div className="identity-sidebar">
        {selectedIdentity ? (
          <div className="details-panel">
            <h3>Identity Details</h3>
            <div className="info-grid">
              <strong>ID:</strong> <span style={{ wordBreak: 'break-all' }}>{selectedIdentity.id}</span>
              <strong>Name:</strong> <span>{selectedIdentity.name}</span>
              <strong>Type:</strong> <span className={`badge ${selectedIdentity.type}`}>{selectedIdentity.type}</span>
              <strong>Provider:</strong> <span className={`badge ${selectedIdentity.provider}`}>{selectedIdentity.provider}</span>
            </div>

            {selectedIdentity.used_permissions && (
              <div className="usage-stats">
                <h4>Permission Intelligence</h4>
                <div className="usage-summary">
                  <div className="usage-item">
                    <strong>Actions Used</strong>
                    <span className="count success">{selectedIdentity.used_permissions.length}</span>
                  </div>
                  <div className="usage-item">
                    <strong>Actions Unused</strong>
                    <span className="count warning">{selectedIdentity.unused_permissions?.length || 0}</span>
                  </div>
                </div>

                {selectedIdentity.unused_permissions?.length > 0 && (
                  <div className="alert-box warning-glow">
                    ⚠️ <strong>Over-permissive Detected:</strong> {((selectedIdentity.unused_permissions.length / (selectedIdentity.used_permissions.length + selectedIdentity.unused_permissions.length)) * 100).toFixed(0)}% of permissions are never used.
                  </div>
                )}
              </div>
            )}

            <button className="primary-btn" onClick={findEscalation} disabled={loading}>
              {loading ? 'Analyzing...' : 'Find Escalation Paths'}
            </button>

            {paths.length > 0 ? (
              <div className="paths-list">
                <h4>Potential Paths ({paths.length})</h4>
                {paths.map((path, idx) => (
                  <div key={idx} className="path-item">
                    <p style={{ color: path.risk_score > 0.7 ? '#f56565' : '#ecc94b', fontWeight: 'bold' }}>
                      Risk Score: {(path.risk_score * 100).toFixed(0)}%
                    </p>
                    <div className="path-visual">
                      {path.nodes.map((n, i) => (
                        <span key={i}>
                          <span style={{ color: n.id === selectedIdentity.id ? '#38bdf8' : 'inherit' }}>{n.name}</span>
                          {i < path.nodes.length - 1 && ' → '}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : paths.length === 0 && !loading && (
              <p style={{ marginTop: '20px', fontSize: '0.8rem', color: '#94a3b8' }}>No escalation paths found yet.</p>
            )}
          </div>
        ) : (
          <div className="empty-state">
            <p>Select a node in the graph to analyze its privilege escalation risks.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default IdentityGraph