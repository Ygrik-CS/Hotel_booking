"""Hotel routers."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from controllers.hotel_controller import HotelController


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/")
async def get_all_hotels(db: Session = Depends(get_db)):
    """Get all hotels."""
    return HotelController.get_all_hotels(db)


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Get hotel by ID with room types."""
    return HotelController.get_hotel_by_id(db, hotel_id)
