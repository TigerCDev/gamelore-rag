import requests
from decouple import config
from datetime import datetime
from games.models import Game


def get_access_token():
    client_id = config('IGDB_CLIENT_ID')
    client_secret = config('IGDB_CLIENT_SECRET')
    url = 'https://id.twitch.tv/oauth2/token'
    response = requests.post(url, params={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
        })

    data = response.json()
    return data['access_token']


def get_game(game_name):
    token = get_access_token()
    client_id = config("IGDB_CLIENT_ID")
    url = 'https://api.igdb.com/v4/games'

    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
    }

    body = f'fields name,summary,first_release_date; search "{game_name}"; limit 1;'

    response = requests.post(url, headers=headers, data=body)
    return response.json()


def load_game(game_name):
    response = get_game(game_name)
    data = response[0]
    year = datetime.fromtimestamp(data['first_release_date']).year
    Game.objects.create(
        title=data['name'],
        release_year=year,
        synopsis=data['summary'],
    )
