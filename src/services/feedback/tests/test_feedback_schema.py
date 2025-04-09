from app.models.feedback_model import Feedback
from app.schemas.feedback_schema import FeedbackResponse

def test_feedback_schema(db_session):
    db_feedback = Feedback(
        organization_id=1,
        feedback="Schema test"
    )
    db_session.add(db_feedback)
    db_session.commit()
    
    response_model = FeedbackResponse.model_validate(db_feedback, from_attributes=True)
    
    assert response_model.id == db_feedback.id
    assert response_model.organization_id == 1
    assert response_model.feedback == "Schema test"
    assert response_model.created_at is not None