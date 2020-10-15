![](https://github.com/graysonliu/spotify-top-200-playlist-generator/workflows/scheduled%20task/badge.svg)

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

![](https://github.com/graysonliu/spotify-top-200-playlist-generator/blob/master/images/get_user_id_and_playlist_id.png)

**Where to get client_id, client_secret and redirect_uri?**

Go [here](https://developer.spotify.com/my-applications) to create your own Spotify application and you will be given a Client ID and a Client Secret. Then, you can edit your redirect URL in app settings. We recommend using `http://localhost:{PORT_NUMBER}` as your redirect URL since this will let your spotify app automatically open the browser and authenticate the app if you have logged in your Spotify account in the same browser.

**Scheduled daily update with Github Actions.**

Here is the [workflow](https://github.com/graysonliu/spotify-top-200-playlist-generator/blob/master/.github/workflows/python.yml) that can help you update your Top 200 playlists daily automatically. Sensitive information like client id and client secret should not be exposed. Therefore, we add them as secrets at Github, and set them as environment variables in the workflow. Also, since Github Actions works in a headless environment, it is impossible to use a browser for authentication. Our strategy is, we first authenticate the app locally, which will give us a `.cache` file that saves tokens. We create secret `AUTH_CACHE` that saves the content of `.cache` at Github and also set it as a environment variable in the runtime. In Python script, we fetch this environment variable and create a `.cache` file using this secret. This newly created `.cache` file by Python will be used for authentication.

Another thing is, tokens in `.cache` could be refreshed in the runtime. If we do not update `AUTH_CACHE` to keep up with the content of `.cache`, tokens saved in `AUTH_CACHE` could be expired. Therefore, after the playlists are updated, we have to write the content of `.cache` back to secret `AUTH_CACHE`. To write secrets of a Github repo, we need a token with specific scopes of permissions. First, we create a personal access token named `TOKEN_WRITE_SECRETS` with scopes as follows:

![](https://github.com/graysonliu/spotify-top-200-playlist-generator/blob/master/images/create_personal_access_token.png)

Copy the generated token, and add it to secrets. We also name this secret `TOKEN_WRITE_SECRETS`.

In total, we should have four secrets:

![](https://github.com/graysonliu/spotify-top-200-playlist-generator/blob/master/images/secrets.png)

