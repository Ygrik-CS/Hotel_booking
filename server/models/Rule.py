"""Rule model for business rules."""
from sqlalchemy import Column, Integer, String, Text
from database.base import Base


class Rule(Base):
    """Business rule model."""
    __tablename__ = "rules"
    
    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String, nullable=False, index=True)  # min_stay, max_stay, etc.
    payload = Column(Text)  # JSON string