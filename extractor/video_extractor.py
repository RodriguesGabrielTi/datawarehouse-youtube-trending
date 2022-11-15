import pandas as pd

import config

from utils.video_builder import VideoBuilder
"""
Extract file from one CSV
video_id
trending_date
title
channel_title
category_id
publish_time
tags
views
likes
dislikes
comment_count
thumbnail_link
comments_disabled
ratings_disabled
video_error_or_removed
description
"""


class VideoExtractor:
    @classmethod
    def extract(cls, csv, country):
        csv_file = pd.read_csv(config.files_dir + "/" + csv, encoding="utf-8")
        video_builder = VideoBuilder()
        for i, row in csv_file.iterrows():
            tags = row.get("tags").replace("\"", "").split("|")
            interactions = (row.get("likes") + row.get("dislikes") + 2 * row.get("comment_count")) / row.get("views")
            video_builder\
                .set_video_id(row.get("video_id"))\
                .set_trending_date(row.get("trending_date"))\
                .set_title(row.get("title"))\
                .set_channel_title(row.get("channel_title")) \
                .set_publish_time(row.get("publish_time")) \
                .set_view_group(int(row.get("views")))\
                .set_interaction_group(interactions)\
                .set_likes(int(row.get("likes")))\
                .set_dislikes(int(row.get("dislikes")))\
                .set_comment_count(int(row.get("comment_count")))\
                .set_ratings_disabled(bool(row.get("ratings_disabled")))\
                .set_video_error_or_removed(bool(row.get("video_error_or_removed")))\
                .set_description(row.get("description"))\
                .set_category(int(row.get("category_id")))\
                .set_trending_location(country)\
                .add_tags(tags)
            try:
                video_builder.submit()
            except AssertionError as e:
                print(e, "id:", row.get("video_id"))
