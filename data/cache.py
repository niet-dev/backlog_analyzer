import logging
from typing import TypeVar

from sqlmodel import select, Session, SQLModel

from data.api import fetch_game_by_id, fetch_foreign_key_object
from data.models import (
    APIGame,
    Franchise,
    Game,
    GameMode,
    Genre,
    Keyword,
    Platform,
    PlayerPerspective,
    Theme
)

T = TypeVar("T", bound=SQLModel)

logger = logging.getLogger(__name__)


def process_game(game_id: int, token: str, session: Session) -> None:
    if game_is_cached(game_id, session):
        logger.info(f"Found cached Game {game_id}")
        return
    
    logger.info(f"Requesting data for Game {game_id}")
    
    data: APIGame = fetch_game_by_id(game_id, token)
    game = Game(id=data.id, name=data.name)
    session.add(game)
    
    entity_configs = [
        (Franchise, game.franchises, "franchises"),
        (GameMode, game.game_modes, "game_modes"),
        (Genre, game.genres, "genres"),
        (Keyword, game.keywords, "keywords"),
        (Platform, game.platforms, "platforms"),
        (PlayerPerspective, game.player_perspectives, "player_perspectives"),
        (Theme, game.themes, "themes")
    ]
    
    for model, relationship, endpoint in entity_configs:
        for id in getattr(data, endpoint):
            entity = get_or_fetch(model, id, endpoint, session, token)
            relationship.append(entity)
    
    session.commit()

def get_or_fetch(
    model: type[T], 
    id: int,
    endpoint: str,
    session: Session,
    token: str
    ) -> T:
    result = session.get(model, id)
    if result is None:
        logger.info(f"Requesting data for {model.__name__} {id}")
        data = fetch_foreign_key_object(id, endpoint, token)
        result = model.model_validate(data)
        session.add(result)
    else:
        logger.info(f"Found cached {model.__name__} {id}")
    return result


def game_is_cached(game_id: int, session: Session) -> bool:
    statement = select(Game).where(Game.id == game_id)
    results = session.exec(statement)
    
    return len(results.all()) > 0

def get_cached_game(game_id: int, session: Session) -> Game:
    statement = select(Game).where(Game.id == game_id)
    results = session.exec(statement)
    
    return results.one()
