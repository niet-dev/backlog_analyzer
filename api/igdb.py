import requests

AUTH_ENDPOINT_BASE = "https://id.twitch.tv/oauth2/token"


def get_auth_token(client_id, client_secret):
    query_params = _get_auth_query_params(client_id, client_secret)
    
    response = requests.post(AUTH_ENDPOINT_BASE, data=query_params)
    response.raise_for_status()
    
    return response.json()["access_token"]

def _get_auth_query_params(client_id, client_secret):
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
