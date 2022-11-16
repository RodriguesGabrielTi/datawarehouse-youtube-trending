import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, relationship, backref

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

    @classmethod
    def get_weekday(cls, i: int):
        return cls._all[i]


class DimensionTime(Base, Timestamp):
    __tablename__ = 'dimension_time'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    day = Column(String())
    month = Column(String())
    year = Column(String())
    weekday = Column(String())

    @validates('weekday')
    def validate_weekday(self, _, weekday):
        assert Weekdays.is_valid(weekday), 'Invalid weekday'
        return weekday


class DimensionView(Base, Timestamp):
    __tablename__ = 'dimension_view'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String())
    max_value = Column(Integer())
    min_value = Column(Integer())


class DimensionInteraction(Base, Timestamp):
    __tablename__ = 'dimension_interaction'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String())
    max_value = Column(Float())
    min_value = Column(Float())


class Category(Base, Timestamp):
    __tablename__ = 'category'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = Column(Integer, unique=True)
    name = Column(String)


class Tag(Base, Timestamp):
    __tablename__ = 'tag'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)


class FactVideo(Base, Timestamp):
    __tablename__ = 'fact_video'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    video_id = Column(String(250), nullable=False)
    trending_date = Column(String(36), ForeignKey('dimension_time.id'), nullable=False)
    title = Column(String)
    channel_title = Column(String)
    publish_time = Column(String(36), ForeignKey('dimension_time.id'), nullable=False)
    view_group_id = Column(String(36), ForeignKey('dimension_view.id', ondelete='SET NULL'))
    interation_group_id = Column(String(36), ForeignKey('dimension_interaction.id', ondelete='SET NULL'))
    ratings_disabled = Column(Boolean)
    video_error_or_removed = Column(Boolean)
    trending_location = Column(String)
    description = Column(String)
    likes = Column(Integer)
    dislikes = Column(Integer)
    comment_count = Column(Integer)
    views = Column(Integer)
    interactions_points = Column(Float)
    category_id = Column(String(36), ForeignKey('category.id'), nullable=False)

    interation_group = relationship("DimensionInteraction", backref=backref('dimension_interaction', passive_deletes=True))
    view_group = relationship("DimensionView", backref=backref('dimension_view', passive_deletes=True))

class VideoTag(Base, Timestamp):
    __tablename__ = 'video_tag'

    tag_id = Column(String(36), ForeignKey('tag.id'), nullable=False, primary_key=True)
    video_id = Column(String(36), ForeignKey('fact_video.id'), nullable=False, primary_key=True)
