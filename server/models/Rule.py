from typing import NamedTuple
# Правило (ограничение или надбавка)
class Rule(NamedTuple):
    id: int  # айди правила
    kind: str  # тип (min_stay, max_stay и т.д.)
    payload: dict  # данные правила (например, {"min_days": 2})