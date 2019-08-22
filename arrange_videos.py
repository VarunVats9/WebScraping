"""
This script will segregate the videos made by OBS, into
proper folder having a hierarchy of Year, Month, Day.

It supports various formats, as supplied by arguments.
It doesn't search for videos in subfolder.
"""

from datetime import datetime
import argparse
import sys
import os
import pprint
from os import listdir, system, stat
from os.path import isfile, join, getctime
from shutil import move

month_list = ['None', 'Jan', 'FEB', 'MAR', 'APR', 'MAY',
              'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def create_folders(dst_path, year_videos):
    """ Creates heirarchial folder of Year, Month and put videos in that. 
        Arguments:
            :dst_path: Path where the folders have to be created.
            :year_videos: Map of (year, map(month, list of videos)).
    """
    pprint.pprint(year_videos)
    user_choice = input('Are you sure you want to move these videos to {} [y/n] : '.format(dst_path))
    if user_choice == 'y':   
        for year, month_dict in year_videos.items():
            absolute_year_path = join(dst_path, str(year))
            if not os.path.exists(absolute_year_path):
                os.makedirs(absolute_year_path)
            for month, day_dict in month_dict.items():
                absolute_month_path = join(absolute_year_path, month_list[month])
                if not os.path.exists(absolute_month_path):
                    os.makedirs(absolute_month_path)
                print(day_dict)
                for day, videos in day_dict.items():
                    absolute_day_path = join(absolute_month_path, str(day))
                    if not os.path.exists(absolute_day_path):
                        os.makedirs(absolute_day_path)
                    for video_path in videos:
                        move(video_path, absolute_day_path)
    else:
        print('Aborting the operation!!')


def segregate_videos(src_path, ext):
    """ Returns a map of (year, map(month, list of videos)). 
        Arguments:
            :src_path: Path where videos are stored.
            :ext: List of video extensions to be segregated.
    """
    year_videos = {}
    for fle in listdir(src_path):
        absolute_file_path = join(src_path, fle)
        if isfile(absolute_file_path) and fle.endswith(tuple(ext)):
            last_metadata_change = datetime.fromtimestamp(getctime(absolute_file_path))
            time_tuple = last_metadata_change.timetuple()
            year = time_tuple.tm_year
            month = time_tuple.tm_mon
            day = time_tuple.tm_mday
            month_videos = year_videos.get(year, {})
            day_videos = month_videos.get(month, {})
            day_videos.setdefault(day, []).append(absolute_file_path)
            month_videos[month] = day_videos
            year_videos[year] = month_videos
    return year_videos


def main():
    """
    Initialize two arguments:
        1. To define the classpath of the videos folder.
        2. To define the video formats.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", required=True,
                        help="Path where videos are stored.")
    parser.add_argument("-dst", required=True,
                        help="Path where folders should be created.")
    parser.add_argument("-ext", nargs='+', required=True,
                        help="Video extensions to arrange.")

    args = parser.parse_args()
    time_videos = segregate_videos(args.src, args.ext)
    create_folders(args.dst, time_videos)


if __name__ == "__main__":
    main()
