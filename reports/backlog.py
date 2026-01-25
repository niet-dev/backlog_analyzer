from abc import ABC, abstractmethod
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

class BacklogReport(ABC):
    @abstractmethod
    def __init__(self, path):
        pass
    
    @abstractmethod
    def _drop_unneeded_columns(self):
        pass
    
    @abstractmethod
    def _map_to_report_columns(self):
        pass

    @abstractmethod
    def generate_backlog_report(self):
        pass

class InfiniteBacklogReport(BacklogReport):
    def __init__(self, path):
        self.base = pd.read_csv(path)
        self.formatted = self.base.copy()

    def _drop_unneeded_columns(self):
        self.formatted = self.formatted[
            self.formatted.columns.intersection(INFINITE_BACKLOG_COLUMNS)]

    def _map_to_report_columns(self):
        column_mapping = dict(zip(INFINITE_BACKLOG_COLUMNS, REPORT_COLUMNS))
        self.formatted = self.formatted.rename(columns=column_mapping)

    def generate_backlog_report(self):
        self._drop_unneeded_columns()
        self._map_to_report_columns()

