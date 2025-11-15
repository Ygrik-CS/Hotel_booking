"""Immutable domain entities."""
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass(frozen=True)
class Hotel:
    """Immutable hotel entity."""
    id: int
    name: str
    stars: int
    city: str
    features: Tuple[str, ...] = ()


@dataclass(frozen=True)
class RoomType:
    """Immutable room type entity."""
    id: int
    hotel_id: int
    name: str
    capacity: int
    beds: Tuple[str, ...] = ()
    features: Tuple[str, ...] = ()


@dataclass(frozen=True)
class RatePlan:
    """Immutable rate plan entity."""
    id: int
    hotel_id: int
    room_type_id: int
    title: str
    meal: str
    refundable: bool
    cancel_before_days: int


@dataclass(frozen=True)
class Price:
    """Immutable price entity."""
    id: int
    rate_id: int
    date: str
    amount: int
    currency: str = "UZS"


@dataclass(frozen=True)
class Availability:
    """Immutable availability entity."""
    id: int
    room_type_id: int
    date: str
    available: int


@dataclass(frozen=True)
class Guest:
    """Immutable guest entity."""
    id: int
    name: str
    email: str


@dataclass(frozen=True)
class CartItem:
    """Immutable cart item entity."""
    id: int
    hotel_id: int
    room_type_id: int
    rate_id: int
    checkin: str
    checkout: str
    guests: int


@dataclass(frozen=True)
class Booking:
    """Immutable booking entity."""
    id: int
    guest_id: int
    items: Tuple[CartItem, ...]
    total: int
    status: str


@dataclass(frozen=True)
class Payment:
    """Immutable payment entity."""
    id: int
    booking_id: int
    amount: int
    ts: str
    method: str


@dataclass(frozen=True)
class Event:
    """Immutable event entity for FRP."""
    id: int
    ts: str
    name: str
    payload: Tuple[Tuple[str, str], ...]  # tuple of key-value pairs


@dataclass(frozen=True)
class Rule:
    """Immutable business rule entity."""
    id: int
    kind: str
    payload: Tuple[Tuple[str, str], ...]  # tuple of key-value pairs


@dataclass(frozen=True)
class SearchOffer:
    """Immutable search offer entity."""
    hotel: Hotel
    room_type: RoomType
    rate_plan: RatePlan
    total_price: int
    available: bool
