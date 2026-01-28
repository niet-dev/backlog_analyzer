import logging
import pandas as pd


class BacklogExport():
    data: pd.DataFrame
    
    def __init__(self, data: pd.DataFrame=pd.DataFrame()) -> None:
        self.data = data
        
    def _rename_columns(
        self, source_names: list[str], target_names: list[str]) -> None:
        name_mapping = { x: y for x, y in zip(source_names, target_names) }
        
        self.data = self.data.rename(columns=name_mapping)
        
        if not self._all_renamed_columns_exist(target_names):
            raise ValueError("One or more source columns is missing.")
        
    def _all_renamed_columns_exist(self, renamed_columns):
        target_names = pd.Index(renamed_columns)
        in_common = self.data.columns.intersection(target_names)
        
        return in_common.equals(target_names)
        

    def get_column_names(self):
        return self.data.columns.to_list()