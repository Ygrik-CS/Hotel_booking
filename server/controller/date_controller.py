from fastapi import FastAPI, APIRouter
from service.hotel_service import iter_available_days, lazy_offers
router = APIRouter(prefix="/date", tags=["Date"])


Avail_days = iter_available_days
Offers = lazy_offers

@router.get("/", response_model=int)
def available_days():
    return Avail_days

@router.get("/", response_model=tuple[dict, ...])
def lazy_offers():
    return Offers