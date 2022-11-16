import datetime
from operator import or_, and_

from database.connection import session
from domain.models import FactVideo, DimensionTime, Weekdays, Category, DimensionView, DimensionInteraction, Tag, \
    VideoTag


class VideoBuilder:
    groups = ["altissimo", "alto", "medio", "baixo","muito baixo"]

    def __init__(self):
        self.__video = None
        self.__tags = set()

    @staticmethod
    def get_interactions_group(value):
        return session.query(DimensionInteraction).filter(and_(DimensionInteraction.max_value >= value, DimensionInteraction.min_value <= value)).first()

    @staticmethod
    def get_views_group(value):
        return session.query(DimensionView).filter(and_(DimensionView.max_value >= value, DimensionView.min_value <= value)).first()

    def submit(self):
        assert session.query(FactVideo).filter(FactVideo.video_id == self._get_video().video_id,
                                               FactVideo.trending_date == self._get_video().trending_date,
                                               FactVideo.trending_location == self._get_video().trending_location) \
               is not None, "Vídeo já cadastrado."
        session.add(self._get_video())
        for tag in self.__tags:
            session.add(VideoTag(tag_id=tag.id, video_id=self._get_video().id))
        session.commit()
        video = self._get_video()
        self._clear()
        return video

    def set_video_id(self, video_id: str):
        self._get_video().video_id = video_id
        return self

    def set_trending_date(self, trending_date: str):
        if trending_date:
            trending_date_list = trending_date.split(".")
            self._get_video().trending_date = self._find_time_dimension(
                {
                    "year": trending_date_list[0],
                    "month": trending_date_list[2],
                    "day": trending_date_list[1]
                }
            ).id
        return self

    def set_title(self, title: str):
        self._get_video().title = title
        return self

    def set_views(self, views: int):
        self._get_video().views = views
        return self

    def set_channel_title(self, channel_title: str):
        self._get_video().channel_title = channel_title
        return self

    def set_publish_time(self, publish_time: str):
        publish_time = publish_time.split("-")
        self._get_video().publish_time = self._find_time_dimension(
            {
                "year": publish_time[0],
                "month": publish_time[1],
                "day": publish_time[2].split('T')[0]
            }
        ).id
        return self

    def set_view_group(self, views: int):
        view_group = self.get_views_group(views)
        if view_group:
            self._get_video().view_group_id = view_group.id
        return self

    def set_interaction_group(self, interation: float):
        interaction_dimension = self.get_interactions_group(interation)
        if interaction_dimension:
            self._get_video().interation_group_id = interaction_dimension.id
        return self

    def set_ratings_disabled(self, ratings_dis: bool):
        self._get_video().ratings_disabled = ratings_dis
        return self

    def set_video_error_or_removed(self, v_error_or_removed: bool):
        self._get_video().video_error_or_removed = v_error_or_removed
        return self

    def set_trending_location(self, location: str):
        self._get_video().trending_location = location
        return self

    def set_description(self, description: str):
        self._get_video().description = description
        return self

    def set_likes(self, likes: int):
        self._get_video().likes = likes
        return self

    def set_dislikes(self, dislikes: int):
        self._get_video().dislikes = dislikes
        return self

    def set_comment_count(self, comment_count: int):
        self._get_video().comment_count = comment_count
        return self

    def set_interactions_points(self, interactions_points: int):
        self._get_video().interactions_points = interactions_points
        return self

    def set_category(self, category_id: int):
        category = session.query(Category).filter(Category.category_id == category_id).first()
        if category is None:
            category = Category(category_id=category_id)
            session.add(category)
            session.commit()
        self._get_video().category_id = category.id
        return self

    def add_tags(self, tags: list):
        # already_created = [tag.name for tag in session.query(Tag).all()]
        # for tag in list(set(tags) - set(already_created)):
        #     tag_obj = Tag(name=tag)
        #     session.add(tag_obj)
        #     self.__tags.add(tag_obj)
        # for tag in already_created:
        #     self.__tags.add(session.query(Tag).filter(Tag.name == tag).first())
        # session.commit()
        return self

    def _get_video(self):
        """
        :return: FactVideo
        """
        if self.__video is None:
            self.__video = FactVideo()
        return self.__video

    def _find_time_dimension(self, time: dict):
        """
        :param time:
        :return: DimensionTime
        """
        time_dimension = session.query(DimensionTime).filter(
            DimensionTime.day == time["day"],
            DimensionTime.month == time["month"],
            DimensionTime.year == time["year"]).first()

        if time_dimension is None:
            weekday = Weekdays.get_weekday(datetime.date(
                day=int(time["day"]), month=int(time["month"]), year=int(time["year"])
            ).weekday())
            time_dimension = DimensionTime(
                day=time["day"], month=time["month"],
                year=time["year"], weekday=weekday
            )
            session.add(time_dimension)
            session.commit()
        return time_dimension

    def _clear(self):
        self.__video = None
        self.__tags = set()
