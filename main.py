import pandas as pd

INFINITE_BACKLOG_COLUMNS = [
    "IGDB ID", 
    "Game name", 
    "Game release date",
    "Platform",
    "Status",
    "Completion",
    "Playtime",
    "Rating (Score)",
    "Tags",
    "Date added",
    "Last updated"
]

REPORT_COLUMNS = [
    "ID",
    "Name",
    "Release Date",
    "Platform",
    "Play Status",
    "Completion",
    "Playtime",
    "Rating (1-10)",
    "Tags",
    "Date Added",
    "Last Updated"
]

CSV_PATH = "data.csv"

def _drop_unneeded_backlog_columns(df):
    return df[df.columns.intersection(INFINITE_BACKLOG_COLUMNS)]

def _map_backlog_columns_to_report_columns(df):
    column_mapping = dict(zip(INFINITE_BACKLOG_COLUMNS, REPORT_COLUMNS))
    return df.rename(columns=column_mapping)

def _format_backlog_dataframe(df):
    backlog_with_dropped_columns = _drop_unneeded_backlog_columns(df)
    backlog_with_correct_columns = \
        _map_backlog_columns_to_report_columns(backlog_with_dropped_columns)
    return backlog_with_correct_columns

def _create_dataframe_from_backlog_file():
    return pd.read_csv(CSV_PATH)

def process_backlog_file():
    backlog_df = _create_dataframe_from_backlog_file()
    formatted_backlog = _format_backlog_dataframe(backlog_df)
    print(formatted_backlog.head())

process_backlog_file()