from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..models.path import Path
from ..services.path_service import find_escalation_paths

router = APIRouter()

@router.get("/", response_model=List[Path])
async def get_paths(
    source: str = Query(..., description="Source identity ID"),
    target: str = Query(None, description="Target identity ID (optional)")
):
    """Find escalation paths between identities"""
    try:
        paths = find_escalation_paths(source, target)
        return paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))