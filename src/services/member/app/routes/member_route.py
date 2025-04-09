from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app import schemas, ops, db as database

router = APIRouter()

@router.post("/{organization_id}/members", 
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.MemberResponse)
def create_member(
    organization_id: int,
    member: schemas.MemberCreate = None,
    db: Session = Depends(database.get_db)
):
    """
    Create a new member for a specific organization.
    
    ## Path Parameters
    - **organization_id**: The ID of the organization to create member for
    
    ## Request Body
    - **first_name**: First name of the member
    - **last_name**: Last name of the member
    - **login**: Login name of the member
    - **avatar_url**: Avatar URL of the member
    - **followers**: Number of followers
    - **following**: Number of following
    - **title**: Title of the member
    - **email**: Email of the member
    
    ## Responses
    - **201**: Feedback created successfully
    - **404**: Organization not found
    - **503**: Organization service unavailable
    """
    try:
        result = ops.member_op.create_member_db(organization_id, member, db)
        return result
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

@router.get("/{organization_id}/members", 
            status_code=status.HTTP_200_OK,
            response_model=List[schemas.MemberResponse])
def get_members(
    organization_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Retrieve all non-deleted members for a specific organization.
    
    ## Path Parameters
    - **organization_id**: The ID of the organization to get members
    
    ## Responses
    - **200**: List of members returned
    - **404**: Organization not found
    - **503**: Organization service unavailable
    """
    try:
        results = ops.member_op.get_member_db(organization_id, db)
        return results
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

@router.delete("/{organization_id}/members", status_code=status.HTTP_200_OK)
def delete_members(
    organization_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Soft-delete all members for a specific organization.
    
    ## Path Parameters
    - **organization_id**: The ID of the organization to delete feedbacks for
    
    ## Responses
    - **200**: Feedbacks deleted successfully
    - **404**: Organization not found
    - **503**: Organization service unavailable
    """
    try:
        ops.member_op.delete_all_members_db(organization_id, db)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "All feedbacks deleted successfully"}
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})