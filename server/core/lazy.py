"""Lazy evaluation with generators."""
from typing import Iterator, Tuple, Any
import itertools
from core.domain import Hotel, RoomType, RatePlan, SearchOffer, Price, Availability


def lazy_search_offers(
    hotels: Tuple[Hotel, ...],
    room_types_map: dict,  # hotel_id -> room_types
    rates_map: dict,  # room_type_id -> rates
    availability_map: dict,  # (room_type_id, date) -> available
    prices_map: dict,  # (rate_id, date) -> price
    checkin: str,
    checkout: str
) -> Iterator[SearchOffer]:
    """Lazy generator for search offers."""
    for hotel in hotels:
        room_types = room_types_map.get(hotel.id, ())
        for room_type in room_types:
            rates = rates_map.get(room_type.id, ())
            for rate in rates:
                # Check availability lazily
                dates = _generate_dates(checkin, checkout)
                is_available = all(
                    availability_map.get((room_type.id, date), 0) > 0
                    for date in dates
                )
                
                if is_available:
                    # Calculate price lazily
                    total_price = sum(
                        prices_map.get((rate.id, date), 0)
                        for date in dates
                    )
                    
                    yield SearchOffer(
                        hotel=hotel,
                        room_type=room_type,
                        rate_plan=rate,
                        total_price=total_price,
                        available=True
                    )


def _generate_dates(start: str, end: str) -> Iterator[str]:
    """Generate dates between start and end."""
    from datetime import datetime, timedelta
    current = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    
    while current < end_dt:
        yield current.date().isoformat()
        current += timedelta(days=1)


def generate_calendar(
    room_type_id: int,
    start_date: str,
    days: int,
    availability_map: dict
) -> Iterator[Tuple[str, int]]:
    """Generate availability calendar lazily."""
    from datetime import datetime, timedelta
    current = datetime.fromisoformat(start_date)
    
    for _ in range(days):
        date_str = current.date().isoformat()
        available = availability_map.get((room_type_id, date_str), 0)
        yield (date_str, available)
        current += timedelta(days=1)


def lazy_filter(predicate, iterable: Iterator) -> Iterator:
    """Lazy filter operation."""
    for item in iterable:
        if predicate(item):
            yield item


def lazy_map(func, iterable: Iterator) -> Iterator:
    """Lazy map operation."""
    for item in iterable:
        yield func(item)


def take_while(predicate, iterable: Iterator) -> Iterator:
    """Take elements while predicate is true."""
    for item in iterable:
        if not predicate(item):
            break
        yield item


def chunk(iterable: Iterator, size: int) -> Iterator[Tuple]:
    """Chunk iterable into fixed-size tuples."""
    iterator = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(iterator, size))
        if not chunk:
            break
        yield chunk
