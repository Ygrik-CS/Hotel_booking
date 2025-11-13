from typing import NamedTuple
# Класс отеля, где хранятся базовые данные
class Hotel(NamedTuple):
    id: int  # айди отеля
    name: str  # название
    city: str  # город
    stars: float  # звёзды
    features: tuple[str, ...]  # удобства (wifi, парковка и т.д.)