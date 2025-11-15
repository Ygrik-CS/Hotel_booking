"""Cart routers."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from controllers.cart_controller import CartController


router = APIRouter(prefix="/cart", tags=["Cart"])


class AddToCartRequest(BaseModel):
    hotel_id: int
    room_type_id: int
    rate_id: int
    checkin: str
    checkout: str
    guests: int


@router.get("/")
async def get_cart(db: Session = Depends(get_db)):
    """Get all cart items."""
    return CartController.get_cart_items(db)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item: AddToCartRequest,
    db: Session = Depends(get_db)
):
    """Add item to cart."""
    return CartController.add_to_cart(
        db=db,
        hotel_id=item.hotel_id,
        room_type_id=item.room_type_id,
        rate_id=item.rate_id,
        checkin=item.checkin,
        checkout=item.checkout,
        guests=item.guests
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    """Remove item from cart."""
    CartController.remove_from_cart(db, item_id)
    return None


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(db: Session = Depends(get_db)):
    """Clear all cart items."""
    CartController.clear_cart(db)
    return None
