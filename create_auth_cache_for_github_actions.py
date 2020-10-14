import os

# for github actions, create .cache file from the secret, which is set to the environment variable SPOTIPY_AUTH_CACHE
auth_cache = os.getenv('SPOTIPY_AUTH_CACHE')
print(auth_cache)
if auth_cache:
    with open('.cache', 'w') as f:
        f.write(auth_cache)
