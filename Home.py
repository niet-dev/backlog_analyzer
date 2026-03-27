import logging
import os

from dotenv import load_dotenv
import pandas as pd
from sqlmodel import (
    create_engine,
    Session,
    SQLModel
)
import streamlit as st

from data import api, cache, dataframes


load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="Backlog Analyzer"
)

st.write("# Backlog Analyzer")
st.sidebar.success("Select from the options above.")

uploaded_file = st.file_uploader("Upload your IB export .csv")
if uploaded_file is not None:
    export_df = pd.read_csv(uploaded_file)
    
    logger.info(f"{len(export_df)} games read from csv.")
    
    sqlite_url = f"sqlite:///{os.getenv("SQLITE_FILE_NAME")}"
    engine = create_engine(sqlite_url)
    SQLModel.metadata.create_all(engine)

    token = api.fetch_auth_token()
    
    progress = st.progress(0, text="Processing games...")
    total = len(export_df)
    
    with Session(engine) as session:
        for i, game_id in enumerate(export_df["IGDB ID"]):
            cache.process_game(game_id, token, session)
            progress.progress((i + 1) / total, text=f"Processing game {i + 1} of {total}")
    
    formatted_df = dataframes.format_export_df(export_df)
    merged_df = dataframes.merge_columns(formatted_df, engine)

    st.session_state["df"] = merged_df

