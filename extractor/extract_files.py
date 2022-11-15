import os
import config
from extractor.video_extractor import VideoExtractor

if __name__ == "__main__":
    # Add Categories

    # Add videos
    with os.scandir(config.files_dir) as entries:
        csv_files = [entry.name for entry in entries]

    for file in csv_files:
        VideoExtractor.extract(file, file[0:2])
