import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, relationship

Base = declarative_base()


class Timestamp(object):
    created = Column(DateTime, default=lambda: datetime.utcnow(), nullable=True)
    updated = Column(DateTime, default=lambda: datetime.utcnow(), nullable=True)


class Weekdays:
    monday = 'Segunda-Feira'
    tuesday = 'Terça-Feira'
    wednesday = 'Quarta-Feira'
    thursday = "Quinta-Feira"
    friday = "Sexta-feira"
    saturday = "Sábado"
    sunday = "Domingo"

    _all = [
        monday,
        tuesday,
        wednesday,
        thursday,
        friday,
        saturday,
        sunday,
    ]

    @classmethod
    def is_valid(cls, weekday):
        return weekday in cls._all


class DimensionTime(Base, Timestamp):
    __tablename__ = 'dimension_time'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    day = Column(String())
    month = Column(String(), primary_key=True)
    year = Column(String(), primary_key=True)
    weekday = Column(String())

    @validates('weekday')
    def validate_weekday(self, _, weekday):
        assert Weekdays.is_valid(weekday), 'Invalid weekday'
        return weekday


class DimensionView(Base, Timestamp):
    __tablename__ = 'dimension_view'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String())


class DimensionInteraction(Base, Timestamp):
    __tablename__ = 'dimension_interaction'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String())


class FactVideo(Base, Timestamp):
    __tablename__ = 'fact_video'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    video_id = Column(String(250), primary_key=True)
    trending_date = Column(String(36), ForeignKey('dimension_time.id'), nullable=False)
    title = Column(String)
    channel_title = Column(String)
    publish_time = Column(String(36), ForeignKey('dimension_time.id'), nullable=False)
    view_group = Column(String(36), ForeignKey('dimension_view.id'), nullable=False)
    interation_group = Column(String(36), ForeignKey('dimension_interaction.id'), nullable=False)
    ratings_disabled = Column(Boolean)
    video_error_or_removed = Column(Boolean)
    post_location = Column(String)
    trending_location = Column(String)
    description = Column(String)
    likes = Column(Integer)
    dislikes = Column(Integer)
    comment_count = Column(Integer)
