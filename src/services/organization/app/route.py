from fastapi import APIRouter, HTTPException
import json
import os
import schema

router = APIRouter()

with open('dummy.json', "r") as f:
    organizations = json.load(f)

@router.get("/{organization_id}", response_model=schema.OrganizationResponse)
def get_organization(organization_id: int):
    """
    Get organization information by id
    """
    for org in organizations:
        if org["id"] == organization_id:
            return org
    raise HTTPException(status_code=404, detail="Organization not found")

@router.get("/{organization_id}/exists")
def check_organization_exists(organization_id: int):
    """
    Check if organization exists
    """
    for org in organizations:
        if org["id"] == organization_id:
            return {"exists": True}
    raise HTTPException(status_code=404, detail="Organization not found")