"""Rate plan model."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class RatePlan(Base):
    """Rate plan model."""
    __tablename__ = "rate_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    meal = Column(String, nullable=False)  # BB, HB, FB, AI
    refundable = Column(Boolean, default=True)
    cancel_before_days = Column(Integer, default=1)
    
    # Relationships
    hotel = relationship("Hotel", back_populates="rate_plans")
    room_type = relationship("RoomType", back_populates="rate_plans")
    prices = relationship("Price", back_populates="rate_plan", cascade="all, delete-orphan")
