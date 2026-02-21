from fastapi import APIRouter, HTTPException
from typing import List
from ..models.identity import Identity
from ..services.risk_service import get_high_risk_identities

router = APIRouter()

@router.get("/high-risk-identities", response_model=List[Identity])
async def list_high_risk_identities():
    """List all high-risk identities"""
    try:
        identities = get_high_risk_identities()
        return identities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))