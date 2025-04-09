import pytest
import httpx

from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from app.models.member_model import Member
from app.schemas.member_schema import MemberCreate, MemberResponse
from app.ops.member_op import create_member_db, get_member_db, delete_all_members_db, verify_organization_exists


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

def test_create_member_op(db_session, mock_verify_organization):
    feedback_data = MemberCreate(
        first_name="John",
        last_name="Doe",
        login="john123",
        avatar_url="https://example.com/avatar.jpg",
        followers=120,
        following=35,
        title="Software Engineer",
        email="john@example.com"
    )
    result = create_member_db(1, feedback_data, db_session)
    
    assert result is not None
    assert isinstance(result, Member)
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.login == "john123"
    assert result.avatar_url == "https://example.com/avatar.jpg"
    assert result.followers == 120
    assert result.following == 35
    assert result.title == "Software Engineer"
    assert result.email == "john@example.com"
    
    db_member = db_session.query(Member).filter(Member.id == result.id).first()
    assert db_member is not None
    assert db_member.id == result.id
    assert db_member.organization_id == 1
    assert db_member.first_name == "John"
    assert db_member.last_name == "Doe"
    assert db_member.login == "john123"
    assert db_member.avatar_url == "https://example.com/avatar.jpg"
    assert db_member.followers == 120
    assert db_member.following == 35
    assert db_member.title == "Software Engineer"
    assert db_member.email == "john@example.com"
    assert db_member.is_deleted == False
    assert db_member.created_at is not None
    assert db_member.updated_at is None

def test_get_members_op(db_session, mock_verify_organization):
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
    
    results = get_member_db(1, db_session)
    
    assert len(results) == 3
    
    for member in results:
        assert member.organization_id == 1
        assert member.is_deleted == False
    
    follower_list = [member.followers for member in results]
    assert follower_list == [122, 121, 120]
    
    member0 = results[-1]
    assert member0.first_name == "John0"
    assert member0.last_name == "Doe0"
    assert member0.avatar_url == "https://example.com/avatar0.jpg"
    assert member0.followers == 120
    assert member0.following == 35
    assert member0.title == "Software Engineer 0"
    assert member0.email == "john0@example.com"
    

def test_delete_members_op(db_session, mock_verify_organization):
    for i in range(2):
        db_session.add(Member(
            organization_id=1,
            first_name="John",
            last_name="Doe",
            login=f"john123_{i}",
            avatar_url=f"https://example.com/avatar{i}.jpg",
            followers=120 + i,
            following=35 + i,
            title=f"Software Engineer {i}",
            email=f"john{i}@example.com"
        ))
    db_session.commit()
    
    delete_all_members_db(1, db_session)
    
    members = db_session.query(Member).filter(
        Member.organization_id == 1
    ).all()
    for member in members:
        assert member.is_deleted == True
    
    results = get_member_db(1, db_session)
    assert len(results) == 0

