"""Guest model."""
from sqlalchemy import Column, Integer, String
from database.base import Base


class Guest(Base):
    """Guest model."""
    __tablename__ = "guests"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)