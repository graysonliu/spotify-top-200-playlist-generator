import spotipy
import spotipy.util as util
import requests
import time
import yaml
import sys
import os
from lxml import html

ISO_TIME_FORMAT = '%Y-%m-%d %X'
project_dir = os.path.split(os.path.realpath(sys.argv[0]))[0]
os.chdir(project_dir)

try:
    config_file = open('config.bak.yml', 'r')
except FileNotFoundError as e:
    config_file = open('config.yml', 'r')
finally:
    config = yaml.safe_load(config_file)
    user_id = str(config['user_id']).strip()
    client_id = str(config['client_id']).strip()
    client_secret = str(config['client_secret']).strip()
    redirect_uri = str(config['redirect_uri']).strip()
    generator = config['generator']

scope = 'playlist-modify-public'

token = util.prompt_for_user_token(user_id, scope, client_id, client_secret, redirect_uri)


def get_chart_page(region_code):
    return 'https://spotifycharts.com/regional/' + region_code + '/daily/latest'


if token:
    sp = spotipy.Spotify(auth=token)
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
            sp.user_playlist_change_details(user_id, playlist_id,
                                            name='{country} Top 200 Daily'.format(country=country),
                                            description='Date: {date}| \
                                            Based on data from spotifycharts.com| \
                                            Powered by spotify-top-200-playlist-generator@GitHub'.format(date=date))

            sp.user_playlist_replace_tracks(user_id, playlist_id, [])
            # You can add a maximum of 100 tracks per request.
            results1 = sp.user_playlist_add_tracks(user_id, playlist_id, track_ids[:100])
            print(region, results1, time.strftime(ISO_TIME_FORMAT, time.localtime()))
            results2 = sp.user_playlist_add_tracks(user_id, playlist_id, track_ids[100:])
            print(region, results2, time.strftime(ISO_TIME_FORMAT, time.localtime()))

else:
    print("Can't get token for", user_id)
