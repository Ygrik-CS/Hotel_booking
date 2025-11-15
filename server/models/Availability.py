"""Availability model."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Availability(Base):
    """Availability model for room inventory."""
    __tablename__ = "availabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False, index=True)  # ISO format
    available = Column(Integer, nullable=False, default=0)
    
    # Relationships
    room_type = relationship("RoomType", back_populates="availabilities")