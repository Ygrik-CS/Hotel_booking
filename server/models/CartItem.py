from typing import NamedTuple
from pydantic import BaseModel

#immutable model
class CartItem(NamedTuple):
    id: int  # айди позиции
    hotel_id: int  # айди отеля
    room_type_id: int  # айди типа номера
    rate_id: int  # айди тарифа
    checkin: str  # дата заезда
    checkout: str  # дата выезда
    guests: int  # кол-во гостей



#pydantic model
class CartItem(BaseModel):
    id: str
    name: str
    price: float
