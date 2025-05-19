# services/search.py
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Place as PlaceModel
from sqlalchemy import or_
from schemas.search import Place as PlaceSchema, CursorResponse

def search_places(
    db: Session,
    text: str,
    limit: int = 20,
    cursor_id: Optional[int] = None,
) -> CursorResponse:
    q = db.query(PlaceModel)
    
      # 1) 텍스트 검색 필터
    if text:
        pattern = f"%{text}%"
        # Postgres: ilike, MySQL은 .like() + collation 에 따라 대소문자 구분 안 되기도 함
        q = q.filter(
            or_(
                PlaceModel.name.ilike(pattern),
                PlaceModel.address.ilike(pattern),
            )
        )
    # (필요시) 텍스트 검색, 페이징 로직…
    if cursor_id:
        q = q.filter(PlaceModel.place_id < cursor_id)

    results: List[PlaceModel] = (
        q.order_by(
            PlaceModel.avg_rating.desc(),
            PlaceModel.place_id.desc())
         .limit(limit)
         .all()
    )

    # Pydantic 스키마 PlaceSchema로 변환
    places_out = [PlaceSchema.from_orm(p) for p in results]
    next_cursor = results[-1].place_id if len(results) == limit else None

    return CursorResponse(
        places=places_out,
        next_cursor={"cursor_id": next_cursor} if next_cursor else None,
        has_more=bool(next_cursor),
    )
