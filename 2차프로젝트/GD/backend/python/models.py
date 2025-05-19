from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class AppUser(Base):
    __tablename__ = 'app_user'

    userId = Column(Integer, primary_key=True)
    userEmail = Column(String(200), nullable=False)
    password = Column(String(100), nullable=False)
    userPassword = Column(String(50), nullable=False)
    userName = Column(String(200), nullable=False)
    userSex = Column(String(5), nullable=False)
    userBirth = Column(String(20), nullable=False)
    createdAt = Column(Date, nullable=False)

    # 관계정리
    preferences = relationship('UserPreference', back_populates='user', cascade='all, delete-orphan')
    itineraries = relationship('Itinerary', back_populates='user', cascade='all, delete-orphan')


class UserPreference(Base):
    __tablename__ = 'user_preference'

    preference_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('app_user.user_id'), nullable=False)
    theme = Column(String(100), nullable=False)
    duration = Column(String(50), nullable=False)
    region = Column(String(100), nullable=False)

    # 관계정리
    user = relationship('AppUser', back_populates='preferences')
    itineraries = relationship('Itinerary', back_populates='preference', cascade='all, delete-orphan')


class Itinerary(Base):
    __tablename__ = 'itinerary'

    itinerary_id = Column(Integer, primary_key=True)
    preference_id = Column(Integer, ForeignKey('user_preference.preference_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('app_user.user_id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(Date, nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)

    # 관계정리
    preference = relationship('UserPreference', back_populates='itineraries')
    user = relationship('AppUser', back_populates='itineraries')
    slots = relationship('ScheduleSlot', back_populates='itinerary', cascade='all, delete-orphan')


class Place(Base):
    __tablename__ = 'place'

    place_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    theme = Column(String(80), nullable=False)
    avg_rating = Column(Numeric(3, 2))
    address = Column(String(200), nullable=False)
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)
    description = Column(Text)
    heritage_type = Column(String(50))
    info_center = Column(String(2000))
    closed_day = Column(String(2000))
    experience_info = Column(Text)
    min_age = Column(String(2000))
    business_hours = Column(String(2000))
    parking_info = Column(String(2000))
    details = Column(Text)
    image = Column(str(2000))

    # 관계정리
    images = relationship('PlaceImage', back_populates='place', cascade='all, delete-orphan')
    slots = relationship('ScheduleSlot', back_populates='place', cascade='all, delete-orphan')



class ScheduleSlot(Base):
    __tablename__ = 'schedule_slot'

    slot_id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey('itinerary.itinerary_id'), nullable=False)
    place_id = Column(Integer, ForeignKey('place.place_id'), nullable=False)
    travel_date = Column(Date, nullable=False)

    # 관계정리
    itinerary = relationship('Itinerary', back_populates='slots')
    place = relationship('Place', back_populates='slots')
