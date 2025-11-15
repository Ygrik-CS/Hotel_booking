"""Hotel model."""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.base import Base


class Hotel(Base):
    """Hotel model."""
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    stars = Column(Integer, nullable=False)
    city = Column(String, nullable=False, index=True)
    features = Column(Text)  # JSON string
    
    # Relationships
    room_types = relationship("RoomType", back_populates="hotel", cascade="all, delete-orphan")
    rate_plans = relationship("RatePlan", back_populates="hotel", cascade="all, delete-orphan")