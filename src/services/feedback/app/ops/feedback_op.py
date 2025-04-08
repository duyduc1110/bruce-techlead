from sqlalchemy.orm import Session
from typing import List
import httpx
from fastapi import HTTPException
from .. import models, schemas

ORGANIZATION_SERVICE_URL = "http://organization-service:8000/api/organizations"

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

def create_feedback_db(organization_id: int, feedback_data: schemas.FeedbackCreate, db: Session) -> models.Feedback:
    verify_organization_exists(organization_id)
    
    db_feedback = models.Feedback(
        organization_id=organization_id,
        feedback=feedback_data.feedback
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedbacks_db(organization_id: int, db: Session) -> List[models.Feedback]:
    verify_organization_exists(organization_id)
    
    return db.query(models.Feedback).filter(
        models.Feedback.organization_id == organization_id,
        models.Feedback.is_deleted == False
    ).all()

def delete_all_feedbacks_db(organization_id: int, db: Session) -> None:
    verify_organization_exists(organization_id)
    
    feedbacks = db.query(models.Feedback).filter(
        models.Feedback.organization_id == organization_id,
        models.Feedback.is_deleted == False
    ).all()
    
    for feedback in feedbacks:
        feedback.is_deleted = True
    
    db.commit()