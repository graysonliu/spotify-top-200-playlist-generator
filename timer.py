import threading
import os
import sys

project_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(project_dir)

def update_playlist_daily():
    os.popen('python generate_top_200_playlist.py >> out')
    timer = threading.Timer(60 * 60 * 24, update_playlist_daily)
    timer.start()


update_playlist_daily()
