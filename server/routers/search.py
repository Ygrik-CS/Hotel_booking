"""Search routers."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db
from controllers.search_controller import SearchController


router = APIRouter(prefix="/search", tags=["Search"])


class SearchRequest(BaseModel):
    city: str
    checkin: str
    checkout: str
    guests: int = 1


@router.post("/")
async def search_hotels(
    search_data: SearchRequest,
    db: Session = Depends(get_db)
):
    """Search for available hotels."""
    return SearchController.search_hotels(
        db=db,
        city=search_data.city,
        checkin=search_data.checkin,
        checkout=search_data.checkout,
        guests=search_data.guests
    )


@router.get("/")
async def search_hotels_get(
    city: str = Query(...),
    checkin: str = Query(...),
    checkout: str = Query(...),
    guests: int = Query(1),
    db: Session = Depends(get_db)
):
    """Search for available hotels (GET method)."""
    return SearchController.search_hotels(
        db=db,
        city=city,
        checkin=checkin,
        checkout=checkout,
        guests=guests
    )
