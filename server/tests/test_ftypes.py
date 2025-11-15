"""Tests for Lab 4: Maybe and Either monads."""
import pytest
from core.ftypes import (
    Maybe,
    Either,
    validate_positive,
    validate_email,
    validate_non_empty,
    validate_date_range
)


def test_maybe_just():
    """Test Maybe with value."""
    maybe = Maybe.just(42)
    assert maybe.is_just()
    assert not maybe.is_nothing()
    assert maybe.value == 42


def test_maybe_nothing():
    """Test Maybe without value."""
    maybe = Maybe.nothing()
    assert maybe.is_nothing()
    assert not maybe.is_just()


def test_maybe_map():
    """Test Maybe map operation."""
    maybe = Maybe.just(10)
    result = maybe.map(lambda x: x * 2)
    assert result.value == 20
    
    # Map on nothing returns nothing
    nothing = Maybe.nothing()
    result2 = nothing.map(lambda x: x * 2)
    assert result2.is_nothing()


def test_maybe_flat_map():
    """Test Maybe flat_map operation."""
    maybe = Maybe.just(10)
    result = maybe.flat_map(lambda x: Maybe.just(x * 2))
    assert result.value == 20


def test_maybe_get_or_else():
    """Test Maybe get_or_else."""
    maybe = Maybe.just(42)
    assert maybe.get_or_else(0) == 42
    
    nothing = Maybe.nothing()
    assert nothing.get_or_else(0) == 0


def test_either_right():
    """Test Either with success value."""
    either = Either.right(42)
    assert either.is_right()
    assert not either.is_left()
    assert either.get_right() == 42


def test_either_left():
    """Test Either with error."""
    either = Either.left("Error occurred")
    assert either.is_left()
    assert not either.is_right()
    assert either.get_left() == "Error occurred"


def test_either_map():
    """Test Either map operation."""
    either = Either.right(10)
    result = either.map(lambda x: x * 2)
    assert result.get_right() == 20
    
    # Map on left returns left
    error = Either.left("Error")
    result2 = error.map(lambda x: x * 2)
    assert result2.is_left()


def test_validate_positive():
    """Test positive number validation."""
    result = validate_positive(10, "amount")
    assert result.is_right()
    assert result.get_right() == 10
    
    result2 = validate_positive(-5, "amount")
    assert result2.is_left()
    assert "positive" in result2.get_left()


def test_validate_email():
    """Test email validation."""
    result = validate_email("test@example.com")
    assert result.is_right()
    
    result2 = validate_email("invalid-email")
    assert result2.is_left()


def test_validate_non_empty():
    """Test non-empty string validation."""
    result = validate_non_empty("Hello", "name")
    assert result.is_right()
    
    result2 = validate_non_empty("", "name")
    assert result2.is_left()


def test_validate_date_range():
    """Test date range validation."""
    result = validate_date_range("2024-01-01", "2024-01-05")
    assert result.is_right()
    
    # Invalid range (end before start)
    result2 = validate_date_range("2024-01-05", "2024-01-01")
    assert result2.is_left()


def test_either_chaining():
    """Test chaining Either operations."""
    result = (
        validate_positive(10, "amount")
        .flat_map(lambda _: validate_email("test@example.com"))
    )
    assert result.is_right()
    
    # Chain with error
    result2 = (
        validate_positive(-5, "amount")
        .flat_map(lambda _: validate_email("test@example.com"))
    )
    assert result2.is_left()
