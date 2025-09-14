from typing import List
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from fastapi import HTTPException

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def get_all_users(self) -> List[UserResponse]:
        """Get all users with business logic if needed"""
        users = self.repository.get_all_users()
        return [UserResponse.model_validate(user) for user in users]
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create user with validation"""
        user = self.repository.create_user(user_data)
        return UserResponse.model_validate(user)
    
    def delete_user(self, user_id: int) -> None:
        """Delete user with proper error handling"""
        if not self.repository.delete_user(user_id):
            raise HTTPException(status_code=404, detail="User not found")