from typing import NamedTuple
# Цена
class Price(NamedTuple):
    id: int  # айди записи
    rate_id: int  # айди тарифа
    date: str  # дата
    amount: int  # стоимость в копейках/тийынах
    currency: int  # валюта
