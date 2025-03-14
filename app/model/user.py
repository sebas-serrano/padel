from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firebase_uid = Column(String(255), unique=True, nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    tickets = Column(Integer, default=0)
    phone_number = Column(String(255), nullable=True)
    packages = relationship("Package", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")