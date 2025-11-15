"""Memoization utilities."""
from functools import lru_cache, wraps
from typing import Callable, Dict, Tuple, Any
from core.recursion import split_date_range


@lru_cache(maxsize=None)
def fibonacci_memo(n: int) -> int:
    """Memoized Fibonacci sequence."""
    if n <= 1:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)


@lru_cache(maxsize=1000)
def calculate_date_range_price(start_date: str, end_date: str, base_price: int) -> int:
    """Calculate price for date range with memoization."""
    dates = split_date_range(start_date, end_date)
    # Weekend multiplier
    total = 0
    for date_str in dates:
        date = __import__('datetime').datetime.fromisoformat(date_str)
        multiplier = 1.2 if date.weekday() >= 5 else 1.0
        total += int(base_price * multiplier)
    return total


@lru_cache(maxsize=500)
def calculate_cancellation_penalty(days_before: int, refundable: bool, total_amount: int) -> int:
    """Calculate cancellation penalty with memoization."""
    if not refundable:
        return total_amount
    if days_before >= 7:
        return 0
    if days_before >= 3:
        return int(total_amount * 0.25)
    if days_before >= 1:
        return int(total_amount * 0.50)
    return int(total_amount * 0.75)


def memoize(func: Callable) -> Callable:
    """Custom memoization decorator."""
    cache: Dict[Tuple, Any] = {}
    
    @wraps(func)
    def memoized(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    memoized.cache = cache
    memoized.cache_clear = lambda: cache.clear()
    return memoized


@memoize
def expensive_calculation(a: int, b: int) -> int:
    """Example expensive calculation with custom memoization."""
    # Simulate expensive calculation
    result = 0
    for i in range(1000):
        result += (a * b * i) % 1000
    return result
