import spotipy
import spotipy.util as util
import requests
import time
import yaml

ISO_TIME_FORMAT = '%Y-%m-%d %X'

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

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    for region, info in generator.items():
        playlist_id = str(info).partition('||')[0].strip()
        chart_url = str(info).partition('||')[2].strip()

        r = requests.get(chart_url)
        tracks = r.text.splitlines()[1:]
        track_ids = []
        for line in tracks:
            track_ids.append(line.rpartition('/')[2])

        # You can add a maximum of 100 tracks per request.
        results1 = sp.user_playlist_replace_tracks(user_id, playlist_id, track_ids[:100])
        print(region, results1, time.strftime(ISO_TIME_FORMAT, time.localtime()))
        results2 = sp.user_playlist_add_tracks(user_id, playlist_id, track_ids[100:])
        print(region, results2, time.strftime(ISO_TIME_FORMAT, time.localtime()))

else:
    print("Can't get token for", user_id)
