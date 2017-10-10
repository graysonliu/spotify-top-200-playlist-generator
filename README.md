# spotify-top-200-playlist-generator
Generate Spotify Global Top 200 Daily playlist.

Powered by [Spotipy](https://github.com/plamere/spotipy). Playlist data from [Spotify Charts](https://spotifycharts.com).

### How to Use

Replace stuff with your own info in the code below.

```python
# replace with your own user id
username = 'your-spotify-user-id'

# replace with your own stuff
token = util.prompt_for_user_token(username, scope, client_id='your-app-client-id', client_secret='your-app-client-secret', redirect_uri='your-app-redirect-url')

# replace with your own playlist id
playlist_id = 'your-spotify-playlist-id'
```

 **Where to get user-id and playlist-id?**

Click `Copy Spotify URI` and you will get text like this:

> spotify:user:12135742379:playlist:6F61J2pfnBeVZkXfumFQIi

For this case, user-id is `12135742379` and playlist-id is `6F61J2pfnBeVZkXfumFQIi`.
![](https://github.com/GraysonLiu/spotify-top-200-playlist-generator/blob/master/get-user-id-and-playlist-id.png)

**Where to get client-id, client-secret and redirect-uri?**

Go [here](https://developer.spotify.com/my-applications) to create your own Spotify application and get all these stuff.



Then, you can run the script. During the runtime, you need to authorize your Spotify account for your Spotify application if you have never done this before. Follow the [instruction](http://spotipy.readthedocs.io/en/latest/#authorized-requests) to get authorized. The credentials will be cached in local file `.cache-*` which can be used to automatically re-authorize expired tokens, so you won't need to go through this procedure next time.

The data source is [Spotify Charts](https://spotifycharts.com). I use the global chart by default, but you can change it if you want. For example, if you want to use USA chart, change

```python
r = requests.get('https://spotifycharts.com/regional/global/daily/latest/download')
```

to

```python
r = requests.get('https://spotifycharts.com/regional/us/daily/latest/download')
```

