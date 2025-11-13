from typing import NamedTuple
from models.CartItem import CartItem
# Бронь (уже оформленная)
class Booking(NamedTuple):
    id: int  # айди брони
    guest_id: int  # кто забронировал
    items: tuple[CartItem, ...]  # список позиций из корзины
    total: int  # итоговая сумма
    status: str  # статус (held, confirmed, cancelled)