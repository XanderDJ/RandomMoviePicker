import ctypes
import os
import re
import sys
from BooleanTree import BooleanParser


def load_videos():
    try:
        storage = open("data.dat", 'r')
    except Exception:
        storage = open("data.dat", "w")
        storage.flush()
        storage.close()
        ctypes.windll.kernel32.SetFileAttributesW(os.getcwd() + "\\" + "data.dat", 2)
        storage = open("data.dat", "r")
    st = set()
    for line in storage:
        st.add(line.rstrip())
    storage.close()
    return st


def get_files_that_end_with(path, end_string):
    dot = re.compile("\.")
    executed_path = os.listdir(path)
    lst = set()

    for file in executed_path:
        if file.endswith(end_string):
            lst.add(file)
        elif os.path.isdir(os.path.join(path, file)):
            try:
                lst.update([file + "/" + vid for vid in get_files_that_end_with(path + "/" + file, end_string)])
            except WindowsError:
                pass
    return lst


def get_video_name(path_to_vid):
    split = path_to_vid.split("/")
    match = re.match(r"^(.*)\.mp4", split[-1])
    return match.group(1)


def watched_video(video):
    storage = open("data.dat", "a")
    storage.write(video + "\n")
    storage.flush()
    storage.close()


def process_args(argv):
    args = argv[1:]
    for arg in args:
        pass


def filter(vid):
    """
        Returns true if vid matches tags passed by argv
    :param vid: the video to check
    :return: boolean
    """

    return True


def start_random_video():
    videos_already_watched = load_videos()
    videos = get_files_that_end_with(os.getcwd(), ".mp4")
    tags = []
    filteredvideos = set()
    if len(sys.argv) > 1:
        parser = BooleanParser(sys.argv[1:])
        f = lambda vid: parser.get_boolean_value(vid[:len(vid) -4])
        filteredvideos.update(list(filter(f, videos)))

    videos = filteredvideos if (len(sys.argv) > 1) else videos
    videos_not_watched = videos - videos_already_watched
    length = len(videos_not_watched)

    if len(sys.argv) > 1 and len(videos) > 0:
        random_vid = videos.pop()
        vid_name = get_video_name(random_vid)
        print("You're now watching : \"" + vid_name[:len(vid_name) -4] + "\"")
        os.startfile(os.getcwd() + "/" + random_vid)

    elif len(videos_not_watched) > 0:
        random_vid = videos_not_watched.pop()
        vid_name = get_video_name(random_vid)
        print("You're now watching : \"" + vid_name[:len(vid_name) -4] + "\"")
        watched_video(random_vid)
        os.startfile(os.getcwd() + "/" + random_vid)

    elif len(videos) == 0:
        print("There were no videos with any of those tags or there were no videos in general")

    else:
        print("you've opened every video in the directories, flushing data and restarting")
        os.remove(os.getcwd() + "\\" + 'data.dat')
        start_random_video()


start_random_video()
