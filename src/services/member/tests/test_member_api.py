from app.models.member_model import Member

def test_create_member_api(client, db_session, mock_verify_organization):
    response = client.post(
        "/api/v1/organizations/1/members",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "login": "john123",
            "avatar_url": "https://example.com/avatar.jpg",
            "followers": 120,
            "following": 35,
            "title": "Software Engineer",
            "email": "john@example.com"
        }
    )
   
    assert response.status_code == 201

    data = response.json()
    assert data["organization_id"] == 1
    assert "id" in data
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["login"] == "john123"
    assert data["avatar_url"] == "https://example.com/avatar.jpg"
    assert data["followers"] == 120
    assert data["following"] == 35
    assert data["title"] == "Software Engineer"
    assert data["email"] == "john@example.com"
    assert data["created_at"] is not None
    assert data["updated_at"] is None


def test_get_members_api(client, db_session, mock_verify_organization):
    for i in range(3):
        db_session.add(Member(
            organization_id=1,
            first_name=f"John{i}",
            last_name=f"Doe{i}",
            login=f"john123_{i}",
            avatar_url=f"https://example.com/avatar{i}.jpg",
            followers=120 + i,
            following=35 + i,
            title=f"Software Engineer {i}",
            email=f"john{i}@example.com"
        ))
    db_session.commit()
    
    response = client.get("/api/v1/organizations/1/members")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    
    follower_list = [item["followers"] for item in data]
    assert follower_list == [122, 121, 120]

def test_delete_feedbacks_api(client, db_session, mock_verify_organization):
    for i in range(3):
        db_session.add(Member(
            organization_id=1,
            first_name=f"John{i}",
            last_name=f"Doe{i}",
            login=f"john123_{i}",
            avatar_url=f"https://example.com/avatar{i}.jpg",
            followers=120 + i,
            following=35 + i,
            title=f"Software Engineer {i}",
            email=f"john{i}@example.com"
        ))
    db_session.commit()
    
    response = client.delete("/api/v1/organizations/1/members")
    assert response.status_code == 200
    
    feedbacks = db_session.query(Member).filter(
        Member.organization_id == 1,
        Member.is_deleted == False
    ).all()
    assert len(feedbacks) == 0
    
    get_response = client.get("/api/v1/organizations/1/members")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0