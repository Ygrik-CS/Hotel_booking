"""Tests for Lab 5: Lazy evaluation."""
import pytest
from core.lazy import (
    lazy_filter,
    lazy_map,
    take_while,
    chunk
)


def test_lazy_filter():
    """Test lazy filter operation."""
    numbers = range(10)
    filtered = lazy_filter(lambda x: x % 2 == 0, numbers)
    result = list(filtered)
    assert result == [0, 2, 4, 6, 8]


def test_lazy_map():
    """Test lazy map operation."""
    numbers = range(5)
    mapped = lazy_map(lambda x: x * 2, numbers)
    result = list(mapped)
    assert result == [0, 2, 4, 6, 8]


def test_take_while():
    """Test take while predicate is true."""
    numbers = range(10)
    result = list(take_while(lambda x: x < 5, numbers))
    assert result == [0, 1, 2, 3, 4]


def test_chunk():
    """Test chunking iterable."""
    numbers = range(10)
    chunks = list(chunk(iter(numbers), 3))
    assert len(chunks) == 4
    assert chunks[0] == (0, 1, 2)
    assert chunks[1] == (3, 4, 5)
    assert chunks[2] == (6, 7, 8)
    assert chunks[3] == (9,)


def test_lazy_evaluation_efficiency():
    """Test that lazy evaluation doesn't compute everything."""
    def expensive_generator():
        for i in range(1000000):
            yield i
    
    # Take only first 5 elements - should be fast
    result = []
    for i, val in enumerate(expensive_generator()):
        if i >= 5:
            break
        result.append(val)
    
    assert len(result) == 5
    assert result == [0, 1, 2, 3, 4]
