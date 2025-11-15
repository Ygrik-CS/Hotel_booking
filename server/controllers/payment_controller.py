"""Payment controller."""
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
from models.Payment import Payment as PaymentModel
from models.Booking import Booking as BookingModel
from core.frp import event_bus, create_event, EVENT_PAYMENT


class PaymentController:
    """Payment business logic."""
    
    @staticmethod
    def create_payment(
        db: Session,
        booking_id: int,
        method: str = "card"
    ) -> dict:
        """Create payment for booking."""
        # Verify booking exists
        booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        if booking.status == "cancelled":
            raise HTTPException(status_code=400, detail="Cannot pay for cancelled booking")
        
        # Create payment
        payment = PaymentModel(
            booking_id=booking_id,
            amount=booking.total,
            ts=datetime.now().isoformat(),
            method=method
        )
        db.add(payment)
        
        # Update booking status
        booking.status = "confirmed"
        
        db.commit()
        db.refresh(payment)
        
        # Publish event
        event = create_event(EVENT_PAYMENT, payment_id=payment.id, booking_id=booking_id)
        event_bus.publish(event)
        
        return {
            "id": payment.id,
            "booking_id": payment.booking_id,
            "amount": payment.amount,
            "ts": payment.ts,
            "method": payment.method
        }
    
    @staticmethod
    def get_payment(db: Session, payment_id: int) -> dict:
        """Get payment details."""
        payment = db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return {
            "id": payment.id,
            "booking_id": payment.booking_id,
            "amount": payment.amount,
            "ts": payment.ts,
            "method": payment.method
        }
