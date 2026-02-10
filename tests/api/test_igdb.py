from typing import Final

import pytest
from pytest_mock import MockerFixture
import requests

from api import igdb
from data.igdb import IGDBGame

TEST_CLIENT_ID: Final[str] = "id"
TEST_CLIENT_SECRET: Final[str] = "secret"
TEST_GAMES_ID: Final[int] = 1234
MOCK_AUTH_OK: Final[dict] = {
  "access_token": "access12345token",
  "expires_in": 5587808,
  "token_type": "bearer"
}
MOCK_AUTH_ERROR: Final[dict] = {
    "status": 403,
    "message": "invalid client secret"
}
MOCK_AUTH_PARAMS: Final[dict] = {
    "client_id": TEST_CLIENT_ID,
    "client_secret": TEST_CLIENT_SECRET,
    "grant_type": "client_credentials"
}
_MOCK_GAME_DATA = {
    "id": 1234,
    "first_release_date": 1167177600,
    "franchises": [891],
    "game_modes": [1, 2],
    "genres": [4],
    "involved_companies": [228835],
    "keywords": [61, 182, 1231],
    "name": "Tekken 5: Dark Resurrection Online",
    "platforms": [9],
    "player_perspectives": [4],
    "tags": [1, 268435460],
    "themes": [1]
}
MOCK_GAME: IGDBGame = IGDBGame(**_MOCK_GAME_DATA)
MOCK_GAMES_RESPONSE_MULTIPLE = [MOCK_GAME, MOCK_GAME]
MOCK_GAMES_RESPONSE_SINGLE = [MOCK_GAME]
MOCK_GAMES_RESPONSE_EMPTY = []

class MockedResponse:
    def __init__(self, status_code: int, data):
        self.status_code = status_code
        self.data = data
        
    def json(self):
        return self.data
    
    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError

@pytest.fixture
def api():
    return igdb.IGDBAPI(TEST_CLIENT_ID)

@pytest.fixture
def api_with_auth():
    api = igdb.IGDBAPI(TEST_CLIENT_ID)
    api._token = MOCK_AUTH_OK["access_token"]
    return api

class TestGetAuthQueryParams:
    def test_builds_parameters(self, api, mocker: MockerFixture):
        mocker.patch("requests.post")
        
        result = api._get_auth_query_params(TEST_CLIENT_SECRET)
        
        assert result == MOCK_AUTH_PARAMS

class TestRequestAuthToken:
    def test_posts_to_endpoint(self, api, mocker: MockerFixture):
        mocked_request = mocker.patch("requests.post")
        
        api.request_auth_token(TEST_CLIENT_SECRET)
        
        mocked_request.assert_called_once_with(api.endpoint, data=MOCK_AUTH_PARAMS)
        
    def test_sets_token_if_200_status_code(self, api, mocker: MockerFixture):
        mocked_response = MockedResponse(200, MOCK_AUTH_OK)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        api.request_auth_token(TEST_CLIENT_SECRET)
        
        assert api._token == MOCK_AUTH_OK["access_token"]
        
    def test_raises_http_error_if_bad_status_code(
        self, api, mocker: MockerFixture):
        mocked_response = MockedResponse(403, MOCK_AUTH_ERROR)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        with pytest.raises(requests.HTTPError) as _:
            api.request_auth_token(TEST_CLIENT_SECRET)

class TestGetToken:
    def test_returns_token(self, api):
        api._token = MOCK_AUTH_OK["access_token"]
        
        assert api.get_token() == MOCK_AUTH_OK["access_token"]
        
class TestGetClientID:
    def test_returns_client_id(self, api):
        api._client_id = TEST_CLIENT_ID
        
        assert api.get_client_id() == TEST_CLIENT_ID
        
class TestGetRequestHeaders:
    def test_returns_dict_of_header_values(self, api):
        api._token = MOCK_AUTH_OK["access_token"]
        
        assert api.get_request_headers() == { 
            "Client-ID": api.get_client_id(), 
            "Authorization": f"Bearer {MOCK_AUTH_OK["access_token"]}"
        }

class TestGetGameByID:
    def test_posts_to_endpoint(self, api_with_auth, mocker: MockerFixture):
        mocked_request = mocker.patch("requests.post")
        
        api_with_auth.game_by_id(TEST_GAMES_ID)
        
        mocked_request.assert_called_once_with(
            f"{igdb.AUTH_ENDPOINT_BASE}/games", 
            data=f"fields {",".join(igdb.GAME_FIELDS)};where id = {TEST_GAMES_ID};",
            headers=api_with_auth.get_request_headers()
        )
    
    def test_throws_value_error_if_empty_list(
        self, 
        api_with_auth, 
        mocker: MockerFixture
    ):
        mocked_response = MockedResponse(200, MOCK_GAMES_RESPONSE_EMPTY)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        with pytest.raises(ValueError):
            api_with_auth.game_by_id(TEST_GAMES_ID)
            
    def test_returns_one_game(self, api_with_auth, mocker: MockerFixture):
        mocked_response = MockedResponse(200, MOCK_GAMES_RESPONSE_MULTIPLE)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        response = api_with_auth.game_by_id(TEST_GAMES_ID)
        
        assert response == MOCK_GAME