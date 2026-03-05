from typing import Callable

from matplotlib import pyplot
import pandas as pd

def avg_playtime_by_genre(
    df: pd.DataFrame, 
    min_games: int=5, 
    drop_unplayed: bool=True
) -> pd.DataFrame:
    validate_columns(df, ["genres", "playtime"])
    
    df_exploded = df.explode("genres").reset_index(drop=True)
    df_exploded["playtime"] = (df_exploded["playtime"] / 60).round(1)
    
    if drop_unplayed:
        df_exploded = df_exploded[
            df_exploded["playtime"] > 0
        ]

    genre_counts = df_exploded["genres"].value_counts()
    valid_genres = genre_counts[genre_counts >= min_games].index
    df_filtered = df_exploded[
        df_exploded["genres"].isin(valid_genres)
    ]

    return df_filtered.groupby("genres").agg({"playtime": "mean"}).reset_index()
    
def validate_columns(df: pd.DataFrame, columns: list[str]):
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing required columns: {missing}")

def generate_chart(plot_fn: Callable, df: pd.DataFrame, **kwargs):
    fig, ax = pyplot.subplots()
    plot_fn(data=df, ax=ax, **kwargs)
    
    return fig
