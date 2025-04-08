from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class FeedbackBase(BaseModel):
    feedback: str

class FeedbackCreate(FeedbackBase):
    pass 

class FeedbackResponse(FeedbackBase):
    id: int
    organization_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True