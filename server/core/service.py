"""Service facades - composition of pure functions."""
from typing import Tuple, Dict, Any
from core.domain import Hotel, SearchOffer
from core.transforms import (
    filter_hotels_by_city,
    filter_hotels_by_stars,
    sort_by_price,
    filter_available_offers,
    take
)
from core.compose import compose, pipe
from core.lazy import lazy_search_offers
import itertools


class SearchService:
    """Search service - facade for hotel search operations."""
    
    @staticmethod
    def search(
        all_hotels: Tuple[Hotel, ...],
        city: str,
        checkin: str,
        checkout: str,
        guests: int,
        min_stars: int = 0,
        limit: int = 50
    ) -> Tuple[SearchOffer, ...]:
        """Search for hotel offers using function composition."""
        # Filter hotels by criteria
        filtered_hotels = compose(
            lambda hotels: filter_hotels_by_stars(hotels, min_stars) if min_stars > 0 else hotels,
            lambda hotels: filter_hotels_by_city(hotels, city)
        )(all_hotels)
        
        return filtered_hotels
    
    @staticmethod
    def search_lazy(
        all_hotels: Tuple[Hotel, ...],
        room_types_map: dict,
        rates_map: dict,
        availability_map: dict,
        prices_map: dict,
        city: str,
        checkin: str,
        checkout: str,
        limit: int = 50
    ):
        """Lazy search using generators."""
        filtered_hotels = filter_hotels_by_city(all_hotels, city)
        
        offers = lazy_search_offers(
            filtered_hotels,
            room_types_map,
            rates_map,
            availability_map,
            prices_map,
            checkin,
            checkout
        )
        
        # Take first N offers lazily
        return tuple(itertools.islice(offers, limit))


class QuoteService:
    """Quote service - facade for price calculations."""
    
    @staticmethod
    def calculate_quote(
        rate_id: int,
        checkin: str,
        checkout: str,
        prices_map: dict
    ) -> int:
        """Calculate quote for a rate and date range."""
        from core.recursion import split_date_range
        from core.transforms import fold_left
        
        dates = split_date_range(checkin, checkout)
        prices = tuple(prices_map.get((rate_id, date), 0) for date in dates)
        return fold_left(lambda acc, price: acc + price, 0, prices)
    
    @staticmethod
    def compare_offers(offers: Tuple[SearchOffer, ...]) -> Dict[str, Any]:
        """Compare offers and return statistics."""
        if not offers:
            return {"min": 0, "max": 0, "avg": 0, "count": 0}
        
        prices = tuple(offer.total_price for offer in offers)
        return {
            "min": min(prices),
            "max": max(prices),
            "avg": sum(prices) // len(prices),
            "count": len(offers)
        }


class BookingService:
    """Booking service - facade for booking operations."""
    
    @staticmethod
    def validate_booking(
        guest_id: int,
        total: int,
        cart_items: Tuple
    ) -> bool:
        """Validate booking data."""
        from core.ftypes import validate_positive
        
        guest_valid = validate_positive(guest_id, "guest_id").is_right()
        total_valid = validate_positive(total, "total").is_right()
        items_valid = len(cart_items) > 0
        
        return guest_valid and total_valid and items_valid
    
    @staticmethod
    def calculate_cancellation_penalty(
        refundable: bool,
        cancel_before_days: int,
        days_until_checkin: int,
        total_amount: int
    ) -> int:
        """Calculate cancellation penalty."""
        from core.memo import calculate_cancellation_penalty
        return calculate_cancellation_penalty(
            days_until_checkin,
            refundable,
            total_amount
        )


class FilterService:
    """Filter service - facade for filtering operations."""
    
    @staticmethod
    def apply_filters(
        offers: Tuple[SearchOffer, ...],
        min_price: int = 0,
        max_price: int = float('inf'),
        min_stars: int = 0,
        sort_by: str = "price"
    ) -> Tuple[SearchOffer, ...]:
        """Apply multiple filters to offers."""
        # Compose filter pipeline
        pipeline = pipe(
            lambda offers: tuple(o for o in offers if o.total_price >= min_price),
            lambda offers: tuple(o for o in offers if o.total_price <= max_price),
            lambda offers: tuple(o for o in offers if o.hotel.stars >= min_stars),
            lambda offers: filter_available_offers(offers),
            lambda offers: sort_by_price(offers) if sort_by == "price" else offers
        )
        
        return pipeline(offers)
