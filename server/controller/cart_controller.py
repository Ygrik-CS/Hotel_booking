from fastapi import APIRouter
from models.CartItem import CartItem
from typing import List

router = APIRouter(prefix="/cart", tags=["Cart"])

CART: list[CartItem] = []

@router.get("/", response_model=List[CartItem])
def get_cart():
    return CART