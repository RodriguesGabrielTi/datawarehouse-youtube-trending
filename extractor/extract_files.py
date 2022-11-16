import os
import config
from extractor.category_extractor import CategoryExtractor
from extractor.compute_dimensions import DimensionCalc
from extractor.video_extractor import VideoExtractor
import time


def execute_categories():
    start_categories = time.process_time()
    with os.scandir(config.jsons_dir) as entries:
        categories_jsons = [entry.name for entry in entries]

    for json in categories_jsons:
        CategoryExtractor.extract(json)
    end_categories = time.process_time()
    print("Process time to read the categories:", str(round(end_categories - start_categories, 3)))


def extract_videos():
    start_videos = time.process_time()
    with os.scandir(config.files_dir) as entries:
        csv_files = [entry.name for entry in entries]
    for file in csv_files:
        start_video = time.process_time()
        VideoExtractor.extract(file, file[0:2])
        end_video = time.process_time()
        print(f"Process time to read {file}:", str(round(end_video - start_video, 3)))
    end_videos = time.process_time()
    print("Process time to read all the CSVs:", str(round(end_videos - start_videos, 3)))


def compute_dimensions():
    calc = DimensionCalc()
    calc.compute_videos_views()
    calc.compute_videos_interactions()
    calc.update_all_videos()

if __name__ == "__main__":
    # Add categories
    execute_categories()
    # Add videos
    extract_videos()
    compute_dimensions()
