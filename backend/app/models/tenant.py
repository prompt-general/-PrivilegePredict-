from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

class Tenant(BaseModel):
    id: str = str(uuid.uuid4())
    name: str
    plan: str  # "free" | "pro" | "enterprise"
    created_at: datetime = datetime.now()

class CloudAccount(BaseModel):
    id: str = str(uuid.uuid4())
    tenant_id: str
    provider: str  # "aws" | "azure"
    external_id: str  # AWS Account ID or Azure Tenant ID
    name: str
    status: str = "active"

class RiskSnapshot(BaseModel):
    total_identities: int
    high_risk_count: int
    over_permissive_percent: float
    recent_alerts_count: int
