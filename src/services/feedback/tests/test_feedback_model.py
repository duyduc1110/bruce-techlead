import pytest
import httpx

from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.db import Base, get_db
from app.models.feedback_model import Feedback
from app.schemas.feedback_schema import FeedbackCreate, FeedbackResponse
from app.ops.feedback_op import create_feedback_db, get_feedbacks_db, delete_all_feedbacks_db, verify_organization_exists
from app.main import app


# Model and schema tests

def test_feedback_model(db_session):
    """Test the Feedback model."""
    # Create a feedback using the model directly
    feedback = Feedback(
        organization_id=1,
        feedback="Model test"
    )
    db_session.add(feedback)
    db_session.commit()
    
    # Verify attributes
    assert feedback.id is not None
    assert feedback.organization_id == 1
    assert feedback.feedback == "Model test"
    assert feedback.is_deleted == False
    assert feedback.created_at is not None