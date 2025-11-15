"""Booking model."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Booking(Base):
    """Booking model."""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    total = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="held")  # held, confirmed, cancelled
    
    # Relationships
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")