from typing import NamedTuple
# Доступность номеров
class Availability(NamedTuple):
    id: int  # айди записи
    room_type_id: int  # айди типа номера
    date: str  # дата
    available: int  # сколько номеров свободно