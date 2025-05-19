# services/schedule.py
import numpy as np
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session
from datetime import timedelta
from collections import defaultdict

from models import Itinerary, ScheduleSlot, Place
from schemas.schedule import DailyItinerary, Place as PlaceSchema

class ItineraryService:

    @staticmethod
    def generate_without_accommodation(
        db: Session,
        region: str,
        theme: str,
        start_date,                # datetime.date
        duration: int, 
        per_day: int = 4,
        user_id: int = None,
        preference_id: int = None,
    ) -> list[DailyItinerary]:
        # 1) 후보 장소 필터링 (주소에 region 포함 + theme 일치)
        places = (
            db.query(Place)
              .filter(Place.address.contains(region))
              .filter(Place.theme == theme)
              .all()
        )
        if not places:
            return []

        # 2) 전체 클러스터링
        coords = np.array([[float(p.latitude), float(p.longitude)] for p in places])
        total_clusters = min(duration * per_day, len(places))
        kmeans = KMeans(n_clusters=total_clusters, random_state=42).fit(coords)
        labels = kmeans.labels_

        # 3) 클러스터별 평균 평점 계산 → 내림차순 정렬
        cluster_idxs = defaultdict(list)
        for idx, lbl in enumerate(labels):
            cluster_idxs[lbl].append(idx)

        cluster_scores = [
            (lbl, np.mean([float(places[i].avg_rating or 0) for i in idxs]))
            for lbl, idxs in cluster_idxs.items()
        ]
        sorted_labels = [lbl for lbl, _ in sorted(cluster_scores, key=lambda x: -x[1])]

        # 4) DB에 Itinerary 저장 (옵션)
        itin = Itinerary(
            user_id=user_id,
            preference_id=preference_id,
            start_date=start_date,
            end_date=start_date + timedelta(days=duration-1),
            created_at=start_date,
        )
        db.add(itin)
        db.flush()  # itin.itinerary_id 확보

        # 5) 일차별 DailyItinerary 생성
        daily = []
        for day in range(duration):
            # 이 날에 해당하는 k개의 클러스터
            sel_lbls = sorted_labels[day * per_day : day * per_day + per_day]
            # 클러스터별 장소 인덱스 모아서 평점순으로 정렬
            idxs = [i for lbl in sel_lbls for i in cluster_idxs[lbl]]
            idxs = sorted(idxs, key=lambda i: -float(places[i].avg_rating or 0))[:per_day]

            # ScheduleSlot 으로 DB 저장
            for i in idxs:
                slot = ScheduleSlot(
                    itinerary_id=itin.itinerary_id,
                    place_id=places[i].place_id,
                    travel_date=start_date + timedelta(days=day)
                )
                db.add(slot)

            # Day 별 응답용 객체
            daily.append(
                DailyItinerary(
                    day=day+1,
                    places=[PlaceSchema.from_orm(places[i]) for i in idxs]
                )
            )

        db.commit()
        return daily


    @staticmethod
    def generate_with_accommodation(
        db: Session,
        region: str,
        theme: str,
        accommodation_coords: dict[int, tuple[float, float]],
        start_date,
        duration: int,
        per_day: int = 4,
        user_id: int = None,
        preference_id: int = None,
    ) -> list[DailyItinerary]:
        # 1) 기본 후보 필터링
        base = (
            db.query(Place)
              .filter(Place.address.contains(region))
              .filter(Place.theme == theme)
              .all()
        )
        if not base:
            return []

        # 2) Itinerary 저장
        itin = Itinerary(
            user_id=user_id,
            preference_id=preference_id,
            start_date=start_date,
            end_date=start_date + timedelta(days=duration-1),
            created_at=start_date,
        )
        db.add(itin)
        db.flush()

        used = set()
        daily = []

        for day in range(1, duration+1):
            center = accommodation_coords.get(day)
            # 3) 숙소 근처 후보 or 남은 전체
            if center:
                lat0, lon0 = center
                cand = [
                    p for p in base if p.place_id not in used
                    and abs(float(p.latitude)-lat0)<=0.3
                    and abs(float(p.longitude)-lon0)<=0.3
                ]
            else:
                cand = [p for p in base if p.place_id not in used]

            if not cand:
                daily.append(DailyItinerary(day=day, places=[]))
                continue

            # 4) k-means 로 하루치 클러스터 (k = per_day)
            coords = np.array([[float(p.latitude), float(p.longitude)] for p in cand])
            k = min(per_day, len(cand))
            km = KMeans(n_clusters=k, random_state=42).fit(coords)

            chosen_idxs = []
            for cluster_idx in range(k):
                pts = np.where(km.labels_==cluster_idx)[0]
                # 중심과 가장 가까운 포인트 선택
                closest = min(pts, key=lambda i: np.linalg.norm(coords[i]-km.cluster_centers_[cluster_idx]))
                chosen_idxs.append(closest)

            # 5) DB 저장 & 응답 리스트에 추가
            places_today = []
            for idx in chosen_idxs:
                p = cand[idx]
                used.add(p.place_id)
                slot = ScheduleSlot(
                    itinerary_id=itin.itinerary_id,
                    place_id=p.place_id,
                    travel_date=start_date + timedelta(days=day-1)
                )
                db.add(slot)
                places_today.append(PlaceSchema.from_orm(p))

            daily.append(DailyItinerary(day=day, places=places_today))

        db.commit()
        return daily