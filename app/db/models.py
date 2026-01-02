from sqlalchemy import Column, Integer, String, Boolean, Date
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(128), unique=True, index=True)
    user_id = Column(Integer, nullable=False)
