from fastapi import APIRouter, HTTPException
from typing import List
from ..models.identity import Identity
from ..services.risk_service import get_high_risk_identities, get_recent_alerts
from ..services.tenant_service import get_tenant_risk_summary
from ..models.tenant import RiskSnapshot

router = APIRouter()

@router.get("/summary", response_model=RiskSnapshot)
async def get_risk_summary(tenant_id: str = "default"):
    """Get high-level risk overview for the dashboard"""
    try:
        return get_tenant_risk_summary(tenant_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts")
async def list_recent_alerts():
    """List recent security alerts"""
    try:
        return get_recent_alerts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/high-risk-identities", response_model=List[Identity])
async def list_high_risk_identities():
    """List all high-risk identities"""
    try:
        identities = get_high_risk_identities()
        return identities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))