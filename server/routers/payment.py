"""Payment routers."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from controllers.payment_controller import PaymentController


router = APIRouter(prefix="/payments", tags=["Payments"])


class CreatePaymentRequest(BaseModel):
    booking_id: int
    method: str = "card"


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: CreatePaymentRequest,
    db: Session = Depends(get_db)
):
    """Create a payment for a booking."""
    return PaymentController.create_payment(
        db=db,
        booking_id=payment_data.booking_id,
        method=payment_data.method
    )


@router.get("/{payment_id}")
async def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get payment details."""
    return PaymentController.get_payment(db, payment_id)
