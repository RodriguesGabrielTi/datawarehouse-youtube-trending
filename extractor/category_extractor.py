import config
from database.connection import session

import pandas as pd

from domain.models import Category


class CategoryExtractor:
    @classmethod
    def extract(cls, json):
        json = pd.read_json(config.jsons_dir + "/" + json)
        for item in json.get("items"):
            category_id = item.get("id")
            name = item.get("snippet").get("title")
            if session.query(Category).filter(Category.category_id == category_id).first() is None:
                session.add(Category(category_id=category_id, name=name))
        session.commit()

