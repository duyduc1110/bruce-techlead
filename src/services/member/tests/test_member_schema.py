from app.models.member_model import Member
from app.schemas.member_schema import MemberResponse

def test_member_schema(db_session):
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
    
    response_model = MemberResponse.model_validate(member, from_attributes=True)
    
    assert response_model.id == member.id
    assert response_model.organization_id == 1
    assert response_model.first_name == "John"
    assert response_model.last_name == "Doe"
    assert response_model.login == "john123"
    assert response_model.avatar_url == "https://example.com/avatar.jpg"
    assert response_model.followers == 120
    assert response_model.following == 35
    assert response_model.title == "Software Engineer"
    assert response_model.email == "john@example.com"
    assert response_model.created_at is not None
    assert response_model.updated_at is None