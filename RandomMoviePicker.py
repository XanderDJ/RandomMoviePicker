import os
import re
import random
import sys


def get_files_that_end_with(path, end_string):
    dot = re.compile("\.")
    executed_path = os.listdir(path)
    lst = []

    for file in executed_path:
        if file.endswith(end_string):
            lst.append(file)
        elif not dot.findall(file):
            lst.extend([file + "/" + vid for vid in get_files_that_end_with(path + "/" + file, end_string)])
    return lst


def start_random_video():
    videos = get_files_that_end_with(os.getcwd(), ".mp4")
    tags = []
    filteredvideos = []
    if len(sys.argv) > 1:
        for x in range(1, len(sys.argv)):
            tag = sys.argv[x]
            tags.append(tag)
            f = lambda vid: tag in vid
            filteredvideos.extend(list(filter(f, videos)))

    videos = filteredvideos if (len(sys.argv) > 1) else videos
    length = len(videos)
    random_vid = videos[random.randint(0, length - 1)]
    os.startfile(os.getcwd() + "/" + random_vid)


start_random_video()
