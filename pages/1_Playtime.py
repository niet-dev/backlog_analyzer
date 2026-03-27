from matplotlib.figure import Figure
import seaborn as sns
import streamlit as st

from data import plots

def display_chart(title: str, fig: Figure):
    st.write(f"## {title}")
    st.pyplot(fig)

if "df" not in st.session_state:
    st.warning("Please upload your data on the home page first")
    st.stop()
    
df = st.session_state["df"]
    
sns.set_theme()

for column in ["genres", "themes", "game_modes", "player_perspectives", "keywords"]:
    grouped_df = plots.avg_playtime(df, column)
    fig = plots.generate_chart(sns.barplot, grouped_df, x="playtime", y=column)
    display_chart(f"Average playtime by {column}", fig)

