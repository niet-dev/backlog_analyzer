import logging
import pandas as pd

class BacklogExport():
    def __init__(self, path: str | None=None) -> None:
        self.data = pd.read_csv(path) if path else pd.DataFrame()
        
    def _map_column_names(self, old_names, new_names):
        self.data.columns = new_names
        
