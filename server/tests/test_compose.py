"""Tests for Lab 6 & 7: Composition and Services."""
import pytest
from core.compose import compose, pipe, partial, curry, identity, const


def test_compose():
    """Test function composition (right to left)."""
    add_one = lambda x: x + 1
    multiply_two = lambda x: x * 2
    
    composed = compose(multiply_two, add_one)
    result = composed(5)  # (5 + 1) * 2 = 12
    assert result == 12


def test_pipe():
    """Test function piping (left to right)."""
    add_one = lambda x: x + 1
    multiply_two = lambda x: x * 2
    
    piped = pipe(add_one, multiply_two)
    result = piped(5)  # (5 + 1) * 2 = 12
    assert result == 12


def test_partial():
    """Test partial application."""
    def add(a, b, c):
        return a + b + c
    
    add_5_and = partial(add, 5)
    result = add_5_and(3, 2)
    assert result == 10


def test_curry():
    """Test currying."""
    def add(x, y):
        return x + y
    
    curried = curry(add)
    add_5 = curried(5)
    result = add_5(3)
    assert result == 8


def test_identity():
    """Test identity function."""
    assert identity(42) == 42
    assert identity("hello") == "hello"


def test_const():
    """Test constant function."""
    always_42 = const(42)
    assert always_42() == 42
    assert always_42("ignored", "args") == 42


def test_compose_multiple():
    """Test composing multiple functions."""
    add_one = lambda x: x + 1
    multiply_two = lambda x: x * 2
    subtract_three = lambda x: x - 3
    
    result = compose(subtract_three, multiply_two, add_one)(10)
    # 10 + 1 = 11, 11 * 2 = 22, 22 - 3 = 19
    assert result == 19
