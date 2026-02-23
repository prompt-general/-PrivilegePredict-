from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class Identity(BaseModel):
    id: str
    provider: str  # "aws" | "azure"
    type: str  # "user" | "role" | "service_principal" | "group"
    name: str
    account_id: Optional[str] = None
    risk_score: Optional[float] = None
    high_privilege: Optional[bool] = False
    used_permissions: Optional[List[str]] = None
    unused_permissions: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None