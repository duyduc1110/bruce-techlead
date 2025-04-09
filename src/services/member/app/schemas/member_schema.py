from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class MemberCreate(BaseModel):
    first_name: str
    last_name: str
    login: str
    avatar_url: str
    followers: int
    following: int
    title: str
    email: str

class MemberResponse(MemberCreate):
    id: int
    organization_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True


"""
{
"first_name": "John",
"last_name": "Doe",
"login": "john123",
"avatar_url": "https://example.com/avatar.jpg",
"followers": 120,
"following": 35,
"title": "Senior Developer",
"email": "john@example.com"
}
"""