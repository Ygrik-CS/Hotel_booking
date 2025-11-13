from fastapi import FastAPI, APIRouter
from models.Hotel import Hotel
from models.CartItem import CartItem
from models.Availability import Availability
from typing import List
from models.Price import Price

router = APIRouter(prefix="/filter", tags=["Filter"])

City: list[Hotel] = []
Capacity: list[Availability] = []
Features: list[Hotel.features]
Prices: list[Price]

@router.get("/", response_model=List[City])
def get_filter_city():
    return City 

@router.get("/", response_model=List[Capacity])
def get_filter_capacity():
    return Capacity

@router.get("/", response_model=List[Features])
def filter_features():
    return Features

@router.get("/", response_model=List[Prices])
def filter_price():
    return Prices