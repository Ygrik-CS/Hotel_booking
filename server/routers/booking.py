"""Booking routers."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db
from controllers.booking_controller import BookingController


router = APIRouter(prefix="/bookings", tags=["Bookings"])


class CreateBookingRequest(BaseModel):
    guest_id: int
    cart_item_ids: List[int]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: CreateBookingRequest,
    db: Session = Depends(get_db)
):
    """Create a new booking."""
    return BookingController.create_booking(
        db=db,
        guest_id=booking_data.guest_id,
        cart_item_ids=booking_data.cart_item_ids
    )


@router.get("/{booking_id}")
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get booking details."""
    return BookingController.get_booking(db, booking_id)


@router.post("/{booking_id}/cancel")
async def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """Cancel a booking."""
    return BookingController.cancel_booking(db, booking_id)
