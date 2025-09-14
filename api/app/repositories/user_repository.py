from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_users(self) -> List[User]:
        """Fetch all users from database"""
        return self.db.query(User).all()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user in database"""
        user = User(**user_data.model_dump())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID, returns True if deleted, False if not found"""
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False