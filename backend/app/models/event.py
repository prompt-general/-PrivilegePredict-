from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CloudEvent(BaseModel):
    event_id: str
    timestamp: datetime
    provider: str  # "aws" | "azure"
    identity_id: str
    action: str
    service: str
    resource: Optional[str] = None
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None

class EffectivePermissionSummary(BaseModel):
    identity_id: str
    granted_count: int
    used_count: int
    over_permissive_count: int
    unused_actions: list[str]
    used_actions: list[str]
