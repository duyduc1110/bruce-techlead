import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Provide a database session for testing."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    
    app.dependency_overrides[get_db] = lambda: session
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client():
    """Provide a test client for the FastAPI app."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_verify_organization():
    """Mock the organization verification function."""
    with patch('app.ops.member_op.verify_organization_exists', return_value=True) as mock:
        yield mock