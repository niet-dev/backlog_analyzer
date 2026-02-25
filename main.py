import logging
import os

from dotenv import load_dotenv
import pandas as pd
from sqlmodel import (
    create_engine,
    Session,
    SQLModel
)

from data.api import fetch_auth_token
from data.cache import process_game

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    df = pd.read_csv("data.csv")
    logger.info(f"{len(df)} games read from csv.")
    
    sqlite_url = f"sqlite:///{os.getenv("SQLITE_FILE_NAME")}"
    engine = create_engine(sqlite_url)
    SQLModel.metadata.create_all(engine)

    token = fetch_auth_token()

    with Session(engine) as session:
        for game_id in df["IGDB ID"].to_list():
            process_game(game_id, token, session)
            
if __name__ == "__main__":
    main()
