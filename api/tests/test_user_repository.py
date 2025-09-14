import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def user_repository(db_session):
    """Create a user repository instance"""
    return UserRepository(db_session)

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return UserCreate(
        firstname="John",
        lastname="Doe",
        age=25,
        date_of_birth=date(1998, 5, 15)
    )

def test_create_user(user_repository, sample_user_data):
    """Test creating a new user"""
    user = user_repository.create_user(sample_user_data)
    
    assert user.id is not None
    assert user.firstname == "John"
    assert user.lastname == "Doe"
    assert user.age == 25
    assert user.date_of_birth == date(1998, 5, 15)

def test_get_all_users_empty(user_repository):
    """Test getting all users when database is empty"""
    users = user_repository.get_all_users()
    assert users == []

def test_get_all_users_with_data(user_repository, sample_user_data):
    """Test getting all users when there is data"""
    user_repository.create_user(sample_user_data)
    
    users = user_repository.get_all_users()
    assert len(users) == 1
    assert users[0].firstname == "John"

def test_delete_user_success(user_repository, sample_user_data):
    """Test successful user deletion"""
    user = user_repository.create_user(sample_user_data)
    
    result = user_repository.delete_user(user.id)
    assert result is True
    
    # Verify user is deleted
    users = user_repository.get_all_users()
    assert len(users) == 0

def test_delete_user_not_found(user_repository):
    """Test deleting a non-existent user"""
    result = user_repository.delete_user(999)
    assert result is False