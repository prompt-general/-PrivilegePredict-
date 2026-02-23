import React, { useState, useEffect } from 'react'
import { getEvaluationHistory } from '../api'

const AuditLog = () => {
    const [history, setHistory] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await getEvaluationHistory()
                setHistory(res.data)
            } catch (err) {
                console.error('Audit load error:', err)
            } finally {
                setLoading(false)
            }
        }
        fetchHistory()
    }, [])

    if (loading) return <div className="loader">Loading audit logs...</div>

    return (
        <div className="audit-container">
            <header className="dashboard-header">
                <h1>Evaluation Audit Trail</h1>
                <p className="subtitle">Historical record of all blocked and approved IAM changes</p>
            </header>

            <div className="audit-table-wrapper">
                <table className="audit-table">
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Identity</th>
                            <th>Risk Score</th>
                            <th>Status</th>
                            <th>Reasons</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.map(evalItem => (
                            <tr key={evalItem.id} className={`status-${evalItem.decision}`}>
                                <td className="time-col">{new Date(evalItem.created_at).toLocaleString()}</td>
                                <td className="id-col">
                                    <strong>{evalItem.identity_name}</strong>
                                    <span className="sub-text">{evalItem.identity_id.split('::').pop()}</span>
                                </td>
                                <td className="score-col">
                                    <span className={`score-badge ${evalItem.risk_score > 70 ? 'high' : 'low'}`}>
                                        {evalItem.risk_score.toFixed(1)}
                                    </span>
                                </td>
                                <td className="status-col">
                                    <span className={`status-pill ${evalItem.decision}`}>
                                        {evalItem.decision.toUpperCase()}
                                    </span>
                                </td>
                                <td className="reasons-col">
                                    <ul className="reason-small-list">
                                        {evalItem.reasons.map((r, i) => <li key={i}>{r}</li>)}
                                    </ul>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default AuditLog
