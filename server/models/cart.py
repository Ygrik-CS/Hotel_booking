"""Cart item model."""
from sqlalchemy import Column, Integer, String, ForeignKey
from database.base import Base


class CartItem(Base):
    """Cart item model for shopping cart."""
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    rate_id = Column(Integer, ForeignKey("rate_plans.id"), nullable=False)
    checkin = Column(String, nullable=False)  # ISO format
    checkout = Column(String, nullable=False)  # ISO format
    guests = Column(Integer, nullable=False)
