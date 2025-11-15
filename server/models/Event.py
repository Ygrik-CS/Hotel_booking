"""Event model for FRP."""
from sqlalchemy import Column, Integer, String, Text
from database.base import Base


class Event(Base):
    """Event model for functional reactive programming."""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(String, nullable=False)  # ISO format timestamp
    name = Column(String, nullable=False, index=True)  # SEARCH, HOLD, BOOKED, etc.
    payload = Column(Text)  # JSON string