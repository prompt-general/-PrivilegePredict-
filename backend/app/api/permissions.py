from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..models.permissions import EffectivePermission, PolicyRecommendation
from ..services.permissions.permission_service import get_effective_permissions, get_least_privilege_policy

router = APIRouter()

@router.get("/effective-permissions", response_model=List[EffectivePermission])
async def list_effective_permissions():
    """List effective permissions for all identities"""
    try:
        permissions = get_effective_permissions()
        return permissions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{identity_id}/effective-permissions", response_model=EffectivePermission)
async def get_identity_effective_permissions(identity_id: str):
    """Get effective permissions for a specific identity"""
    try:
        permission = get_effective_permissions(identity_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Identity not found")
        return permission
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{identity_id}/least-privilege", response_model=PolicyRecommendation)
async def get_least_privilege_policy_route(identity_id: str):
    """Get least-privilege policy recommendation for an identity"""
    try:
        policy = get_least_privilege_policy(identity_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Identity not found or no policy available")
        return policy
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))