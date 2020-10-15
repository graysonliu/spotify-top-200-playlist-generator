import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import time
import yaml
import sys
import os
from lxml import html
from dotenv import load_dotenv

project_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(project_dir)

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# for github actions, create .cache file from the secret, which is set to the environment variable AUTH_CACHE
auth_cache = os.getenv('AUTH_CACHE')
if auth_cache:

    with open('.cache', 'w') as f:
        f.write(auth_cache)

    # update secret AUTH_CACHE in case that content in .cache is changed during runtime (e.g. token is refreshed)
    secret_name = 'AUTH_CACHE'
    # we need authentication to write secrets
    # default GITHUB_TOKEN does not have the permission to write secrets, we need to create a personal access token
    # we also need to set this personal access token as an environment variable
    token_write_secrets = os.getenv('TOKEN_WRITE_SECRETS')

    # these are default environment variables in Github Actions
    github_api_url = os.getenv('GITHUB_API_URL')
    github_repo = os.getenv('GITHUB_REPOSITORY')
    github_actor = os.getenv('GITHUB_ACTOR')

    # for authentication
    from requests.auth import HTTPBasicAuth

    auth = HTTPBasicAuth(github_actor, token_write_secrets)

    headers = {'Accept': 'application/vnd.github.v3+json'}
    # Get the public key to encrypt secrets
    # reference: https://docs.github.com/en/free-pro-team@latest/rest/reference/actions#get-a-repository-public-key
    r = requests.get(f'{github_api_url}/repos/{github_repo}/actions/secrets/public-key', headers=headers, auth=auth)
    public_key = r.json()['key']
    key_id = r.json()['key_id']

    # reference: https://docs.github.com/en/free-pro-team@latest/rest/reference/actions#create-or-update-a-repository-secret
    from base64 import b64encode
    from nacl import encoding, public


    def encrypt(public_key: str, secret_value: str) -> str:
        """Encrypt a Unicode string using the public key."""
        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")


    with open('.cache', 'r') as f:
        encrypted_value = encrypt(public_key, f.read())
        data = {'encrypted_value': encrypted_value, 'key_id': key_id}
        r = requests.put(f'{github_api_url}/repos/{github_repo}/actions/secrets/{secret_name}', headers=headers,
                         json=data, auth=auth)
        if r.ok:
            print(f'Secret {secret_name} updated.')

ISO_TIME_FORMAT = '%Y-%m-%d %X'

with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)
    user_id = str(config['user_id']).strip()
    redirect_uri = str(config['redirect_uri']).strip()
    generator = config['generator']

scope = 'playlist-modify-public'

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)


def get_chart_page(region_code):
    return 'https://spotifycharts.com/regional/' + region_code + '/daily/latest'


sp = spotipy.Spotify(auth_manager=auth_manager)
sp.trace = False
for (region, playlist_id) in generator.items():
    playlist_id = str(playlist_id).strip()
    chart_page = get_chart_page(region)

    r = requests.get(chart_page)
    if r.ok:
        tree = html.fromstring(r.content)
        selected_values = tree.xpath('//div[@class="responsive-select-value"]/text()')
        country = selected_values[0]
        recurrence = selected_values[1].capitalize()
        date = selected_values[2]

        track_urls = tree.xpath('//td[@class="chart-table-image"]/a/@href')
        track_ids = []
        for url in track_urls:
            track_ids.append(url.rpartition('/')[2])
        sp.playlist_change_details(playlist_id,
                                   name='{country} Top 200 Daily'.format(country=country),
                                   description=('Date: {date} | '
                                                'Based on data from spotifycharts.com | '
                                                'Powered by spotify-top-200-playlist-generator@GitHub')
                                   .format(date=date))

        sp.playlist_replace_items(playlist_id, [])
        # You can add a maximum of 100 tracks per request.
        results1 = sp.playlist_add_items(playlist_id, track_ids[:100])
        print(region, results1, time.strftime(ISO_TIME_FORMAT, time.localtime()))
        results2 = sp.playlist_add_items(playlist_id, track_ids[100:])
        print(region, results2, time.strftime(ISO_TIME_FORMAT, time.localtime()))
