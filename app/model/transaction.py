from sqlalchemy import Column, Integer, ForeignKey, Boolean, Date, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Transaction(Base):
    __tablename__ = 'transaction'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    description = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)  # Clave foránea
    user_email = Column(String(50), nullable=False)
    tickets = Column(Integer, nullable=False)
    user = relationship("User", back_populates="transactions")