import React, { useState, useEffect } from 'react'
import { getIdentities } from '../api'

const IdentityList = () => {
  const [identities, setIdentities] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchIdentities = async () => {
      try {
        const response = await getIdentities()
        setIdentities(response.data)
      } catch (err) {
        setError('Failed to fetch identities. Ensure the backend is running.')
      } finally {
        setLoading(false)
      }
    }

    fetchIdentities()
  }, [])

  if (loading) return <div className="loader-container"><span className="loader">Loading identities...</span></div>
  if (error) return <div className="error-container">{error}</div>

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