import requests

from .config import cdek_settings


def get_cdek_token():
    response = requests.post(
        cdek_settings.API_TOKEN_URL, 
        data={'grant_type': 'client_credentials', 'client_id': cdek_settings.ACCOUNT, 'client_secret': cdek_settings.PASSWORD},
    )

    if response.status_code == 200:
        data = response.json()
        return data['access_token']