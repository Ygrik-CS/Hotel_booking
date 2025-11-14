from service.hotel_cart_service import cartItemAdd, cartItemRemove, cartGet
from models.CartItem import CartItem

def addItemToController(item: CartItem):
    return cartItemAdd(item)

def removeItemInController(item_id: str):
    return cartItemRemove(item_id)

def getCartFromController():
    return cartGet()