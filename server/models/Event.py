from typing import NamedTuple
# Событие (для системы или логов)
class Event(NamedTuple):
    id: int  # айди события
    ts: str  # время
    name: str  # тип события
    payload: dict  # доп инфа (например, данные по брони)