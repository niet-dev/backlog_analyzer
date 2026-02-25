from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

class APIGame(BaseModel):
    id: int
    franchises: list[int]
    game_modes: list[int]
    genres: list[int]
    keywords: list[int]
    name: str
    platforms: list[int]
    player_perspectives: list[int]
    themes: list[int]

class APIForeignKey(BaseModel):
    id: int
    name: str

class GameFranchiseLink(SQLModel, table=True):
    game_id: int = Field(foreign_key="game.id", primary_key=True)
    franchise_id: int = Field(foreign_key="franchise.id", primary_key=True)

class GameGameModeLink(SQLModel, table=True):
    game_id: int = Field(foreign_key="game.id", primary_key=True)
    game_mode_id: int = Field(foreign_key="game_mode.id", primary_key=True)

class GameGenreLink(SQLModel, table=True):
    game_id: int = Field(foreign_key="game.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)

class GameKeywordLink(SQLModel, table=True):
    game_id: int = Field(foreign_key="game.id", primary_key=True)
    keyword_id: int = Field(foreign_key="keyword.id", primary_key=True)

class GamePlatformLink(SQLModel, table=True):
    game_id: int = Field(foreign_key="game.id", primary_key=True)
    platform_id: int = Field(foreign_key="platform.id", primary_key=True)

class GamePlayerPerspectiveLink(SQLModel, table=True):
    game_id: int = Field(foreign_key="game.id", primary_key=True)
    player_perspective_id: int = Field(foreign_key="player_perspective.id", primary_key=True)
    
class GameThemeLink(SQLModel, table=True):
    game_id: int = Field(foreign_key="game.id", primary_key=True)
    theme_id: int = Field(foreign_key="theme.id", primary_key=True)


class Game(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    
    franchises: list["Franchise"] = Relationship(back_populates="games", link_model=GameFranchiseLink)
    game_modes: list["GameMode"] = Relationship(back_populates="games", link_model=GameGameModeLink)
    genres: list["Genre"] = Relationship(back_populates="games", link_model=GameGenreLink)
    keywords: list["Keyword"] = Relationship(back_populates="games", link_model=GameKeywordLink)
    platforms: list["Platform"] = Relationship(back_populates="games", link_model=GamePlatformLink)
    player_perspectives: list["PlayerPerspective"] = Relationship(back_populates="games", link_model=GamePlayerPerspectiveLink)
    themes: list["Theme"] = Relationship(back_populates="games", link_model=GameThemeLink)


class Franchise(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    
    games: list[Game] = Relationship(back_populates="franchises", link_model=GameFranchiseLink)

class GameMode(SQLModel, table=True):
    __tablename__ = "game_mode" # type: ignore
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    
    games: list[Game] = Relationship(back_populates="game_modes", link_model=GameGameModeLink)
    
class Genre(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    
    games: list[Game] = Relationship(back_populates="genres", link_model=GameGenreLink)

class Keyword(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    
    games: list[Game] = Relationship(back_populates="keywords", link_model=GameKeywordLink)

class Platform(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    
    games: list[Game] = Relationship(back_populates="platforms", link_model=GamePlatformLink)

class PlayerPerspective(SQLModel, table=True):
    __tablename__ = "player_perspective" # type: ignore
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    
    games: list[Game] = Relationship(back_populates="player_perspectives", link_model=GamePlayerPerspectiveLink)

class Theme(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    
    games: list[Game] = Relationship(back_populates="themes", link_model=GameThemeLink)
