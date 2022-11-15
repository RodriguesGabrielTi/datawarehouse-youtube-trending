import datetime
from database.connection import session
from domain.models import FactVideo, DimensionTime, Weekdays, Category, DimensionView, DimensionInteraction


class VideoBuilder:
    groups = ["altissimo", "alto", "medio", "baixo","muito baixo"]
    interaction_constraint = [7, 5, 3, 1, -1]
    view_constraint = [10_000_000, 1_000_000, 100_000, 10_000, -1]

    def __init__(self):
        self.__video = None

    def submit(self):
        assert session.query(FactVideo).filter(FactVideo.video_id == self._get_video().video_id,
                                               FactVideo.trending_location == self._get_video().trending_location) \
               is not None, "Vídeo já cadastrado."
        session.add(self._get_video())
        session.commit()
        video = self._get_video()
        self._clear()
        return video

    def set_video_id(self, video_id: str):
        self._get_video().video_id = video_id
        return self

    def set_trending_date(self, trending_date: str):
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
        for i, group in enumerate(VideoBuilder.groups):
            if VideoBuilder.view_constraint[i] <= views:
                views_dimension = session.query(DimensionView).filter(
                    DimensionView.description == group
                ).first()
                if views_dimension is None:
                    views_dimension = DimensionView(description=group)
                    session.add(views_dimension)
                    session.commit()
                self._get_video().view_group = views_dimension.id
                break
        return self

    def set_interaction_group(self, interation: float):
        for i, group in enumerate(VideoBuilder.groups):
            if VideoBuilder.interaction_constraint[i] <= interation:
                interaction_dimension = session.query(DimensionInteraction).filter(
                    DimensionInteraction.description == group
                ).first()
                if interaction_dimension is None:
                    interaction_dimension = DimensionInteraction(description=group)
                    session.add(interaction_dimension)
                    session.commit()
                self._get_video().interation_group = interaction_dimension.id
                break
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

    def set_category(self, category_id: int):
        category = session.query(Category).filter(Category.category_id == category_id).first()
        if category is None:
            category = Category(category_id=category_id)
            session.add(category)
            session.commit()
        self._get_video().category_id = category.id
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
