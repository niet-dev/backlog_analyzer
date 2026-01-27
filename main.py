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


class BacklogExport():
    def __init__(self, path=None):
        self.data = pd.DataFrame()
    
    def read_backlog_file(self, relative_path):
        return pd.read_csv(relative_path)

    def remove_extra_columns(self, dataframe):
        return dataframe[dataframe.columns.intersection(INFINITE_BACKLOG_COLUMNS)]
