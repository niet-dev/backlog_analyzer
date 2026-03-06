import logging

from dotenv import load_dotenv
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns

import streamlit as st

from data import pipeline, plots


load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def display_chart(title: str, fig: Figure):
    st.write(f"# {title}")
    st.pyplot(fig)


uploaded_file = st.file_uploader("Upload your IB export .csv")
if uploaded_file is not None:
    df = pipeline.process_df(pd.read_csv(uploaded_file))
    
    sns.set_theme()
    
    for column in ["genres", "themes", "game_modes", "player_perspectives", "keywords"]:
        grouped_df = plots.avg_playtime(df, column)
        fig = plots.generate_chart(sns.barplot, grouped_df, x="playtime", y=column)
        display_chart(f"Average playtime by {column}", fig)
