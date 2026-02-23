import React, { useState, useEffect } from 'react'
import { getAlerts } from '../api'

const AlertFeed = () => {
    const [alerts, setAlerts] = useState([])

    useEffect(() => {
        const fetchAlerts = async () => {
            try {
                const response = await getAlerts()
                setAlerts(response.data)
            } catch (error) {
                console.error('Error fetching alerts:', error)
            }
        }

        fetchAlerts()
        const interval = setInterval(fetchAlerts, 5000) // Poll every 5s for the demo
        return () => clearInterval(interval)
    }, [])

    if (alerts.length === 0) return null

    return (
        <div className="alert-feed">
            <h4>Recent Security Events</h4>
            <div className="alert-list">
                {alerts.map((alert, idx) => (
                    <div key={idx} className="alert-card">
                        <div className="alert-header">
                            <span className="alert-type">IAM_CHANGE</span>
                            <span className="alert-time">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                        </div>
                        <p className="alert-msg">{alert.message}</p>
                        <span className="alert-target">{alert.identity_name}</span>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default AlertFeed
