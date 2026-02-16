import pytest
from pytest_mock import MockerFixture
import requests

from api.igdb import (
    IGDBAPI,
    AUTH_ENDPOINT_BASE,
    GAME_FIELDS,
    GENRE_FIELDS
)
from tests.test_constants import (
    TEST_CLIENT_ID, 
    TEST_CLIENT_SECRET, 
    TEST_GAMES_ID,
    TEST_GENRE_ID,
    MOCK_AUTH_PARAMS, 
    MOCK_AUTH_OK, 
    MOCK_AUTH_ERROR,
    MOCK_GAME,
    MOCK_GAMES_RESPONSE_EMPTY,
    MOCK_GAMES_RESPONSE_OK,
    MOCK_GENRE,
    MOCK_GENRE_RESPONSE_EMPTY,
    MOCK_GENRE_RESPONSE_OK
)


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
    return IGDBAPI(TEST_CLIENT_ID)

@pytest.fixture
def api_with_auth():
    api = IGDBAPI(TEST_CLIENT_ID)
    api._token = MOCK_AUTH_OK["access_token"]
    return api

class TestGetAuthQueryParams:
    def test_builds_parameters(
        self, 
        api: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocker.patch("requests.post")
        
        result = api._get_auth_query_params(TEST_CLIENT_SECRET)
        
        assert result == MOCK_AUTH_PARAMS

class TestRequestAuthToken:
    def test_posts_to_endpoint(
        self, 
        api: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_request = mocker.patch("requests.post")
        
        api.request_auth_token(TEST_CLIENT_SECRET)
        
        mocked_request.assert_called_once_with(
            api.endpoint, 
            data=MOCK_AUTH_PARAMS
        )
        
    def test_sets_token_if_200_status_code(
        self, 
        api: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_response = MockedResponse(200, MOCK_AUTH_OK)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        api.request_auth_token(TEST_CLIENT_SECRET)
        
        assert api._token == MOCK_AUTH_OK["access_token"]
        
    def test_raises_http_error_if_bad_status_code(
        self, 
        api: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_response = MockedResponse(403, MOCK_AUTH_ERROR)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        with pytest.raises(requests.HTTPError) as _:
            api.request_auth_token(TEST_CLIENT_SECRET)

class TestGetToken:
    def test_returns_token(self, api: IGDBAPI) -> None:
        api._token = MOCK_AUTH_OK["access_token"]
        
        assert api.get_token() == MOCK_AUTH_OK["access_token"]
        
class TestGetClientID:
    def test_returns_client_id(self, api: IGDBAPI) -> None:
        api._client_id = TEST_CLIENT_ID
        
        assert api.get_client_id() == TEST_CLIENT_ID
        
class TestGetRequestHeaders:
    def test_returns_dict_of_header_values(self, api: IGDBAPI) -> None:
        api._token = MOCK_AUTH_OK["access_token"]
        
        assert api.get_request_headers() == { 
            "Client-ID": api.get_client_id(), 
            "Authorization": f"Bearer {MOCK_AUTH_OK["access_token"]}"
        }

class TestGetGameByID:
    def test_posts_to_endpoint(
        self, 
        api_with_auth: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_request = mocker.patch("requests.post")
        
        api_with_auth.game_by_id(TEST_GAMES_ID)
        
        mocked_request.assert_called_once_with(
            f"{AUTH_ENDPOINT_BASE}/games", 
            data=f"fields {",".join(GAME_FIELDS)};where id = {TEST_GAMES_ID};",
            headers=api_with_auth.get_request_headers()
        )
    
    def test_throws_value_error_if_empty_list(
        self, 
        api_with_auth: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_response = MockedResponse(200, MOCK_GAMES_RESPONSE_EMPTY)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        with pytest.raises(ValueError):
            api_with_auth.game_by_id(TEST_GAMES_ID)
            
    def test_returns_one_game(
        self, 
        api_with_auth: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_response = MockedResponse(200, MOCK_GAMES_RESPONSE_OK)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        response = api_with_auth.game_by_id(TEST_GAMES_ID)
        
        assert response == MOCK_GAME
        
class TestGetGenreByID:
    def test_posts_to_endpoint(
        self, 
        api_with_auth: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_request = mocker.patch("requests.post")
        
        api_with_auth.genre_by_id(TEST_GENRE_ID)

        mocked_request.assert_called_once_with(
            f"{AUTH_ENDPOINT_BASE}/genres",
            data=f"fields {",".join(GENRE_FIELDS)};where id = {TEST_GENRE_ID};",
            headers=api_with_auth.get_request_headers()
        )
        
    def test_throws_value_error_if_empty_list(
        self, 
        api_with_auth: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_response = MockedResponse(200, MOCK_GENRE_RESPONSE_EMPTY)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        with pytest.raises(ValueError):
            api_with_auth.game_by_id(TEST_GENRE_ID)
    
    def test_returns_one_genre(
        self, 
        api_with_auth: IGDBAPI, 
        mocker: MockerFixture
    ) -> None:
        mocked_response = MockedResponse(200, MOCK_GENRE_RESPONSE_OK)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        response = api_with_auth.game_by_id(TEST_GENRE_ID)
        
        assert response == MOCK_GENRE