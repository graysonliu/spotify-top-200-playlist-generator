# spotify-top-200-playlist-generator
Generate Spotify top 200 playlist from [Spotify Charts](https://spotifycharts.com).

Powered by [Spotipy](https://github.com/plamere/spotipy). 

### How to Use

Fill `config.yml` with your own info:

```yaml
user_id: your-spotify-account-id
redirect_uri: your-spotify-app-redirect-uri
generator:
# region_code: playlist_id
  global: your-global-top-200-playlist-id
  us: your-us-top-200-playlist-id
```

Create `.env` and set environment variables:

```bash
CLIENT_ID=your-spotify-app-client-id
CLIENT_SECRET=your-spotify-app-client-secret
```

 **Where to get user_id and playlist_id?**

Click `Copy Spotify URI` in the image below and you will get text like this:

> spotify:user:12135742379:playlist:6F61J2pfnBeVZkXfumFQIi

In this case, user_id is `12135742379` and playlist_id is `6F61J2pfnBeVZkXfumFQIi`.

![](https://github.com/graysonliu/spotify-top-200-playlist-generator/blob/master/get-user-id-and-playlist-id.png)

**Where to get client_id, client_secret and redirect_uri?**

Go [here](https://developer.spotify.com/my-applications) to create your own Spotify application and you will be given a Client ID and a Client Secret. Then, you can edit your redirect URL in app settings. We recommend using 'http://localhost:[PORT_NUMBER]' as your redirect URL since this will let your spotify app automatically open the browser and authorize the app if you have logged in your Spotify account in the same browser.

**Scheduled update with Github Actions.**

Here is the [workflow](https://github.com/graysonliu/spotify-top-200-playlist-generator/blob/master/.github/workflows/python.yml) that can help you update your Top 200 playlists. Sensitive information like client id and client secret should not be exposed. Therefore, we add them as secrets at Github, and set them as environment variables in the workflow when executing the Python script. Also, since Github Actions works in a headless environment, it is impossible to use a browser for authorization. Our strategy is, we first authorize the app locally, which will give us a `.cache` file that saves tokens. We create a secret that saves the content of `.cache` at Github and also set it as a environment variable in the runtime. In Python script, we fetch this environment variable and create a `.cache` file using this secret. This newly created `.cache` file by Python will be used for authorization.

Created secrets:

![](https://github.com/graysonliu/spotify-top-200-playlist-generator/blob/master/secrets.png)

In Python script:

```python
# for github actions, create .cache file from the secret, which is set to the environment variable AUTH_CACHE
auth_cache = os.getenv('AUTH_CACHE')
if auth_cache:
    with open('.cache', 'w') as f:
        f.write(auth_cache)
```

In workflow:
```yaml
- name: Set environment variables with secrets and update playlists
  env:
    CLIENT_ID: ${{ secrets.CLIENT_ID }}
    CLIENT_SECRET: ${{ secrets.CLIENT_SECRET }}
    AUTH_CACHE: ${{ secrets.AUTH_CACHE }}
  run: python generate_top_200_playlist.py
```

