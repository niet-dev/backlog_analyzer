import requests
from typing import Final

from data.igdb import (
    IGDBGame, 
    IGDBGamesResponse, 
    IGDBGenre, 
    IGDBGenresResponse
)

AUTH_ENDPOINT_BASE: Final[str] = "https://id.twitch.tv/oauth2/token"
GAME_FIELDS: Final[list[str]] = [
    "id",
    "first_release_date",
    "franchises",
    "game_modes",
    "genres",
    "involved_companies",
    "keywords",
    "name",
    "platforms",
    "player_perspectives",
    "tags",
    "themes"
]
GENRE_FIELDS: Final[list[str]] = [
    "id",
    "name"
]

class IGDBAPI:
    endpoint: str
    _client_id: str
    _token: str
    
    def __init__(self, client_id: str) -> None:
        self.endpoint = AUTH_ENDPOINT_BASE
        self._client_id = client_id
    
    def request_auth_token(self, client_secret: str) -> None:
        query_params = self._get_auth_query_params(client_secret)
        
        response = requests.post(AUTH_ENDPOINT_BASE, data=query_params)
        response.raise_for_status()
        
        self._token = response.json()["access_token"]
        
    def get_token(self) -> str:
        return self._token
    
    def get_client_id(self) -> str:
        return self._client_id
    
    def _get_auth_query_params(self, client_secret) -> dict:
        return {
            "client_id": self._client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }

    def get_request_headers(self) -> dict:
        return {
            "Client-ID": self.get_client_id(),
            "Authorization": f"Bearer {self.get_token()}"
        }
    
    def game_by_id(self, id: int) -> IGDBGame:
        request_data = f"fields {",".join(GAME_FIELDS)};where id = {id};"
        
        response = requests.post(
            f"{AUTH_ENDPOINT_BASE}/games",
            data=request_data,
            headers=self.get_request_headers()
        )
        response_data: IGDBGamesResponse = response.json()
        
        if not response_data: 
            raise ValueError(f"Could not find matching IGDB Games entry for ID {id}")
            
        return response_data[0]
    
    def genre_by_id(self, id: int) -> IGDBGenre:
        request_data = f"fields {",".join(GENRE_FIELDS)};where id = {id};"

        response = requests.post(
            f"{AUTH_ENDPOINT_BASE}/genres",
            data=request_data,
            headers=self.get_request_headers()
        )
        response_data: IGDBGenresResponse = response.json()
        
        if not response_data:
            raise ValueError(f"Could not find matching IGDB Genre entry for ID {id}")
        
        return response_data[0]