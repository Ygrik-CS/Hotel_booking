from typing import NamedTuple
# Платёж
class Payment(NamedTuple):
    id: int  # айди платежа
    booking_id: int  # айди брони
    amount: int  # сумма платежа
    ts: str  # время платежа
    method: str  # метод оплаты (карта, нал, онлайн)