"""Function composition utilities."""
from typing import Callable, TypeVar

T = TypeVar('T')


def compose(*functions: Callable) -> Callable:
    """Compose functions from right to left.
    
    compose(f, g, h)(x) == f(g(h(x)))
    """
    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return inner


def pipe(*functions: Callable) -> Callable:
    """Pipe functions from left to right.
    
    pipe(f, g, h)(x) == h(g(f(x)))
    """
    def inner(arg):
        result = arg
        for func in functions:
            result = func(result)
        return result
    return inner


def partial(func: Callable, *args, **kwargs) -> Callable:
    """Partial application of function."""
    def inner(*more_args, **more_kwargs):
        combined_kwargs = {**kwargs, **more_kwargs}
        return func(*args, *more_args, **combined_kwargs)
    return inner


def curry(func: Callable) -> Callable:
    """Curry a function (simplified version for 2 args)."""
    def outer(x):
        def inner(y):
            return func(x, y)
        return inner
    return outer


def identity(x: T) -> T:
    """Identity function."""
    return x


def const(x: T) -> Callable:
    """Constant function - always returns x."""
    def inner(*args, **kwargs):
        return x
    return inner
