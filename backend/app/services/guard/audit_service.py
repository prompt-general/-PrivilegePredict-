import json
from datetime import datetime
from typing import Dict, Any
from ...models.audit import EvaluationAudit
from ...models.guard import ProposedChange, GuardDecision
# In a real app, we'd use a database session
# For this MVP, we simulate storing to a database or a feature log

class AuditService:
    """Handles archival of CI evaluations and feature extraction for ML training"""

    @staticmethod
    def log_evaluation(tenant_id: str, change: ProposedChange, decision: GuardDecision, features: Dict[str, Any]):
        """
        Stores evaluation details and extracted features.
        This data will be used to train future predictive ML models.
        """
        audit_entry = {
            "evaluation_id": decision.evaluation_id,
            "tenant_id": tenant_id,
            "identity_id": change.identity_id,
            "risk_score": decision.risk_score,
            "decision": decision.status,
            "new_escalation": decision.new_escalation_path,
            "reasons": decision.reasons,
            "features": features,
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate PostgreSQL entry
        print(f"Audit Logged: {decision.evaluation_id} for identity {change.identity_id}")
        
        # In actual implementation:
        # session.add(EvaluationAudit(...))
        # session.commit()
        
        # Also log to a feature store (e.g. JSONLines or feature-specific table)
        return audit_entry
