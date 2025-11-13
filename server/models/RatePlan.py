from typing import NamedTuple, Optional
# Тариф
class RatePlan(NamedTuple):
    id: int  # айди тарифа
    hotel_id: int  # айди отеля
    room_type_id: int  # айди типа номера
    title: str  # название тарифа
    meal: str  # тип питания
    refundable: bool  # можно ли отменить
    cancel_before_days: Optional[int]  # за сколько дней до заезда можно отменить