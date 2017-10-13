# spotify-top-200-playlist-generator
Generate Spotify top 200 playlist from [Spotify Charts](https://spotifycharts.com).

Powered by [Spotipy](https://github.com/plamere/spotipy). 

### How to Use

Fill config.yml with your own info:

```yaml
user_id: your-spotify-account-id
client_id: your-spotify-app-client-id
client_secret: your-spotify-app-client-secret
redirect_uri: your-spotify-app-redirect-uri
generator:
# region_code: playlist_id
  global: your-global-top-200-playlist-id
  us: your-us-top-200-playlist-id
```

 **Where to get user_id and playlist_id?**

Click `Copy Spotify URI` in the image below and you will get text like this:

> spotify:user:12135742379:playlist:6F61J2pfnBeVZkXfumFQIi

In this case, user_id is `12135742379` and playlist_id is `6F61J2pfnBeVZkXfumFQIi`.

![](https://github.com/GraysonLiu/spotify-top-200-playlist-generator/blob/master/get-user-id-and-playlist-id.png)

**Where to get client_id, client_secret and redirect_uri?**

Go [here](https://developer.spotify.com/my-applications) to create your own Spotify application and get all these stuff.

Then, you can run the script. During the runtime, you need to authorize your Spotify account for your Spotify application if you have never done this before. Follow the [instruction](http://spotipy.readthedocs.io/en/latest/#authorized-requests) to get authorized. The credentials will be cached in local file `.cache-*` which can be used to automatically re-authorize expired tokens, so you won't need to go through this procedure next time.

### Auto Update Playlist Daily

Run shell command on your server:

```shell
python timer.py &
```

The output is redirected to file `out`.