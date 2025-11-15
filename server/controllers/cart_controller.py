"""Cart controller."""
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.cart import CartItem as CartItemModel
from models.Hotel import Hotel as HotelModel
from models.room_type import RoomType as RoomTypeModel
from models.rate_plan import RatePlan as RatePlanModel
from core.ftypes import validate_positive, validate_date_range


class CartController:
    """Cart business logic."""
    
    @staticmethod
    def get_cart_items(db: Session) -> List[dict]:
        """Get all cart items."""
        items = db.query(CartItemModel).all()
        return [
            {
                "id": item.id,
                "hotel_id": item.hotel_id,
                "room_type_id": item.room_type_id,
                "rate_id": item.rate_id,
                "checkin": item.checkin,
                "checkout": item.checkout,
                "guests": item.guests
            }
            for item in items
        ]
    
    @staticmethod
    def add_to_cart(
        db: Session,
        hotel_id: int,
        room_type_id: int,
        rate_id: int,
        checkin: str,
        checkout: str,
        guests: int
    ) -> dict:
        """Add item to cart with validation."""
        # Validate inputs using Either monad
        hotel_valid = validate_positive(hotel_id, "hotel_id")
        guests_valid = validate_positive(guests, "guests")
        dates_valid = validate_date_range(checkin, checkout)
        
        if hotel_valid.is_left():
            raise HTTPException(status_code=400, detail=hotel_valid.get_left())
        if guests_valid.is_left():
            raise HTTPException(status_code=400, detail=guests_valid.get_left())
        if dates_valid.is_left():
            raise HTTPException(status_code=400, detail=dates_valid.get_left())
        
        # Verify hotel exists
        hotel = db.query(HotelModel).filter(HotelModel.id == hotel_id).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        
        # Create cart item
        cart_item = CartItemModel(
            hotel_id=hotel_id,
            room_type_id=room_type_id,
            rate_id=rate_id,
            checkin=checkin,
            checkout=checkout,
            guests=guests
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        
        return {
            "id": cart_item.id,
            "hotel_id": cart_item.hotel_id,
            "room_type_id": cart_item.room_type_id,
            "rate_id": cart_item.rate_id,
            "checkin": cart_item.checkin,
            "checkout": cart_item.checkout,
            "guests": cart_item.guests
        }
    
    @staticmethod
    def remove_from_cart(db: Session, item_id: int):
        """Remove item from cart."""
        item = db.query(CartItemModel).filter(CartItemModel.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        db.delete(item)
        db.commit()
    
    @staticmethod
    def clear_cart(db: Session):
        """Clear all cart items."""
        db.query(CartItemModel).delete()
        db.commit()
