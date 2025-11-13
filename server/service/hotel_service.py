from models import *
from typing import Iterator, Tuple, Callable

def iter_available_days(avail: tuple[tuple[str, int], ...], room_type_id: str) -> Iterator[tuple[str, int]]:
    """Лениво перебирает дни доступности для данного типа номера"""
    for day, available_room_id in avail:
        if available_room_id == room_type_id:
            yield (day, available_room_id)

def lazy_offers(hotels, room_types, rates, prices, avail, predicate: Callable) -> Iterator[tuple]:
    for h in hotels:
        for r in room_types:
            if r['hotel_id'] != h['id']:
                continue
            for rt in rates:
                for p in prices:
                    if p['hotel_id'] == h['id'] and p['room_id'] == r['id'] and p['tariff_id'] == rt['id']:
                        offer = (h, r, rt, p['price'])
                        if predicate(offer):
                            yield offer