"""Price model."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Price(Base):
    """Price model for daily rates."""
    __tablename__ = "prices"
    
    id = Column(Integer, primary_key=True, index=True)
    rate_id = Column(Integer, ForeignKey("rate_plans.id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False, index=True)  # ISO format
    amount = Column(Integer, nullable=False)  # in kopecks/tiyin
    currency = Column(String, default="UZS")
    
    # Relationships
    rate_plan = relationship("RatePlan", back_populates="prices")
