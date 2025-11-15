"""Tests for Lab 1: Pure functions, HOF, Immutability."""
import pytest
from core.domain import Hotel, Price
from core.transforms import (
    apply_to_all,
    filter_items,
    fold_left,
    compose,
    calculate_total_price,
    filter_hotels_by_city,
    filter_hotels_by_stars,
    get_hotel_names,
    group_by
)


def test_immutability():
    """Test that domain entities are immutable."""
    hotel = Hotel(id=1, name="Test Hotel", stars=5, city="Tashkent", features=("WiFi",))
    
    # Try to modify - should raise error
    with pytest.raises(Exception):
        hotel.name = "New Name"


def test_apply_to_all_hof():
    """Test Higher-Order Function: map."""
    hotels = (
        Hotel(1, "Hotel A", 5, "Tashkent", ()),
        Hotel(2, "Hotel B", 4, "Samarkand", ()),
    )
    
    names = apply_to_all(lambda h: h.name, hotels)
    assert names == ("Hotel A", "Hotel B")


def test_filter_items_hof():
    """Test Higher-Order Function: filter."""
    hotels = (
        Hotel(1, "Hotel A", 5, "Tashkent", ()),
        Hotel(2, "Hotel B", 4, "Tashkent", ()),
        Hotel(3, "Hotel C", 3, "Samarkand", ()),
    )
    
    luxury = filter_items(lambda h: h.stars >= 4, hotels)
    assert len(luxury) == 2
    assert all(h.stars >= 4 for h in luxury)


def test_fold_left_hof():
    """Test Higher-Order Function: reduce."""
    numbers = (1, 2, 3, 4, 5)
    total = fold_left(lambda acc, x: acc + x, 0, numbers)
    assert total == 15


def test_compose():
    """Test function composition."""
    add_one = lambda x: x + 1
    multiply_two = lambda x: x * 2
    
    composed = compose(multiply_two, add_one)
    result = composed(5)  # (5 + 1) * 2 = 12
    assert result == 12


def test_calculate_total_price():
    """Test pure function: calculate total price."""
    prices = (
        Price(1, 1, "2024-01-01", 10000, "UZS"),
        Price(2, 1, "2024-01-02", 15000, "UZS"),
        Price(3, 1, "2024-01-03", 20000, "UZS"),
    )
    
    total = calculate_total_price(prices)
    assert total == 45000


def test_filter_hotels_by_city():
    """Test domain function: filter by city."""
    hotels = (
        Hotel(1, "Hotel A", 5, "Tashkent", ()),
        Hotel(2, "Hotel B", 4, "Samarkand", ()),
        Hotel(3, "Hotel C", 5, "Tashkent", ()),
    )
    
    tashkent_hotels = filter_hotels_by_city(hotels, "Tashkent")
    assert len(tashkent_hotels) == 2
    assert all(h.city == "Tashkent" for h in tashkent_hotels)


def test_group_by():
    """Test grouping function."""
    hotels = (
        Hotel(1, "Hotel A", 5, "Tashkent", ()),
        Hotel(2, "Hotel B", 4, "Samarkand", ()),
        Hotel(3, "Hotel C", 5, "Tashkent", ()),
    )
    
    grouped = group_by(lambda h: h.city, hotels)
    assert len(grouped["Tashkent"]) == 2
    assert len(grouped["Samarkand"]) == 1
