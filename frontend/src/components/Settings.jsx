import React, { useState, useEffect } from 'react'
import { getRiskSummary } from '../api'

const Settings = () => {
    const [thresholds, setThresholds] = useState({
        block: 80,
        warning: 50
    })
    const [saved, setSaved] = useState(false)

    const handleSave = () => {
        // In a real scenario, this would call an API like updateTenantConfig(thresholds)
        localStorage.setItem('pp_thresholds', JSON.stringify(thresholds))
        setSaved(true)
        setTimeout(() => setSaved(false), 3000)
    }

    return (
        <div className="settings-container">
            <header className="dashboard-header">
                <h1>Guard Policy Settings</h1>
                <p className="subtitle">Configure risk thresholds for CI/CD enforcement</p>
            </header>

            <div className="settings-panel">
                <div className="settings-group">
                    <label>
                        Hard Block Threshold (0-100)
                        <span className="help-text">Any change with a risk score above this will fail the CI pipeline.</span>
                    </label>
                    <input
                        type="range"
                        min="1" max="100"
                        value={thresholds.block}
                        onChange={(e) => setThresholds({ ...thresholds, block: parseInt(e.target.value) })}
                    />
                    <span className="range-value">{thresholds.block}</span>
                </div>

                <div className="settings-group">
                    <label>
                        Warning Threshold (0-100)
                        <span className="help-text">Changes above this score will trigger a warning and require approval.</span>
                    </label>
                    <input
                        type="range"
                        min="1" max="100"
                        value={thresholds.warning}
                        onChange={(e) => setThresholds({ ...thresholds, warning: parseInt(e.target.value) })}
                    />
                    <span className="range-value">{thresholds.warning}</span>
                </div>

                <div className="settings-actions">
                    <button className="primary-btn" onClick={handleSave}>Save Configuration</button>
                    {saved && <span className="save-confirmed">✅ Policy updated successfully</span>}
                </div>
            </div>

            <div className="policy-preview">
                <h3>Current Policy Logic</h3>
                <ul className="preview-list">
                    <li className="block">Score <strong>&ge; {thresholds.block}</strong>: Hard Block (Merge Blocked)</li>
                    <li className="warning">Score <strong>&ge; {thresholds.warning}</strong>: Soft Warning (Review Required)</li>
                    <li className="allow">Score <strong>&lt; {thresholds.warning}</strong>: Auto-Approved</li>
                </ul>
            </div>
        </div>
    )
}

export default Settings
