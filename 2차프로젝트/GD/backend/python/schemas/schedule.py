# schemas/schedule.py
from datetime import date
from typing import List, Optional, Dict, Tuple
from pydantic import BaseModel

class Place(BaseModel):
    place_id: int
    name: str
    theme: str
    avg_rating: float
    address: str
    latitude: float
    longitude: float
    description: Optional[str]     = None
    heritage_type: Optional[str]   = None
    info_center: Optional[str]     = None
    closed_day: Optional[str]      = None
    experience_info: Optional[str] = None
    min_age: Optional[str]         = None
    business_hours: Optional[str]  = None
    parking_info: Optional[str]    = None
    details: Optional[str]         = None

    class Config:
        orm_mode = True  # SQLAlchemy 모델에서 바로 읽어올 수 있게


class DailyItinerary(BaseModel):
    day: int                  # 몇 일차
    places: List[Place]       # 그 날 추천 장소 리스트


class ItineraryResponse(BaseModel):
    itinerary: List[DailyItinerary]


class ItineraryRequest(BaseModel):
    region: str               # ex) "서울"
    theme: str
    start_date: date
    end_date: date
    per_day: int = 4


class ItineraryWithAccommodationRequest(ItineraryRequest):
    accommodation_coords: Dict[int, Tuple[float, float]]