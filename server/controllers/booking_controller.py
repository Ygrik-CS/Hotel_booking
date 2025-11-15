"""Booking controller."""
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
from models.Booking import Booking as BookingModel
from models.Guest import Guest as GuestModel
from models.cart import CartItem as CartItemModel
from models.Payment import Payment as PaymentModel
from core.frp import event_bus, create_event, EVENT_BOOKED, EVENT_CANCELLED
from core.memo import calculate_cancellation_penalty


class BookingController:
    """Booking business logic."""
    
    @staticmethod
    def create_booking(
        db: Session,
        guest_id: int,
        cart_item_ids: List[int]
    ) -> dict:
        """Create booking from cart items."""
        # Verify guest exists
        guest = db.query(GuestModel).filter(GuestModel.id == guest_id).first()
        if not guest:
            raise HTTPException(status_code=404, detail="Guest not found")
        
        # Get cart items
        cart_items = db.query(CartItemModel).filter(
            CartItemModel.id.in_(cart_item_ids)
        ).all()
        
        if not cart_items:
            raise HTTPException(status_code=400, detail="No cart items found")
        
        # Calculate total (simplified - would need to fetch prices)
        total = len(cart_items) * 100000  # Placeholder
        
        # Create booking
        booking = BookingModel(
            guest_id=guest_id,
            total=total,
            status="held"
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        
        # Publish event
        event = create_event(EVENT_BOOKED, booking_id=booking.id, guest_id=guest_id)
        event_bus.publish(event)
        
        return {
            "id": booking.id,
            "guest_id": booking.guest_id,
            "total": booking.total,
            "status": booking.status
        }
    
    @staticmethod
    def cancel_booking(db: Session, booking_id: int) -> dict:
        """Cancel booking with penalty calculation."""
        booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        if booking.status == "cancelled":
            raise HTTPException(status_code=400, detail="Booking already cancelled")
        
        # Calculate penalty (simplified)
        penalty = calculate_cancellation_penalty(
            days_before=7,
            refundable=True,
            total_amount=booking.total
        )
        
        # Update booking
        booking.status = "cancelled"
        db.commit()
        
        # Publish event
        event = create_event(EVENT_CANCELLED, booking_id=booking_id, penalty=penalty)
        event_bus.publish(event)
        
        return {
            "id": booking.id,
            "status": booking.status,
            "penalty": penalty
        }
    
    @staticmethod
    def get_booking(db: Session, booking_id: int) -> dict:
        """Get booking details."""
        booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        return {
            "id": booking.id,
            "guest_id": booking.guest_id,
            "total": booking.total,
            "status": booking.status
        }
