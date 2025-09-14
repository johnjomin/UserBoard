from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserDelete
from app.services.user_service import UserService

# Create router instance for user-related endpoints
router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Get all users from the database"""
    service = UserService(db)
    return service.get_all_users()

@router.post("/users/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database"""
    service = UserService(db)
    return service.create_user(user)

@router.delete("/user")
def delete_user(user_data: UserDelete, db: Session = Depends(get_db)):
    """Delete a user from the database by ID"""
    service = UserService(db)
    service.delete_user(user_data.id)
    return {"message": "User deleted successfully"}