from math import ceil

import pandas as pd
from pandas import DataFrame
import numpy as np

from database.connection import session
from domain.models import FactVideo, DimensionView, DimensionInteraction
from utils.video_builder import VideoBuilder


class DimensionCalc:
    def __init__(self):
        self._session = session
        self._percentages = [0.021, 0.157, 0.843, 0.979, 1]

    def update_all_videos(self):
        videos = self._session.query(FactVideo).filter().all()
        for video in videos:
            views_group = VideoBuilder.get_views_group(video.views)
            if views_group:
                video.view_group_id = views_group.id
            interactions_group = VideoBuilder.get_interactions_group(video.interactions_points)
            if interactions_group:
                video.interation_group_id = interactions_group.id
        session.commit()

    def compute_videos_interactions(self):
        interactions_points = [row.interactions_points if row.interactions_points else 0 for row in self._session.query(FactVideo.interactions_points).filter()]
        df = pd.DataFrame({'values': interactions_points})
        dimensions = self.execute(df)
        if not dimensions:
            return
        ids = []
        next_min_percentage = 0
        for dimension_key in dimensions:
            interaction_dimension = DimensionInteraction()
            interaction_dimension.description = f"{str(next_min_percentage*100)}%-{str(dimension_key*100)}% de todos os valores"
            interaction_dimension.min_value = float(dimensions[dimension_key]["min_value"])
            interaction_dimension.max_value = float(dimensions[dimension_key]["max_value"])
            session.add(interaction_dimension)
            session.commit()
            ids.append(interaction_dimension.id)
            next_min_percentage = dimension_key
        self._session.query(DimensionInteraction).filter(DimensionInteraction.id.not_in(ids)).delete()
        self._session.commit()

    def compute_videos_views(self):
        views = [row.views if row.views else 0 for row in self._session.query(FactVideo.views).filter()]
        df = pd.DataFrame({'values': views})
        dimensions = self.execute(df)
        if not dimensions:
            return
        ids = []
        next_min_percentage = 0
        for dimension_key in dimensions:
            views_dimension = DimensionView()
            views_dimension.description = f"{str(next_min_percentage*100)}%-{str(dimension_key*100)}% de todos os valores"
            views_dimension.min_value = int(dimensions[dimension_key]["min_value"])
            views_dimension.max_value = int(dimensions[dimension_key]["max_value"])
            session.add(views_dimension)
            session.commit()
            ids.append(views_dimension.id)
            next_min_percentage = dimension_key
        self._session.query(DimensionView).filter(DimensionView.id.not_in(ids)).delete()
        self._session.commit()

    def execute(self, df: DataFrame):
        dimensions_by_percentage_position = {}
        if 'values' not in df.columns:
            raise ValueError("Dataframe needs values to compute")
        interactions_orderly = pd.array(df["values"].sort_values())
        if not interactions_orderly:
            return
        next_value = None
        for percentage in self._percentages:
            max_value_position = ceil(interactions_orderly.size * percentage) - 1
            max_value = interactions_orderly[max_value_position]
            min_value = next_value if next_value else 0
            dimensions_by_percentage_position.update({
                percentage: {
                    'min_value': min_value,
                    'max_value': max_value,
                }
            })
            try:
                next_value = np.nextafter(max_value, np.inf) if isinstance(max_value, np.float64) else max_value + 1
            except IndexError:
                next_value = None
        return dimensions_by_percentage_position


if __name__ == '__main__':
    print(DimensionCalc().compute_videos_interactions())
    #print(DimensionCalc().execute(pd.read_csv(f"{config.files_dir}/interactions-count.csv", names=["vide_id", "values"])))