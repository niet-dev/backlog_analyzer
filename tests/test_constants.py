from typing import Final

from data.igdb import IGDBGame, IGDBGenre

TEST_CLIENT_ID: Final[str] = "id"
TEST_CLIENT_SECRET: Final[str] = "secret"

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

_MOCK_GAME_DATA: Final[dict] = {
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
TEST_GAMES_ID: Final[int] = _MOCK_GAME_DATA["id"]
MOCK_GAME: IGDBGame = IGDBGame(**_MOCK_GAME_DATA)
MOCK_GAMES_RESPONSE_EMPTY: Final[list[IGDBGame]] = []
MOCK_GAMES_RESPONSE_OK: Final[list[IGDBGame]] = [MOCK_GAME, MOCK_GAME]

_MOCK_GENRE_DATA = {
    "id": 2,
    "name": "Point-and-click"
}
TEST_GENRE_ID: Final[int] = _MOCK_GENRE_DATA["id"]
MOCK_GENRE: IGDBGenre = IGDBGenre(**_MOCK_GENRE_DATA)
MOCK_GENRE_RESPONSE_EMPTY: Final[list[IGDBGenre]] = []
MOCK_GENRE_RESPONSE_OK: Final[list[IGDBGenre]] = [MOCK_GENRE, MOCK_GENRE]
