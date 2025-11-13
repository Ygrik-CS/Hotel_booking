from typing import NamedTuple
# Тип номера в отеле
class RoomType(NamedTuple):
    id: int  # айди типа номера
    hotel_id: int  # айди отеля
    name: str  # название типа
    capacity: int  # вместимость
    beds: tuple[str, ...]  # список кроватей
    features: tuple[str, ...]  # удобства номера