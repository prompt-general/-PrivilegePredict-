from pydantic import BaseModel
from typing import Optional, Dict, Any

class Identity(BaseModel):
    id: str
    provider: str  # "aws" | "azure"
    type: str  # "user" | "role" | "service_principal" | "group"
    name: str
    account_id: Optional[str] = None
    risk_score: Optional[float] = None
    properties: Optional[Dict[str, Any]] = None