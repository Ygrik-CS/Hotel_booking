from models.CartItem import CartItem

cart: tuple[CartItem, ...] = ()

def cartItemAdd(cart: tuple[CartItem, ...], item: CartItem) -> tuple[CartItem, ...]:
    # создаём новую корзину, старую не трогаем
    cart = cart + (item,)
    return cart

def cartItemRemove(cart: tuple[CartItem, ...], item_id: str) -> tuple[CartItem, ...]:
    # фильтруем корзину, оставляем всё кроме удаляемого
    cart = tuple(filter(lambda x: x.id != item_id, cart))
    return cart

def cartGet() -> tuple[CartItem, ...]:
    return cart