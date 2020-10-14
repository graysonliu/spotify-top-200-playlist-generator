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

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

ISO_TIME_FORMAT = '%Y-%m-%d %X'

with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)
    user_id = str(config['user_id']).strip()
    # client_id = str(config['client_id']).strip()
    # client_secret = str(config['client_secret']).strip()
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
    if r.status_code == 200:
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
