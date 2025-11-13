from models.CartItem import CartItem

def hold_item(cart: tuple[CartItem, ...], item: CartItem) -> tuple[CartItem, ...]:
    # создаём новую корзину, старую не трогаем
    return cart + (item,)

def remove_hold(cart: tuple[CartItem, ...], item_id: str) -> tuple[CartItem, ...]:
    # фильтруем корзину, оставляем всё кроме удаляемого
    return tuple(filter(lambda x: x.id != item_id, cart))
