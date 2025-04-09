from app.models.feedback_model import Feedback


def test_create_feedback_api(client, db_session, mock_verify_organization):
    response = client.post(
        "/api/v1/organizations/1/feedbacks",
        json={"feedback": "API test create feedback"}
    )
    assert response.status_code == 201

    data = response.json()
    assert data["feedback"] == "API test create feedback"
    assert data["organization_id"] == 1
    assert "id" in data

def test_get_feedbacks_api(client, db_session, mock_verify_organization):
    feedback1 = Feedback(organization_id=1, feedback="API Feedback 1")
    feedback2 = Feedback(organization_id=1, feedback="API Feedback 2")
    db_session.add_all([feedback1, feedback2])
    db_session.commit()
    
    response = client.get("/api/v1/organizations/1/feedbacks")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    
    feedbacks = [item["feedback"] for item in data]
    assert "API Feedback 1" in feedbacks
    assert "API Feedback 2" in feedbacks

def test_delete_feedbacks_api(client, db_session, mock_verify_organization):
    feedback = Feedback(organization_id=1, feedback="To be deleted")
    db_session.add(feedback)
    db_session.commit()
    
    response = client.delete("/api/v1/organizations/1/feedbacks")
    assert response.status_code == 200
    
    feedbacks = db_session.query(Feedback).filter(
        Feedback.organization_id == 1,
        Feedback.is_deleted == False
    ).all()
    assert len(feedbacks) == 0
    
    get_response = client.get("/api/v1/organizations/1/feedbacks")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0