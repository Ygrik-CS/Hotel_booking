"""Search controller with functional approach."""
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from models.Hotel import Hotel as HotelModel
from models.room_type import RoomType as RoomTypeModel
from models.rate_plan import RatePlan as RatePlanModel
from models.Price import Price as PriceModel
from models.Availability import Availability as AvailabilityModel
from core.transforms import filter_hotels_by_city
from core.recursion import split_date_range
from core.frp import event_bus, create_event, EVENT_SEARCH
from controllers.hotel_controller import HotelController
import json


class SearchController:
    """Search business logic using functional approach."""
    
    @staticmethod
    def search_hotels(
        db: Session,
        city: str,
        checkin: str,
        checkout: str,
        guests: int = 1
    ) -> List[dict]:
        """Search for available hotels."""
        # Publish search event
        event = create_event(EVENT_SEARCH, city=city, checkin=checkin, checkout=checkout)
        event_bus.publish(event)
        
        # Get all hotels in city
        hotels = db.query(HotelModel).filter(HotelModel.city.ilike(f"%{city}%")).all()
        
        if not hotels:
            return []
        
        # Get date range
        dates = split_date_range(checkin, checkout)
        
        results = []
        
        for hotel in hotels:
            # Get room types
            room_types = db.query(RoomTypeModel).filter(
                RoomTypeModel.hotel_id == hotel.id,
                RoomTypeModel.capacity >= guests
            ).all()
            
            for room_type in room_types:
                # Check availability for all dates
                availabilities = db.query(AvailabilityModel).filter(
                    AvailabilityModel.room_type_id == room_type.id,
                    AvailabilityModel.date.in_(dates)
                ).all()
                
                if len(availabilities) < len(dates):
                    continue
                
                is_available = all(a.available > 0 for a in availabilities)
                
                if not is_available:
                    continue
                
                # Get rate plans
                rate_plans = db.query(RatePlanModel).filter(
                    RatePlanModel.room_type_id == room_type.id
                ).all()
                
                for rate_plan in rate_plans:
                    # Calculate total price
                    prices = db.query(PriceModel).filter(
                        PriceModel.rate_id == rate_plan.id,
                        PriceModel.date.in_(dates)
                    ).all()
                    
                    if len(prices) < len(dates):
                        continue
                    
                    total_price = sum(p.amount for p in prices)
                    
                    results.append({
                        "hotel": {
                            "id": hotel.id,
                            "name": hotel.name,
                            "stars": hotel.stars,
                            "city": hotel.city
                        },
                        "room_type": {
                            "id": room_type.id,
                            "name": room_type.name,
                            "capacity": room_type.capacity
                        },
                        "rate_plan": {
                            "id": rate_plan.id,
                            "title": rate_plan.title,
                            "meal": rate_plan.meal,
                            "refundable": rate_plan.refundable
                        },
                        "total_price": total_price,
                        "currency": "UZS",
                        "nights": len(dates),
                        "available": True
                    })
        
        # Sort by price
        results.sort(key=lambda x: x["total_price"])
        
        return results[:50]  # Limit to 50 results
