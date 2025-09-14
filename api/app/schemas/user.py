from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    """Schema for creating a new user"""
    firstname: str = Field(..., min_length=1, max_length=50)
    lastname: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=0, le=150)
    date_of_birth: date

class UserResponse(BaseModel):
    """Schema for returning user data"""
    id: int
    firstname: str
    lastname: str
    age: int
    date_of_birth: date
    
    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    """Schema for deleting a user"""
    id: int