import requests


AUTH_ENDPOINT_BASE = "https://id.twitch.tv/oauth2/token"

class IGDBAPI:
    endpoint: str
    _client_id: str
    _token: str
    
    def __init__(self, client_id):
        self.endpoint = AUTH_ENDPOINT_BASE
        self._client_id = client_id
    
    def request_auth_token(self, client_secret):
        query_params = self._get_auth_query_params(client_secret)
        
        response = requests.post(AUTH_ENDPOINT_BASE, data=query_params)
        response.raise_for_status()
        
        self._token = response.json()["access_token"]
        
    def get_token(self):
        return self._token
    
    def _get_auth_query_params(self, client_secret):
        return {
            "client_id": self._client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
