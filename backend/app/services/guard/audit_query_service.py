from typing import List, Dict, Any
from datetime import datetime
from ..graph.database import get_db_connection
# In a real app, this would query the PostgreSQL table 'evaluations'
# For the MVP, we'll simulate some mock audit data if the database is empty

def get_evaluation_history(tenant_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves the history of CI evaluations for a tenant"""
    
    # Mock data for demonstration
    return [
        {
            "id": "eval-9999",
            "identity_id": "aws::123456789012::role::unprivileged-app-role",
            "identity_name": "unprivileged-app-role",
            "risk_score": 92.5,
            "decision": "blocked",
            "reasons": [
                "Proposed changes introduce a new privilege escalation path to administrative access.",
                "Adding highly sensitive permission: iam:PassRole",
                "Permissions are scoped to all resources ('*'), increasing blast radius."
            ],
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "eval-8821",
            "identity_id": "aws::123456789012::role::lambda-exec-role",
            "identity_name": "lambda-exec-role",
            "risk_score": 87.5,
            "decision": "blocked",
            "reasons": ["Added iam:PassRole", "Introduced escalation path"],
            "created_at": "2024-03-21T14:30:00Z"
        },
        {
            "id": "eval-8822",
            "identity_id": "aws::123456789012::user::dev-user-01",
            "identity_name": "dev-user-01",
            "risk_score": 42.0,
            "decision": "approved",
            "reasons": ["Standard S3 read permissions"],
            "created_at": "2024-03-21T15:10:00Z"
        },
        {
            "id": "eval-8823",
            "identity_id": "aws::123456789012::role::admin-role-update",
            "identity_name": "admin-role",
            "risk_score": 95.0,
            "decision": "blocked",
            "reasons": ["Adding *:* wildcard", "Modified trust relationship"],
            "created_at": "2024-03-22T09:00:00Z"
        }
    ]
