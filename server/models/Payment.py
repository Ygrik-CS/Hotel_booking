"""Payment model."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Payment(Base):
    """Payment model."""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
    ts = Column(String, nullable=False)  # ISO format timestamp
    method = Column(String, nullable=False)  # card, cash, etc.
    
    # Relationships
    booking = relationship("Booking", back_populates="payments")