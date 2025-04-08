from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, ops, db as database

router = APIRouter()

@router.post("/{organization_id}/feedbacks", status_code=status.HTTP_201_CREATED)
def create_feedback(
    organization_id: int,
    feedback: schemas.FeedbackCreate = None,
    db: Session = Depends(database.get_db)
):
    """
    Create a new feedback for a specific organization.
    
    ## Path Parameters
    - **organization_id**: The ID of the organization to create feedback for
    
    ## Request Body
    - **feedback**: Feedback content
    
    ## Responses
    - **201**: Feedback created successfully
    - **404**: Organization not found
    - **503**: Organization service unavailable
    """
    try:
        result = ops.feedback_op.create_feedback_db(organization_id, feedback, db)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Feedback created successfully", "data": schemas.FeedbackResponse.from_orm(result).dict()}
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

@router.get("/{organization_id}/feedbacks", status_code=status.HTTP_200_OK)
def get_feedbacks(
    organization_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Retrieve all non-deleted feedbacks for a specific organization.
    
    ## Path Parameters
    - **organization_id**: The ID of the organization to get feedbacks for
    
    ## Responses
    - **200**: List of feedbacks returned
    - **404**: Organization not found
    - **503**: Organization service unavailable
    """
    try:
        results = ops.feedback_op.get_feedbacks_db(organization_id, db)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Feedbacks retrieved successfully",
                "data": [schemas.FeedbackResponse.from_orm(result).dict() for result in results]
            }
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

@router.delete("/{organization_id}/feedbacks", status_code=status.HTTP_200_OK)
def delete_feedbacks(
    organization_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Soft-delete all feedbacks for a specific organization.
    
    ## Path Parameters
    - **organization_id**: The ID of the organization to delete feedbacks for
    
    ## Responses
    - **200**: Feedbacks deleted successfully
    - **404**: Organization not found
    - **503**: Organization service unavailable
    """
    try:
        ops.feedback_op.delete_all_feedbacks_db(organization_id, db)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "All feedbacks deleted successfully"}
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})