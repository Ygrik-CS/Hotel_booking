"""Pure functions and higher-order functions."""
from typing import Callable, TypeVar, Tuple, Dict, Any
from core.domain import Hotel, Price, SearchOffer

T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')


# Higher-Order Functions
def apply_to_all(func: Callable[[T], U], items: Tuple[T, ...]) -> Tuple[U, ...]:
    """Map function over tuple (HOF)."""
    return tuple(func(item) for item in items)


def filter_items(predicate: Callable[[T], bool], items: Tuple[T, ...]) -> Tuple[T, ...]:
    """Filter tuple by predicate (HOF)."""
    return tuple(item for item in items if predicate(item))


def fold_left(func: Callable[[U, T], U], initial: U, items: Tuple[T, ...]) -> U:
    """Reduce/fold left over tuple (HOF)."""
    result = initial
    for item in items:
        result = func(result, item)
    return result


def compose(*functions: Callable) -> Callable:
    """Compose functions from right to left (HOF)."""
    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return inner


# Pure functions for domain logic
def calculate_total_price(prices: Tuple[Price, ...]) -> int:
    """Calculate total price from tuple of prices."""
    return fold_left(lambda acc, price: acc + price.amount, 0, prices)


def filter_hotels_by_city(hotels: Tuple[Hotel, ...], city: str) -> Tuple[Hotel, ...]:
    """Filter hotels by city."""
    return filter_items(lambda h: h.city.lower() == city.lower(), hotels)


def filter_hotels_by_stars(hotels: Tuple[Hotel, ...], min_stars: int) -> Tuple[Hotel, ...]:
    """Filter hotels by minimum stars."""
    return filter_items(lambda h: h.stars >= min_stars, hotels)


def get_hotel_names(hotels: Tuple[Hotel, ...]) -> Tuple[str, ...]:
    """Extract hotel names."""
    return apply_to_all(lambda h: h.name, hotels)


def group_by(key_func: Callable[[T], K], items: Tuple[T, ...]) -> Dict[K, Tuple[T, ...]]:
    """Group items by key function."""
    result: Dict[K, list] = {}
    for item in items:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return {k: tuple(v) for k, v in result.items()}


def max_by(key_func: Callable[[T], Any], items: Tuple[T, ...]) -> T:
    """Find maximum element by key function."""
    if not items:
        raise ValueError("Cannot find max of empty tuple")
    return max(items, key=key_func)


def min_by(key_func: Callable[[T], Any], items: Tuple[T, ...]) -> T:
    """Find minimum element by key function."""
    if not items:
        raise ValueError("Cannot find min of empty tuple")
    return min(items, key=key_func)


def take(n: int, items: Tuple[T, ...]) -> Tuple[T, ...]:
    """Take first n items."""
    return items[:n]


def drop(n: int, items: Tuple[T, ...]) -> Tuple[T, ...]:
    """Drop first n items."""
    return items[n:]


def sort_by_price(offers: Tuple[SearchOffer, ...]) -> Tuple[SearchOffer, ...]:
    """Sort offers by price."""
    return tuple(sorted(offers, key=lambda o: o.total_price))


def filter_available_offers(offers: Tuple[SearchOffer, ...]) -> Tuple[SearchOffer, ...]:
    """Filter only available offers."""
    return filter_items(lambda o: o.available, offers)
