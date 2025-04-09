from app.models.feedback_model import Feedback


def test_feedback_model(db_session):
    feedback = Feedback(
        organization_id=1,
        feedback="Model test"
    )
    db_session.add(feedback)
    db_session.commit()
    
    assert feedback.id is not None
    assert feedback.organization_id == 1
    assert feedback.feedback == "Model test"
    assert feedback.is_deleted == False
    assert feedback.created_at is not None