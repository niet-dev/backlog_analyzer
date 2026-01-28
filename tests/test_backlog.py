import pandas as pd
import pytest

from data.backlog import BacklogExport

TEST_DATA = {
    "Game": ["Ms. Pac-Man", "Resident Evil", "Bomberman 64"],
    "Platform": ["Arcade", "Playstation", "Nintendo 64"],
    "Status": ["Unplayed", "Played", "Played"]
}
TEST_COLUMN_NAMES = list(TEST_DATA.keys())
DEFAULT_DATAFRAME = pd.DataFrame(TEST_DATA)

def column_names_as_list(export: BacklogExport) -> list[str]:
    return export.data.columns.to_list()

class TestBacklogExportConstructor:
    def test_default_constructor_creates_empty_dataframe(self):
        backlog = BacklogExport()
        
        assert isinstance(backlog.data, pd.DataFrame)
        assert backlog.data.empty
        
    def test_constructor_loads_dataframe(self):
        backlog = BacklogExport(DEFAULT_DATAFRAME)
        
        assert backlog.get_column_names() == TEST_COLUMN_NAMES

"""Map the columns using rename, throw an exception if one is not found"""
class TestColumnRenamer:
    @pytest.fixture
    def start_names(self):
        return ["Game", "Platform", "Status"]
    
    @pytest.fixture
    def end_names(self):
        return ["Modified Game", "Modified Platform", "Modified Status"]
    
    def empty_dataframe(self, column_names):
        return pd.DataFrame({ x: [] for x in column_names })

    def test_renames_columns(self, start_names, end_names):
        backlog = BacklogExport(self.empty_dataframe([
            "Game", 
            "Platform", 
            "Status"]))

        backlog._rename_columns(start_names, end_names)

        assert backlog.get_column_names() == [
            "Modified Game", 
            "Modified Platform", 
            "Modified Status"]

    def test_leaves_nonmatching_columns(self, start_names, end_names):
        backlog = BacklogExport(self.empty_dataframe([
             "ID", 
             "Game", 
             "Platform", 
             "Completion", 
             "Status", 
             "Release Date"]))

        backlog._rename_columns(start_names, end_names)
        
        assert backlog.get_column_names() == [
            "ID", 
            "Modified Game", 
            "Modified Platform", 
            "Completion", 
            "Modified Status", 
            "Release Date"]
        
    def test_raises_value_error_if_not_all_columns_renamed(
        self, start_names, end_names):
        backlog = BacklogExport(self.empty_dataframe([
            "ID", 
            "Game",
            "Completion"
        ]))
        
        with pytest.raises(ValueError) as exception_info:
            backlog._rename_columns(start_names, end_names)
        
        assert isinstance(exception_info.value, ValueError)
        
class TestColumnNames:
    def test_returns_list_of_column_names(self):
        backlog = BacklogExport(DEFAULT_DATAFRAME)
        
        assert backlog.get_column_names() == TEST_COLUMN_NAMES