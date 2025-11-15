"""Routers package."""
from .auth import router as auth_router
from .hotel import router as hotel_router
from .search import router as search_router
from .cart import router as cart_router
from .booking import router as booking_router
from .payment import router as payment_router

__all__ = [
    "auth_router",
    "hotel_router",
    "search_router",
    "cart_router",
    "booking_router",
    "payment_router",
]
