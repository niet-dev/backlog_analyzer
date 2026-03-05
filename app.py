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
    
    df_genre_playtime = plots.avg_playtime_by_genre(df)
    
    sns.set_theme()
    
    fig = plots.generate_chart(sns.barplot, df_genre_playtime, x="playtime", y="genres")
    display_chart("Average playtime by genre", fig)
