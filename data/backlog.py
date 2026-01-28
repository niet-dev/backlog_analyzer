import logging
import pandas as pd

def _all_renamed_columns_exist(dataframe: pd.DataFrame, target_names: list[str]) -> bool:
    in_common = dataframe.columns.intersection(target_names)

    return in_common.equals(pd.Index(target_names))


class BacklogExport():
    data: pd.DataFrame
    
    def __init__(self, data: pd.DataFrame=pd.DataFrame()) -> None:
        self.data = data
        
    def get_column_names(self) -> list[str]:
        return self.data.columns.to_list()
        
    def _rename_columns(
        self, source_names: list[str], target_names: list[str]) -> None:
        name_mapping = { x: y for x, y in zip(source_names, target_names) }
        
        result = self.data.rename(columns=name_mapping)
        
        if not _all_renamed_columns_exist(result, target_names):
            raise ValueError("One or more source columns is missing.")
        
        self.data = result
