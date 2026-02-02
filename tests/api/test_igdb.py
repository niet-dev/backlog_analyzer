import pytest
from pytest_mock import MockerFixture
import requests

from api import igdb

TEST_CLIENT_ID = "id"
TEST_CLIENT_SECRET = "secret"
MOCK_AUTH_RESPONSE = {
  "access_token": "access12345token",
  "expires_in": 5587808,
  "token_type": "bearer"
}
MOCK_AUTH_PARAMS = {
    "client_id": TEST_CLIENT_ID,
    "client_secret": TEST_CLIENT_SECRET,
    "grant_type": "client_credentials"
}
MOCK_AUTH_ERROR = {
    "status": 403,
    "message": "invalid client secret"
}

class MockedResponse:
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data
        
    def json(self):
        return self.data
    
    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError

class TestGetAuthQueryParams:
    def test_builds_parameters(self):
        result = igdb._get_auth_query_params(TEST_CLIENT_ID, TEST_CLIENT_SECRET)
        
        assert result == MOCK_AUTH_PARAMS

class TestGetAuthToken:
    def test_posts_to_endpoint(self, mocker: MockerFixture):
        mocked_request = mocker.patch("requests.post")
        
        igdb.get_auth_token(TEST_CLIENT_ID, TEST_CLIENT_SECRET)
        
        mocked_request.assert_called_once_with(igdb.AUTH_ENDPOINT_BASE, data=MOCK_AUTH_PARAMS)
        
    def test_returns_token_if_200_status_code(self, mocker: MockerFixture):
        mocked_response = MockedResponse(200, MOCK_AUTH_RESPONSE)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        token = igdb.get_auth_token(TEST_CLIENT_ID, TEST_CLIENT_SECRET)
        
        assert token == MOCK_AUTH_RESPONSE["access_token"]
        
    def test_raises_http_error_if_bad_status_code(
        self, mocker: MockerFixture):
        mocked_response = MockedResponse(403, MOCK_AUTH_ERROR)
        mocked_request = mocker.patch("requests.post")
        mocked_request.return_value = mocked_response
        
        with pytest.raises(requests.HTTPError) as _:
            igdb.get_auth_token(TEST_CLIENT_ID, TEST_CLIENT_SECRET)
