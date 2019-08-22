''' 
This script will segregate the videos made by OBS, into
proper folder having a hierarchy of Year, Month, Day.

It supports various formats, as supplied by arguments.
It doesn't search for videos in subfolder.
'''

import datetime
import argparse
import sys
import os
from os import listdir, system, stat
from os.path import isfile, join
from shutil import move

time_videos = {}
month_list = ['None', 'Jan', 'FEB', 'MAR', 'APR', 'MAY',
              'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def create_folders(path):
    # print(time_videos)
    for year, month_dict in time_videos.items():
        whole_year_path = join(path, str(year))
        print("Year --> " + whole_year_path)
        if not os.path.exists(whole_year_path):
            os.makedirs(whole_year_path)
            print("YEAR_CREATED")
        for month, videos in month_dict.items():
            whole_month_path = join(whole_year_path, month_list[month])
            print("Month -->" + whole_month_path)
            if not os.path.exists(whole_month_path):
                os.makedirs(whole_month_path)
                print("MONTH_CREATED")
            for video_path in videos:
                print(video_path)
                print(whole_month_path)
                move(video_path, whole_month_path)


def segregate_videos(path):
    for fle in listdir(path):
        whole_path = join(path, fle)
        if isfile(whole_path) and fle.endswith('.mp4'):
            print("Found a file : " + fle)
            create_time = stat(whole_path).st_ctime
            time_tuple = datetime.datetime.fromtimestamp(
                create_time).timetuple()
            year = time_tuple.tm_year
            month = time_tuple.tm_mon
            month_videos = time_videos.get(year, {})
            # print(month_videos)
            month_videos.setdefault(month, []).append(whole_path)
            time_videos[year] = month_videos
    # print(time_videos)


def main():
    '''
    Initialize two arguments:
        1. To define the classpath of the videos folder.
        2. To define the video formats.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("")
    args = parser.parse_args()
    for i in range(len(sys.argv)):
        print(sys.argv[i])

    # Assuming only one argument is there.
    path = sys.argv[1]
    segregate_videos(path)
    create_folders(path)


if __name__ == "__main__":
    main()
