from fastapi import APIRouter, HTTPException
from typing import List
from ..models.identity import Identity
from ..services.identity_service import get_all_identities, get_identity_by_id, get_full_graph

router = APIRouter()

@router.get("/graph")
async def get_graph_data():
    """Get full graph data including nodes and edges"""
    try:
        return get_full_graph()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Identity])
async def list_identities():
    """List all identities in the graph"""
    try:
        identities = get_all_identities()
        return identities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{identity_id}", response_model=Identity)
async def get_identity(identity_id: str):
    """Get an identity by ID"""
    try:
        identity = get_identity_by_id(identity_id)
        if not identity:
            raise HTTPException(status_code=404, detail="Identity not found")
        return identity
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))