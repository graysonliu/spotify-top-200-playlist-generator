import pprint
import spotipy
import spotipy.util as util
import requests

# replace with your own user id
username = 'your-spotify-user-id'
scope = 'playlist-modify-public'

# replace with your own staff
token = util.prompt_for_user_token(username, scope, client_id='your-app-client-id',
                                   client_secret='your-app-client-secret', redirect_uri='your-app-redirect-url')

# replace with your own playlist id
playlist_id = 'your-spotify-playlist-id'
track_ids = []

r = requests.get('https://spotifycharts.com/regional/global/daily/latest/download')
tracks = r.text.splitlines()[1:]
for line in tracks:
    track_ids.append(line.rpartition('/')[2])

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    # You can add a maximum of 100 tracks per request.
    results1 = sp.user_playlist_replace_tracks(username, playlist_id, track_ids[:100])
    pprint.pprint(results1)
    results2 = sp.user_playlist_add_tracks(username, playlist_id, track_ids[100:])
    print(results2)

else:
    print("Can't get token for", username)
