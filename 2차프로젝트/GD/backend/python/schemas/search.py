from typing import List, Optional
from pydantic import BaseModel


class SearchRequest(BaseModel):
    text: str
    limit: int = 20
    cursor_id: Optional[int] = None


class Place(BaseModel):
    place_id: int
    name: str
    theme: str
    avg_rating: float
    address: str
    latitude: float
    longitude: float
    description: Optional[str]       = None
    heritage_type: Optional[str]     = None
    info_center: Optional[str]       = None
    closed_day: Optional[str]        = None
    experience_info: Optional[str]   = None
    min_age: Optional[str]           = None
    business_hours: Optional[str]    = None
    parking_info: Optional[str]      = None
    details: Optional[str]           = None

    class Config:
        from_attributes=True

class CursorResponse(BaseModel):
    places: List[Place]
    next_cursor: Optional[dict] = None
    has_more: bool