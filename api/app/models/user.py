from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class User(Base):
    """User model representing users in the database"""
    __tablename__ = "users"
    
    # Primary key with auto-increment
    id = Column(Integer, primary_key=True, index=True)
    
    # User basic information
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    date_of_birth = Column(Date, nullable=False)