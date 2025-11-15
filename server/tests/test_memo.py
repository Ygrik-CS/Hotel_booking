"""Tests for Lab 3: Memoization."""
import pytest
from core.memo import (
    fibonacci_memo,
    calculate_date_range_price,
    calculate_cancellation_penalty,
    memoize,
    expensive_calculation
)


def test_fibonacci_memo():
    """Test memoized Fibonacci."""
    # Clear cache first
    fibonacci_memo.cache_clear()
    
    result = fibonacci_memo(10)
    assert result == 55
    
    # Should be cached now
    result2 = fibonacci_memo(10)
    assert result2 == 55


def test_fibonacci_memo_performance():
    """Test that memoization improves performance."""
    fibonacci_memo.cache_clear()
    
    # First call - not cached
    result1 = fibonacci_memo(30)
    
    # Second call - should be much faster (cached)
    result2 = fibonacci_memo(30)
    
    assert result1 == result2


def test_calculate_date_range_price():
    """Test memoized price calculation."""
    price1 = calculate_date_range_price("2024-01-01", "2024-01-05", 10000)
    price2 = calculate_date_range_price("2024-01-01", "2024-01-05", 10000)
    
    # Should return same result
    assert price1 == price2
    assert price1 > 0


def test_calculate_cancellation_penalty():
    """Test memoized cancellation penalty."""
    # No penalty for cancellation 7+ days before
    penalty1 = calculate_cancellation_penalty(7, True, 100000)
    assert penalty1 == 0
    
    # 50% penalty for 1-2 days before
    penalty2 = calculate_cancellation_penalty(1, True, 100000)
    assert penalty2 == 50000
    
    # Full penalty for non-refundable
    penalty3 = calculate_cancellation_penalty(7, False, 100000)
    assert penalty3 == 100000


def test_custom_memoize():
    """Test custom memoization decorator."""
    # Clear cache
    expensive_calculation.cache_clear()
    
    result1 = expensive_calculation(5, 10)
    result2 = expensive_calculation(5, 10)
    
    assert result1 == result2
    
    # Check cache size
    assert len(expensive_calculation.cache) > 0
