from math import ceil

import pandas as pd

import config
from database.connection import session


class DimensionInteraction:
    def __init__(self):
        self._session = session
        self._percentages = [0.1, 0.3, 0.6, 0.8, 1]

    def execute(self):
        dimensions_by_percentage_position = {}
        df = pd.read_csv(f"{config.files_dir}/interactions-count.csv", names=["vide_id", "interaction_result"])
        interactions_orderly = pd.unique(df["interaction_result"].sort_values())

        next_value = None
        for percentage in self._percentages:
            max_value_position = ceil(interactions_orderly.size * percentage) - 1
            max_value = interactions_orderly[max_value_position]
            min_value = next_value if next_value else interactions_orderly[0]
            dimensions_by_percentage_position.update({
                percentage: {
                    'min_value': min_value,
                    'max_value': max_value,
                }
            })
            try:
                next_value = interactions_orderly[max_value_position + 1]
            except IndexError:
                next_value = None
        print(dimensions_by_percentage_position)

if __name__ == '__main__':
    DimensionInteraction().execute()