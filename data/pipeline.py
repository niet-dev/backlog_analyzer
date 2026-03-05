import logging
import os

import pandas as pd
from sqlmodel import (
    create_engine,
    Session,
    SQLModel
)

from data import api, cache, dataframes


logger = logging.getLogger(__name__)

def process_df(export_df: pd.DataFrame):
    logger.info(f"{len(export_df)} games read from csv.")
    
    sqlite_url = f"sqlite:///{os.getenv("SQLITE_FILE_NAME")}"
    engine = create_engine(sqlite_url)
    SQLModel.metadata.create_all(engine)

    token = api.fetch_auth_token()

    with Session(engine) as session:
        for game_id in export_df["IGDB ID"].to_list():
            cache.process_game(game_id, token, session)
    
    formatted_df = dataframes.format_export_df(export_df)
    merged_df = dataframes.merge_columns(formatted_df, engine)
    return merged_df
