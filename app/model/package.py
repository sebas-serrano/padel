from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Package(Base):
    __tablename__ = 'package'
    
    package_id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    ticket_quantity = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    firebase_uid = Column(String(255), ForeignKey('user.firebase_uid'), nullable=False)
    user = relationship("User", back_populates="packages")