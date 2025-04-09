from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FeedbackBase(BaseModel):
    feedback: str

class FeedbackCreate(FeedbackBase):
    pass 

class FeedbackResponse(FeedbackBase):
    id: int
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True