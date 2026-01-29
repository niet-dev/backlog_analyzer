import logging
import pandas as pd
from data import mappings

class BacklogExport():
    _data: pd.DataFrame
    _mapping: mappings.ColumnMapping
    _generated: bool
    
    def __init__(self, data: pd.DataFrame, mapping: mappings.ColumnMapping) -> None:
        self._data = data
        self._mapping = mapping
        self._generated = False
        
    def get_column_names(self) -> list[str]:
        return self._data.columns.to_list()
    
    def generate(self):
        self._rename_columns()
        self._drop_extra_columns()
        self._generated = True
    
    def get_dataframe(self):
        return self._data
        
    def _rename_columns(self) -> None:
        name_mapping = { x: y for x, y in zip(self._mapping.source_names, self._mapping.target_names) }
        
        result = self._data.rename(columns=name_mapping)
        
        if not self._all_renamed_columns_exist(result):
            raise ValueError("One or more source columns is missing.")
        
        self._data = result
        
    def _all_renamed_columns_exist(self, result) -> bool:
        in_common = result.columns.intersection(self._mapping.target_names)

        return in_common.equals(pd.Index(self._mapping.target_names))
        
    def _drop_extra_columns(self):
        self._data = self._data[self._mapping.target_names]
