from pydantic import BaseModel
from typing import List, Dict, Any
from .identity import Identity

class PathNode(BaseModel):
    id: str
    type: str
    name: str
    provider: str

class PathRelationship(BaseModel):
    source: str
    target: str
    type: str  # "ASSUMES", "MEMBER_OF", "ATTACHED_POLICY", etc.
    properties: Dict[str, Any]

class Path(BaseModel):
    nodes: List[PathNode]
    relationships: List[PathRelationship]
    risk_score: float