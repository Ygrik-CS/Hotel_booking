from typing import NamedTuple
# Элемент корзины (предварительная бронь)
class CartItem(NamedTuple):
    id: int  # айди позиции
    hotel_id: int  # айди отеля
    room_type_id: int  # айди типа номера
    rate_id: int  # айди тарифа
    checkin: str  # дата заезда
    checkout: str  # дата выезда
    guests: int  # кол-во гостей




