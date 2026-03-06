from dataclasses import dataclass

import pandas as pd
from sqlmodel import select
from sqlalchemy import Engine

from data.models import (
    Game, 
    Franchise,
    GameFranchiseLink,
    GameMode,
    GameGameModeLink,
    Genre,
    GameGenreLink,
    Keyword,
    GameKeywordLink,
    Platform,
    GamePlatformLink,
    PlayerPerspective,
    GamePlayerPerspectiveLink, 
    Theme,
    GameThemeLink
)

SOURCE_COLUMNS = [
    "IGDB ID",
    "Status",
    "Completion",
    "Playtime",
    "Rating (Score)",
    "Tags",
]
TARGET_COLUMNS = [
    "id",
    "status",
    "completion",
    "playtime",
    "rating",
    "tags",
]
RENAME_CONFIG = dict(zip(SOURCE_COLUMNS, TARGET_COLUMNS))

@dataclass
class MergeConfig:
    model: type
    link_model: type
    link_index_col: str
    game_col_name: str
    
    index_col: str = "id"
    game_id_col: str = "game_id"
    model_name_col: str = "name"

MERGE_CONFIGS: list[MergeConfig] = [
    MergeConfig(
        model=Franchise,
        link_model=GameFranchiseLink,
        link_index_col="franchise_id",
        game_col_name="franchises"
    ),
    MergeConfig(
        model=GameMode,
        link_model=GameGameModeLink,
        link_index_col="game_mode_id",
        game_col_name="game_modes"
    ),
    MergeConfig(
        model=Genre, 
        link_model=GameGenreLink,
        link_index_col="genre_id",
        game_col_name="genres"
    ),
    MergeConfig(
        model=Keyword,
        link_model=GameKeywordLink,
        link_index_col="keyword_id",
        game_col_name="keywords"
    ),
    MergeConfig(
        model=Platform,
        link_model=GamePlatformLink,
        link_index_col="platform_id",
        game_col_name="platforms"  
    ),
    MergeConfig(
        model=PlayerPerspective,
        link_model=GamePlayerPerspectiveLink,
        link_index_col="player_perspective_id",
        game_col_name="player_perspectives"  
    ),
    MergeConfig(
        model=Theme,
        link_model=GameThemeLink,
        link_index_col="theme_id",
        game_col_name="themes"
    )
]

def format_export_df(export_df: pd.DataFrame) -> pd.DataFrame:
    return (
        export_df
            .rename(columns=RENAME_CONFIG)
            [TARGET_COLUMNS]
    )

def merge_columns(export_df: pd.DataFrame, engine: Engine) -> pd.DataFrame:
    df_games = pd.read_sql(select(Game), engine)

    for config in MERGE_CONFIGS:
        df_table = pd.read_sql(select(config.model), engine)
        df_link = pd.read_sql(select(config.link_model), engine)
        df_combined = (
            df_link
                .merge(
                    df_table, 
                    left_on=config.link_index_col, 
                    right_on=config.index_col
                )
                .groupby(config.game_id_col)
                .agg({config.model_name_col: list})
                .rename(columns={config.model_name_col: config.game_col_name})
        )
        df_games = df_games.merge(
            df_combined, 
            left_on=config.index_col, 
            right_on=config.game_id_col
        )
    
    merged_df = (
        export_df
            .merge(
                df_games,
                left_on="id",
                right_on="id"
            )
    )
    return merged_df

def validate_columns(df: pd.DataFrame, columns: list[str]):
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing required columns: {missing}")

def playtime_minutes_to_hours(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df, ["playtime"])
    
    modified_df = df.copy()
    modified_df["playtime"] = (modified_df["playtime"] / 60).round(1)
    
    print(modified_df["playtime"])
    
    return modified_df

def drop_games_with_no_playtime(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df, ["playtime"])
    
    modified_df = df.copy()
    
    modified_df = modified_df[
        modified_df["playtime"] > 0
    ]
    
    return modified_df
