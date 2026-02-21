import React, { useState, useEffect } from 'react'
import axios from 'axios'

const IdentityList = () => {
  const [identities, setIdentities] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchIdentities = async () => {
      try {
        const response = await axios.get('/api/identities')
        setIdentities(response.data)
        setLoading(false)
      } catch (err) {
        setError('Failed to fetch identities')
        setLoading(false)
      }
    }

    fetchIdentities()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div className="identity-list">
      <h2>Identities</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Provider</th>
            <th>Account ID</th>
          </tr>
        </thead>
        <tbody>
          {identities.map((identity) => (
            <tr key={identity.id}>
              <td>{identity.name}</td>
              <td>{identity.type}</td>
              <td>{identity.provider}</td>
              <td>{identity.account_id || 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default IdentityList