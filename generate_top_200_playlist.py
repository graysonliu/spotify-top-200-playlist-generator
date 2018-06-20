import spotipy
import spotipy.util as util
import requests
import time
import yaml
import sys
import os

ISO_TIME_FORMAT = '%Y-%m-%d %X'
project_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(project_dir)

try:
    config_file = open('config.bak.yml', 'r')
except FileNotFoundError as e:
    config_file = open('config.yml', 'r')
finally:
    config = yaml.load(config_file)
    user_id = str(config['user_id']).strip()
    client_id = str(config['client_id']).strip()
    client_secret = str(config['client_secret']).strip()
    redirect_uri = str(config['redirect_uri']).strip()
    generator = config['generator']

scope = 'playlist-modify-public'

token = util.prompt_for_user_token(user_id, scope, client_id, client_secret, redirect_uri)


def get_chart_url(region_code):
    return 'https://spotifycharts.com/regional/' + region_code + '/daily/latest/download'


if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    for (region, playlist_id) in generator.items():
        playlist_id = str(playlist_id).strip()
        chart_url = get_chart_url(region)

        r = requests.get(chart_url)
        lines = r.text.splitlines()
        track_ids = []
        for line in lines:
            if line[0].isdigit:
                track_ids.append(line.rpartition('/')[2])

        # You can add a maximum of 100 tracks per request.
        results1 = sp.user_playlist_replace_tracks(user_id, playlist_id, track_ids[:100])
        print(region, results1, time.strftime(ISO_TIME_FORMAT, time.localtime()))
        results2 = sp.user_playlist_add_tracks(user_id, playlist_id, track_ids[100:])
        print(region, results2, time.strftime(ISO_TIME_FORMAT, time.localtime()))

else:
    print("Can't get token for", user_id)
