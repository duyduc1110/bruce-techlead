import pytest
import httpx

from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from app.models.feedback_model import Feedback
from app.schemas.feedback_schema import FeedbackCreate, FeedbackResponse
from app.ops.feedback_op import create_feedback_db, get_feedbacks_db, delete_all_feedbacks_db, verify_organization_exists
from app.main import app


def test_verify_organization_exists_success():
    with patch('httpx.Client') as mock_client:
        mock_response = MagicMock(status_code=200)
        mock_instance = mock_client.return_value.__enter__.return_value
        mock_instance.get.return_value = mock_response
        
        result = verify_organization_exists(1)
        assert result is True
        mock_instance.get.assert_called_once()

def test_verify_organization_exists_failure():
    with patch('httpx.Client') as mock_client:
        mock_response = MagicMock(status_code=404)
        mock_instance = mock_client.return_value.__enter__.return_value
        mock_instance.get.return_value = mock_response
        
        with pytest.raises(HTTPException) as excinfo:
            verify_organization_exists(1)
        assert excinfo.value.status_code == 404

def test_verify_organization_exists_service_unavailable():
    with patch('httpx.Client') as mock_client:
        mock_instance = mock_client.return_value.__enter__.return_value
        mock_instance.get.side_effect = httpx.RequestError("Service unavailable")
        
        with pytest.raises(HTTPException) as excinfo:
            verify_organization_exists(1)
        assert excinfo.value.status_code == 503

def test_create_feedback_op(db_session, mock_verify_organization):
    feedback_data = FeedbackCreate(feedback="Test feedback")
    result = create_feedback_db(1, feedback_data, db_session)
    
    assert result is not None
    assert result.feedback == "Test feedback"
    assert result.organization_id == 1
    assert result.is_deleted == False
    
    db_feedback = db_session.query(Feedback).filter(Feedback.id == result.id).first()
    assert db_feedback is not None
    assert db_feedback.feedback == "Test feedback"

def test_get_feedbacks_op(db_session, mock_verify_organization):
    feedback1 = Feedback(organization_id=1, feedback="Feedback 1")
    feedback2 = Feedback(organization_id=1, feedback="Feedback 2")
    feedback3 = Feedback(organization_id=2, feedback="Other org")
    db_session.add_all([feedback1, feedback2, feedback3])
    db_session.commit()
    
    results = get_feedbacks_db(1, db_session)
    
    assert len(results) == 2
    feedbacks = sorted([f.feedback for f in results])
    assert feedbacks == ["Feedback 1", "Feedback 2"]

def test_delete_feedbacks_op(db_session, mock_verify_organization):
    feedback1 = Feedback(organization_id=1, feedback="Feedback 1")
    feedback2 = Feedback(organization_id=1, feedback="Feedback 2")
    feedback3 = Feedback(organization_id=2, feedback="Other org")
    db_session.add_all([feedback1, feedback2, feedback3])
    db_session.commit()
    
    delete_all_feedbacks_db(1, db_session)
    
    org1_feedbacks = db_session.query(Feedback).filter(
        Feedback.organization_id == 1
    ).all()
    for f in org1_feedbacks:
        assert f.is_deleted == True
    
    org2_feedbacks = db_session.query(Feedback).filter(
        Feedback.organization_id == 2
    ).all()
    for f in org2_feedbacks:
        assert f.is_deleted == False
    
    results = get_feedbacks_db(1, db_session)
    assert len(results) == 0

