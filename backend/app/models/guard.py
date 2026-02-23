from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ProposedChange(BaseModel):
    identity_id: str
    identity_name: str
    identity_type: str  # "role", "user", "group"
    added_permissions: List[str] = []
    removed_permissions: List[str] = []
    resource_scope: str = "*"
    provider: str = "aws"

class GuardDecision(BaseModel):
    status: str  # "approved" | "warning" | "blocked"
    risk_score: float
    reasons: List[str]
    new_escalation_path: bool
    evaluation_id: str
    timestamp: datetime = datetime.now()

class CIRequest(BaseModel):
    tenant_id: str = "default"
    plan_json: Dict[str, Any]
    provider: str = "aws"
    block_threshold: Optional[float] = 80.0
    warning_threshold: Optional[float] = 50.0
