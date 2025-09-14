import pytest
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create a test client"""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_user():
    """Sample user data for testing"""
    return {
        "firstname": "Jane",
        "lastname": "Smith", 
        "age": 30,
        "date_of_birth": "1993-12-10"
    }

def test_get_users_empty(client):
    """Test getting users when database is empty"""
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

def test_create_user_success(client, sample_user):
    """Test successful user creation"""
    response = client.post("/users/create", json=sample_user)
    assert response.status_code == 200
    
    data = response.json()
    assert data["firstname"] == "Jane"
    assert data["lastname"] == "Smith"
    assert data["age"] == 30
    assert data["date_of_birth"] == "1993-12-10"
    assert "id" in data

def test_create_user_invalid_data(client):
    """Test user creation with invalid data"""
    invalid_user = {
        "firstname": "",  # Empty firstname should fail
        "lastname": "Smith",
        "age": -5,  # Invalid age
        "date_of_birth": "1993-12-10"
    }
    
    response = client.post("/users/create", json=invalid_user)
    assert response.status_code == 422  # Validation error

def test_get_users_with_data(client, sample_user):
    """Test getting users after creating one"""
    # Create a user first
    client.post("/users/create", json=sample_user)
    
    response = client.get("/users")
    assert response.status_code == 200
    
    users = response.json()
    assert len(users) == 1
    assert users[0]["firstname"] == "Jane"

def test_delete_user_success(client, sample_user):
    """Test successful user deletion"""
    # Create a user first
    create_response = client.post("/users/create", json=sample_user)
    user_id = create_response.json()["id"]
    
    # Delete the user
    delete_response = client.delete("/user", json={"id": user_id})
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "User deleted successfully"
    
    # Verify user is deleted
    get_response = client.get("/users")
    assert len(get_response.json()) == 0

def test_delete_user_not_found(client):
    """Test deleting a non-existent user"""
    response = client.delete("/user", json={"id": 999})
    assert response.status_code == 404