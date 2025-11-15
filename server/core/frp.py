"""Functional Reactive Programming - Event Bus."""
from dataclasses import dataclass
from typing import Dict, List, Callable
from core.domain import Event as DomainEvent


class EventBus:
    """Event bus for functional reactive programming."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, handler: Callable):
        """Subscribe to an event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
    
    def unsubscribe(self, event_name: str, handler: Callable):
        """Unsubscribe from an event."""
        if event_name in self._subscribers:
            self._subscribers[event_name].remove(handler)
    
    def publish(self, event: DomainEvent):
        """Publish an event to all subscribers."""
        if event.name in self._subscribers:
            for handler in self._subscribers[event.name]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in event handler: {e}")
    
    def clear(self):
        """Clear all subscribers."""
        self._subscribers.clear()
    
    def get_subscriber_count(self, event_name: str) -> int:
        """Get number of subscribers for an event."""
        return len(self._subscribers.get(event_name, []))


# Global event bus instance
event_bus = EventBus()


# Event types
EVENT_SEARCH = "SEARCH"
EVENT_HOLD = "HOLD"
EVENT_BOOKED = "BOOKED"
EVENT_CANCELLED = "CANCELLED"
EVENT_PAYMENT = "PAYMENT"
EVENT_PRICE_CHANGED = "PRICE_CHANGED"


# Helper functions for creating events
def create_event(name: str, **kwargs) -> DomainEvent:
    """Create an event with payload."""
    from datetime import datetime
    payload = tuple((k, str(v)) for k, v in kwargs.items())
    return DomainEvent(
        id=0,  # Will be set by database
        ts=datetime.now().isoformat(),
        name=name,
        payload=payload
    )


# Example event handlers
def log_event(event: DomainEvent):
    """Log event to console."""
    print(f"[{event.ts}] {event.name}: {dict(event.payload)}")


def save_event_to_db(event: DomainEvent):
    """Save event to database."""
    # This would be implemented in the controller layer
    pass
