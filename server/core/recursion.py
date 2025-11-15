"""Recursive functions."""
from datetime import datetime, timedelta
from typing import Tuple, List, Any, TypeVar

T = TypeVar('T')


def split_date_range(start_date: str, end_date: str) -> Tuple[str, ...]:
    """Recursively split date range into individual dates."""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    def _split_helper(current: datetime, end: datetime, acc: List[str]) -> Tuple[str, ...]:
        if current > end:
            return tuple(acc)
        acc.append(current.date().isoformat())
        return _split_helper(current + timedelta(days=1), end, acc)
    
    return _split_helper(start, end, [])


def flatten_tuple(nested: Tuple) -> Tuple:
    """Recursively flatten nested tuples."""
    result = []
    for item in nested:
        if isinstance(item, tuple):
            result.extend(flatten_tuple(item))
        else:
            result.append(item)
    return tuple(result)


def filter_tree(predicate, tree: Tuple) -> Tuple:
    """Recursively filter tree structure."""
    result = []
    for item in tree:
        if isinstance(item, tuple):
            filtered = filter_tree(predicate, item)
            if filtered:
                result.append(filtered)
        elif predicate(item):
            result.append(item)
    return tuple(result)


def max_depth(tree: Tuple) -> int:
    """Calculate maximum depth of nested tuple."""
    if not tree:
        return 0
    
    def _max_depth_helper(item) -> int:
        if not isinstance(item, tuple):
            return 0
        if not item:
            return 1
        return 1 + max(_max_depth_helper(sub) for sub in item)
    
    return _max_depth_helper(tree)


def count_leaves(tree: Tuple) -> int:
    """Count leaf nodes in tree."""
    if not tree:
        return 0
    
    def _count_helper(item) -> int:
        if not isinstance(item, tuple):
            return 1
        if not item:
            return 0
        return sum(_count_helper(sub) for sub in item)
    
    return _count_helper(tree)


def sum_recursive(numbers: Tuple[int, ...]) -> int:
    """Recursive sum of numbers."""
    if not numbers:
        return 0
    return numbers[0] + sum_recursive(numbers[1:])


def reverse_recursive(items: Tuple[T, ...]) -> Tuple[T, ...]:
    """Recursively reverse tuple."""
    if not items:
        return ()
    return reverse_recursive(items[1:]) + (items[0],)
