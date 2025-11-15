"""Room type model."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class RoomType(Base):
    """Room type model."""
    __tablename__ = "room_types"
    
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    beds = Column(Text)  # JSON string
    features = Column(Text)  # JSON string
    
    # Relationships
    hotel = relationship("Hotel", back_populates="room_types")
    rate_plans = relationship("RatePlan", back_populates="room_type", cascade="all, delete-orphan")
    availabilities = relationship("Availability", back_populates="room_type", cascade="all, delete-orphan")
