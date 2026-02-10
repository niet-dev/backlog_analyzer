from typing import NewType

from pydantic import BaseModel


class IGDBGame(BaseModel):
    id: int
    first_release_date: int
    franchises: list[int]
    game_modes: list[int]
    genres: list[int]
    involved_companies: list[int]
    keywords: list[int]
    name: str
    platforms: list[int]
    player_perspectives: list[int]
    tags: list[int]
    themes: list[int]

IGDBGamesResponse = NewType("IGDBGamesResponse", list[IGDBGame])