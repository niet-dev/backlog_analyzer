import os
from typing import Final

import requests

from .models import APIGame

AUTH_ENDPOINT_BASE: Final[str] = "https://id.twitch.tv/oauth2/token"
API_ENDPOINT_BASE: Final[str] = "https://api.igdb.com/v4"
GAME_FIELDS: Final[list[str]] = [
    "id",
    "franchises",
    "game_modes",
    "genres",
    "keywords",
    "name",
    "platforms",
    "player_perspectives",
    "themes"
]
FOREIGN_KEY_FIELDS: Final[list[str]] = [
    "id",
    "name"
]

def fetch_auth_token():
    query_params = get_auth_query_params()
    response = requests.post(AUTH_ENDPOINT_BASE, data=query_params)
    response.raise_for_status()
    
    return response.json()["access_token"]

def get_auth_query_params():
    return {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "client_credentials"
    }
    
def get_request_headers(token: str):
    return {
        "Client-ID": os.getenv("CLIENT_ID"),
        "Authorization": f"Bearer {token}"
    }
    
def fetch_game_by_id(game_id: int, token: str) -> APIGame:
    joined_fields = ",".join(GAME_FIELDS)
    request_data = f"fields {joined_fields}; where id = {game_id};"
    
    response = requests.post(
        f"{API_ENDPOINT_BASE}/games",
        data=request_data,
        headers=get_request_headers(token)
    )
    response_data: list[APIGame] = response.json()
    game = APIGame.model_validate(response_data[0])
    return game

def fetch_foreign_key_object(object_id: int, endpoint: str, token: str):
    joined_fields = ",".join(FOREIGN_KEY_FIELDS)
    request_data = f"fields {joined_fields}; where id = {object_id};"
    
    response = requests.post(
        f"{API_ENDPOINT_BASE}/{endpoint}",
        data=request_data,
        headers=get_request_headers(token)
    )
    
    return response.json()[0]
