from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class EffectivePermission(BaseModel):
    """Represents the effective permissions for an identity"""
    identity_id: str
    provider: str
    identity_type: str
    identity_name: str
    used_permissions: List[str]
    granted_permissions: List[str]
    unused_permissions: List[str]
    over_permissive: bool
    risk_score: float
    last_updated: datetime
    usage_window_days: int

class PermissionEvent(BaseModel):
    """Represents a normalized permission event from CloudTrail or Azure Activity Logs"""
    event_id: str
    timestamp: datetime
    provider: str  # "aws" | "azure"
    identity_id: str
    action: str
    resource: str
    source_ip: str
    user_agent: str

class PolicyRecommendation(BaseModel):
    """Represents a least-privilege policy recommendation"""
    identity_id: str
    identity_name: str
    provider: str
    recommended_policy_json: Dict[str, Any]
    recommended_policy_terraform: str
    recommended_policy_cloudformation: Optional[str] = None
    risk_reduction: float
    created_at: datetime

class Alert(BaseModel):
    """Represents a security alert for risky IAM changes"""
    alert_id: str
    identity_id: str
    identity_name: str
    provider: str
    alert_type: str  # "NEW_PRIVILEGE" | "OVER_PERMISSIVE" | "ANOMALOUS_BEHAVIOR"
    description: str
    severity: str  # "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
    timestamp: datetime
    resolved: bool = False