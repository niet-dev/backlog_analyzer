import logging
import pandas as pd

def _all_renamed_columns_exist(dataframe: pd.DataFrame, target_names: list[str]) -> bool:
    in_common = dataframe.columns.intersection(target_names)

    return in_common.equals(pd.Index(target_names))


class BacklogExport():
    _data: pd.DataFrame
    _generated: bool
    
    def __init__(self, data: pd.DataFrame=pd.DataFrame()) -> None:
        self._data = data
        self._generated = False
        
    def get_column_names(self) -> list[str]:
        return self._data.columns.to_list()
    
    def generate(self, source_names, target_names):
        self._rename_columns(source_names, target_names)
        self._drop_extra_columns(target_names)
        self._generated = True
        
    def _rename_columns(
        self, source_names: list[str], target_names: list[str]) -> None:
        name_mapping = { x: y for x, y in zip(source_names, target_names) }
        
        result = self._data.rename(columns=name_mapping)
        
        if not _all_renamed_columns_exist(result, target_names):
            raise ValueError("One or more source columns is missing.")
        
        self._data = result
        
    def _drop_extra_columns(self, columns_to_keep):
        self._data = self._data[columns_to_keep]
