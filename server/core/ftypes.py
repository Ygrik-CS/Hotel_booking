"""Maybe and Either monads for safe error handling."""
from dataclasses import dataclass
from typing import Optional, TypeVar, Generic, Callable
import re

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')


@dataclass(frozen=True)
class Maybe(Generic[T]):
    """Maybe monad for handling optional values."""
    value: Optional[T]
    
    @staticmethod
    def just(value: T) -> 'Maybe[T]':
        """Create a Maybe with a value."""
        return Maybe(value)
    
    @staticmethod
    def nothing() -> 'Maybe[T]':
        """Create an empty Maybe."""
        return Maybe(None)
    
    def is_just(self) -> bool:
        """Check if Maybe has a value."""
        return self.value is not None
    
    def is_nothing(self) -> bool:
        """Check if Maybe is empty."""
        return self.value is None
    
    def map(self, func: Callable[[T], U]) -> 'Maybe[U]':
        """Apply function to value if present."""
        if self.is_just():
            return Maybe.just(func(self.value))
        return Maybe.nothing()
    
    def flat_map(self, func: Callable[[T], 'Maybe[U]']) -> 'Maybe[U]':
        """Monadic bind operation."""
        if self.is_just():
            return func(self.value)
        return Maybe.nothing()
    
    def get_or_else(self, default: T) -> T:
        """Get value or return default."""
        return self.value if self.is_just() else default
    
    def or_else(self, alternative: 'Maybe[T]') -> 'Maybe[T]':
        """Return alternative if empty."""
        return self if self.is_just() else alternative


@dataclass(frozen=True)
class Either(Generic[E, T]):
    """Either monad for error handling."""
    _left: Optional[E] = None
    _right: Optional[T] = None
    
    @staticmethod
    def left(error: E) -> 'Either[E, T]':
        """Create an Either with error."""
        return Either(_left=error, _right=None)
    
    @staticmethod
    def right(value: T) -> 'Either[E, T]':
        """Create an Either with value."""
        return Either(_left=None, _right=value)
    
    def is_left(self) -> bool:
        """Check if Either contains error."""
        return self._left is not None
    
    def is_right(self) -> bool:
        """Check if Either contains value."""
        return self._right is not None
    
    def map(self, func: Callable[[T], U]) -> 'Either[E, U]':
        """Apply function to value if right."""
        if self.is_right():
            return Either.right(func(self._right))
        return Either.left(self._left)
    
    def flat_map(self, func: Callable[[T], 'Either[E, U]']) -> 'Either[E, U]':
        """Monadic bind operation."""
        if self.is_right():
            return func(self._right)
        return Either.left(self._left)
    
    def get_left(self) -> E:
        """Get error value."""
        return self._left
    
    def get_right(self) -> T:
        """Get success value."""
        return self._right
    
    def get_or_else(self, default: T) -> T:
        """Get value or return default."""
        return self._right if self.is_right() else default


# Validation functions using Either
def validate_positive(value: int, field_name: str) -> Either[str, int]:
    """Validate that value is positive."""
    if value > 0:
        return Either.right(value)
    return Either.left(f"{field_name} must be positive")


def validate_non_empty(value: str, field_name: str) -> Either[str, str]:
    """Validate that string is not empty."""
    if value and value.strip():
        return Either.right(value)
    return Either.left(f"{field_name} cannot be empty")


def validate_email(email: str) -> Either[str, str]:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return Either.right(email)
    return Either.left("Invalid email format")


def validate_date_range(start: str, end: str) -> Either[str, tuple[str, str]]:
    """Validate date range."""
    try:
        from datetime import datetime
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        if start_dt < end_dt:
            return Either.right((start, end))
        return Either.left("End date must be after start date")
    except ValueError:
        return Either.left("Invalid date format")
