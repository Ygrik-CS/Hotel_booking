from typing import NamedTuple
# Инфо о госте
class Guest(NamedTuple):
    id: int  # айди гостя
    name: str  # имя
    email: str  # почта