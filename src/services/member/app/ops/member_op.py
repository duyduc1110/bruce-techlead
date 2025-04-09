import httpx
import os

from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from app import models, schemas

ORGANIZATION_SERVICE_URL = os.environ.get("ORGANIZATION_SERVICE_URL", "http://organization-service:18000/api/v1/organizations")

def verify_organization_exists(organization_id: int):
    with httpx.Client() as client:
        try:
            response = client.get(f"{ORGANIZATION_SERVICE_URL}/{organization_id}/exists")
            if response.status_code == 200:
                return True
            else:
                raise HTTPException(status_code=404, detail="Organization not found")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Organization service unavailable")

def create_member_db(organization_id: int, member_data: schemas.MemberCreate, db: Session) -> models.Member:
    verify_organization_exists(organization_id)
    
    db_member = models.Member(
        organization_id=organization_id,
        first_name=member_data.first_name,
        last_name=member_data.last_name,
        login=member_data.login,
        avatar_url=member_data.avatar_url,
        followers=member_data.followers,
        following=member_data.following,
        title=member_data.title,
        email=member_data.email,
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_member_db(organization_id: int, db: Session) -> List[models.Member]:
    verify_organization_exists(organization_id)
    
    return db.query(models.Member).filter(
        models.Member.organization_id == organization_id,
        models.Member.is_deleted == False
    ).order_by(models.Member.followers.desc()).all()

def delete_all_members_db(organization_id: int, db: Session) -> None:
    verify_organization_exists(organization_id)
    
    feedbacks = db.query(models.Member).filter(
        models.Member.organization_id == organization_id,
        models.Member.is_deleted == False
    ).all()
    
    for feedback in feedbacks:
        feedback.is_deleted = True
    
    db.commit()