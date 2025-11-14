from fastapi import APIRouter
from models.CartItem import CartItem
from controller.cart_controller import *


router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/")
def get_cart():
    return getCartFromController()

@router.post("/add")
def add_to_cart():
    return addItemToController(item)

@router.delete("/remove/{item_id}")
def remove_item(item_id: str):
    removeItemInController(item_id)