from app.models.member_model import Member

def test_member_model(db_session):
    member = Member(
        organization_id=1,
        first_name="John",
        last_name="Doe",
        login="john123",
        avatar_url="https://example.com/avatar.jpg",
        followers=120,
        following=35,
        title="Software Engineer",
        email="john@example.com"
    )
    db_session.add(member)
    db_session.commit()
    
    assert member.id is not None
    assert member.organization_id == 1
    assert member.first_name == "John"
    assert member.last_name == "Doe"
    assert member.login == "john123"
    assert member.avatar_url == "https://example.com/avatar.jpg"
    assert member.followers == 120
    assert member.following == 35
    assert member.title == "Software Engineer"
    assert member.email == "john@example.com"
    assert member.is_deleted == False
    assert member.created_at is not None
    assert member.updated_at is None  