"""Hotel controller."""
from typing import List, Tuple
from sqlalchemy.orm import Session
from models.Hotel import Hotel as HotelModel
from models.room_type import RoomType as RoomTypeModel
from core.domain import Hotel, RoomType
import json


class HotelController:
    """Hotel business logic."""
    
    @staticmethod
    def get_all_hotels(db: Session) -> List[dict]:
        """Get all hotels."""
        hotels = db.query(HotelModel).all()
        return [
            {
                "id": h.id,
                "name": h.name,
                "stars": h.stars,
                "city": h.city,
                "features": json.loads(h.features) if h.features else []
            }
            for h in hotels
        ]
    
    @staticmethod
    def get_hotel_by_id(db: Session, hotel_id: int) -> dict:
        """Get hotel by ID with room types."""
        hotel = db.query(HotelModel).filter(HotelModel.id == hotel_id).first()
        if not hotel:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
        
        room_types = db.query(RoomTypeModel).filter(RoomTypeModel.hotel_id == hotel_id).all()
        
        return {
            "id": hotel.id,
            "name": hotel.name,
            "stars": hotel.stars,
            "city": hotel.city,
            "features": json.loads(hotel.features) if hotel.features else [],
            "room_types": [
                {
                    "id": rt.id,
                    "name": rt.name,
                    "capacity": rt.capacity,
                    "beds": json.loads(rt.beds) if rt.beds else [],
                    "features": json.loads(rt.features) if rt.features else []
                }
                for rt in room_types
            ]
        }
    
    @staticmethod
    def convert_to_domain(hotel_model: HotelModel) -> Hotel:
        """Convert SQLAlchemy model to immutable domain entity."""
        features = tuple(json.loads(hotel_model.features)) if hotel_model.features else ()
        return Hotel(
            id=hotel_model.id,
            name=hotel_model.name,
            stars=hotel_model.stars,
            city=hotel_model.city,
            features=features
        )
