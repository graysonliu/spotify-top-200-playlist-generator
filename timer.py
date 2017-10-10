import threading
import os


def update_playlist_daily():
    os.popen('python generate_top_200_playlist.py >> out')
    timer = threading.Timer(60 * 60 * 24, update_playlist_daily)
    timer.start()


update_playlist_daily()
