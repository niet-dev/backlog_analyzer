from typing import Callable

from matplotlib import pyplot
import pandas as pd

from data import dataframes

def avg_playtime(
    df: pd.DataFrame,
    column: str,
    min_games: int=5,
    drop_unplayed: bool=True,
    max_results: int=20
) -> pd.DataFrame:
    dataframes.validate_columns(df, [column, "playtime"])
    
    exploded = df.explode(column).reset_index(drop=True)
    exploded = dataframes.playtime_minutes_to_hours(exploded)
    
    if drop_unplayed:
        exploded = dataframes.drop_games_with_no_playtime(exploded)
        
    counts = exploded[column].value_counts()
    valid = counts[counts >= min_games].index
    
    filtered = exploded[exploded[column].isin(valid)]
    
    return filtered\
        .groupby(column)\
        .agg({"playtime": "mean"})\
        .reset_index()\
        .sort_values("playtime", ascending=False)\
        .head(max_results)

def avg_rating(
    df: pd.DataFrame,
    column: str,
    min_games: int=5,
    drop_unplayed: bool=True,
    max_results: int=20
) -> pd.DataFrame:
    dataframes.validate_columns(df, [column, "rating"])
    
    exploded = df.explode(column).reset_index(drop=True)
    
    if drop_unplayed:
        exploded = dataframes.drop_games_with_no_playtime(exploded)
        
    counts = exploded[column].value_counts()
    valid = counts[counts >= min_games].index
    
    filtered = exploded[exploded[column].isin(valid)]
    
    return filtered\
        .groupby(column)\
        .agg({"rating": "mean"})\
        .reset_index()\
        .sort_values("rating", ascending=False)\
        .head(max_results)

def generate_chart(plot_fn: Callable, df: pd.DataFrame, **kwargs):
    fig, ax = pyplot.subplots()
    plot_fn(data=df, ax=ax, **kwargs)
    
    return fig
