import React, { useState, useEffect, useRef } from 'react'
import cytoscape from 'cytoscape'
import axios from 'axios'

const IdentityGraph = () => {
  const cyRef = useRef(null)
  const [cy, setCy] = useState(null)
  const [selectedIdentity, setSelectedIdentity] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    // Initialize Cytoscape
    const cyInstance = cytoscape({
      container: cyRef.current,
      elements: [],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#666',
            'label': 'data(name)',
            'color': '#fff',
            'text-valign': 'center',
            'text-halign': 'center'
          }
        },
        {
          selector: 'node[type = "user"]',
          style: {
            'background-color': '#66f'
          }
        },
        {
          selector: 'node[type = "role"]',
          style: {
            'background-color': '#f66'
          }
        },
        {
          selector: 'node[type = "group"]',
          style: {
            'background-color': '#6f6'
          }
        },
        {
          selector: 'node[type = "service_principal"]',
          style: {
            'background-color': '#ff6'
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(type)'
          }
        },
        {
          selector: 'edge[type = "ASSUMES"]',
          style: {
            'line-color': '#f00',
            'target-arrow-color': '#f00'
          }
        },
        {
          selector: 'edge[type = "MEMBER_OF"]',
          style: {
            'line-color': '#0f0',
            'target-arrow-color': '#0f0'
          }
        }
      ],
      layout: {
        name: 'cose',
        animate: true
      }
    })

    setCy(cyInstance)

    // Load initial data
    loadGraphData(cyInstance)

    // Cleanup
    return () => {
      if (cyInstance) {
        cyInstance.destroy()
      }
    }
  }, [])

  const loadGraphData = async (cyInstance) => {
    try {
      // In a real implementation, this would fetch from our API
      // For now, we'll use sample data
      const sampleData = {
        nodes: [
          { data: { id: 'aws::123456789012::user::alice', name: 'alice', type: 'user', provider: 'aws' } },
          { data: { id: 'aws::123456789012::role::admin-role', name: 'admin-role', type: 'role', provider: 'aws' } },
          { data: { id: 'aws::123456789012::group::developers', name: 'developers', type: 'group', provider: 'aws' } },
          { data: { id: 'azure::abcd1234-efgh-5678::user::bob', name: 'bob', type: 'user', provider: 'azure' } },
          { data: { id: 'azure::abcd1234-efgh-5678::service_principal::app-sp', name: 'app-sp', type: 'service_principal', provider: 'azure' } }
        ],
        edges: [
          { data: { source: 'aws::123456789012::user::alice', target: 'aws::123456789012::group::developers', type: 'MEMBER_OF' } },
          { data: { source: 'aws::123456789012::user::alice', target: 'aws::123456789012::role::admin-role', type: 'ASSUMES' } }
        ]
      }

      cyInstance.add(sampleData.nodes)
      cyInstance.add(sampleData.edges)

      // Fit the graph to the viewport
      cyInstance.fit()
    } catch (error) {
      console.error('Error loading graph data:', error)
    }
  }

  const handleNodeClick = (event) => {
    const node = event.target
    setSelectedIdentity(node.data())
  }

  const searchIdentities = async () => {
    if (!searchTerm) return

    try {
      // In a real implementation, this would search the API
      console.log('Searching for:', searchTerm)
    } catch (error) {
      console.error('Search error:', error)
    }
  }

  return (
    <div className="identity-graph">
      <h2>Identity Graph Visualization</h2>

      <div className="controls">
        <input
          type="text"
          placeholder="Search identities..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button onClick={searchIdentities}>Search</button>
      </div>

      <div
        ref={cyRef}
        style={{ width: '100%', height: '600px', border: '1px solid #ccc' }}
      />

      {selectedIdentity && (
        <div className="identity-details">
          <h3>Identity Details</h3>
          <p><strong>ID:</strong> {selectedIdentity.id}</p>
          <p><strong>Name:</strong> {selectedIdentity.name}</p>
          <p><strong>Type:</strong> {selectedIdentity.type}</p>
          <p><strong>Provider:</strong> {selectedIdentity.provider}</p>
        </div>
      )}
    </div>
  )
}

export default IdentityGraph