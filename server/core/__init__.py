"""Core package - functional programming utilities."""
from .domain import (
    Hotel, RoomType, RatePlan, Price, Availability,
    Guest, CartItem, Booking, Payment, Event, Rule, SearchOffer
)
from .transforms import (
    apply_to_all, filter_items, fold_left, compose,
    calculate_total_price, filter_hotels_by_city, filter_hotels_by_stars
)
from .recursion import split_date_range, flatten_tuple, filter_tree
from .memo import fibonacci_memo, calculate_date_range_price, memoize
from .ftypes import Maybe, Either, validate_positive, validate_email, validate_non_empty
from .lazy import lazy_search_offers, generate_calendar
from .frp import EventBus, event_bus, create_event
from .service import SearchService, QuoteService, BookingService, FilterService

__all__ = [
    # Domain
    "Hotel", "RoomType", "RatePlan", "Price", "Availability",
    "Guest", "CartItem", "Booking", "Payment", "Event", "Rule", "SearchOffer",
    # Transforms
    "apply_to_all", "filter_items", "fold_left", "compose",
    "calculate_total_price", "filter_hotels_by_city", "filter_hotels_by_stars",
    # Recursion
    "split_date_range", "flatten_tuple", "filter_tree",
    # Memoization
    "fibonacci_memo", "calculate_date_range_price", "memoize",
    # FTypes
    "Maybe", "Either", "validate_positive", "validate_email", "validate_non_empty",
    # Lazy
    "lazy_search_offers", "generate_calendar",
    # FRP
    "EventBus", "event_bus", "create_event",
    # Services
    "SearchService", "QuoteService", "BookingService", "FilterService",
]
