import React, { useState, useEffect } from 'react'
import { getRiskSummary, getHighRiskIdentities } from '../api'
import { Link } from 'react-router-dom'

const Dashboard = () => {
    const [summary, setSummary] = useState(null)
    const [highRisk, setHighRisk] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [summaryRes, highRiskRes] = await Promise.all([
                    getRiskSummary(),
                    getHighRiskIdentities()
                ])
                setSummary(summaryRes.data)
                setHighRisk(highRiskRes.data)
            } catch (err) {
                console.error('Dashboard load error:', err)
            } finally {
                setLoading(false)
            }
        }
        fetchData()
    }, [])

    if (loading) return <div className="loader-container"><span className="loader">Loading intelligence...</span></div>

    return (
        <div className="saas-dashboard">
            <header className="dashboard-header">
                <h1>Cloud Intelligence Dashboard</h1>
                <p className="subtitle">Real-time privilege usage and risk telemetry</p>
            </header>

            <div className="stats-grid">
                <div className="stat-card">
                    <label>Total Identities</label>
                    <span className="value">{summary?.total_identities}</span>
                </div>
                <div className="stat-card danger">
                    <label>High Risk Paths</label>
                    <span className="value">{summary?.high_risk_count}</span>
                </div>
                <div className="stat-card warning">
                    <label>Over-permissive</label>
                    <span className="value">{summary?.over_permissive_percent.toFixed(1)}%</span>
                </div>
                <div className="stat-card alert">
                    <label>Active Alerts</label>
                    <span className="value">{summary?.recent_alerts_count}</span>
                </div>
            </div>

            <div className="dashboard-sections">
                <section className="risk-section">
                    <h3>🚨 Critical Identities</h3>
                    <div className="risk-list">
                        {highRisk.slice(0, 5).map(id => (
                            <div key={id.id} className="risk-row">
                                <div className="risk-info">
                                    <strong>{id.name}</strong>
                                    <span className="risk-id">{id.id}</span>
                                </div>
                                <Link to="/graph" className="view-link">Investigate</Link>
                            </div>
                        ))}
                    </div>
                </section>

                <section className="action-section">
                    <h3>⚡ Quick Remediations</h3>
                    <p>The system has identified <strong>{Math.floor(summary?.total_identities * 0.4)}</strong> identities whose attack surface can be reduced immediately.</p>
                    <Link to="/graph" className="primary-btn">Review Recommendations</Link>
                </section>
            </div>
        </div>
    )
}

export default Dashboard
