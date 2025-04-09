from sqlalchemy import Column, Integer, Text, Boolean, DateTime, String
from sqlalchemy.sql import func
from app.db import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, nullable=False)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    login = Column(String(32), nullable=False)
    avatar_url = Column(String(256), nullable=False)
    followers = Column(Integer, nullable=False, default=0)
    following = Column(Integer, nullable=False, default=0)
    title = Column(String(32), nullable=False)
    email = Column(String(256), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

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