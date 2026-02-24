from dotenv import load_dotenv
import pandas as pd
from sqlmodel import (
    create_engine,
    Session,
    SQLModel
)

from .api import fetch_auth_token
from .cache import process_game

load_dotenv()


SQLITE_FILE_NAME = "database.db"

def main():
    df = pd.read_csv("data.csv")
    print(f"{len(df)} games read from csv.")
    
    sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"
    engine = create_engine(sqlite_url)
    SQLModel.metadata.create_all(engine)

    token = fetch_auth_token()

    with Session(engine) as session:
        for game_id in df["IGDB ID"].to_list():
            process_game(game_id, token, session)
            
if __name__ == "__main__":
    main()
