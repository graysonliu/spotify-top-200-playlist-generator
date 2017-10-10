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
    user_id = str(config['user_id'])
    playlist_id = config['playlist_id']
    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_uri = config['redirect_uri']
    chart_url = config['chart_url']

scope = 'playlist-modify-public'

token = util.prompt_for_user_token(user_id, scope, client_id, client_secret, redirect_uri)

r = requests.get(chart_url)
tracks = r.text.splitlines()[1:]

track_ids = []
for line in tracks:
    track_ids.append(line.rpartition('/')[2])

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    # You can add a maximum of 100 tracks per request.
    results1 = sp.user_playlist_replace_tracks(user_id, playlist_id, track_ids[:100])
    print(results1, time.strftime(ISO_TIME_FORMAT, time.localtime()))
    results2 = sp.user_playlist_add_tracks(user_id, playlist_id, track_ids[100:])
    print(results2, time.strftime(ISO_TIME_FORMAT, time.localtime()))

else:
    print("Can't get token for", user_id)
