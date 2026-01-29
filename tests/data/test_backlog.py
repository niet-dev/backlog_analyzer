import pandas as pd
import pytest

from data import backlog as bl

TEST_DATA = {
    "Game": ["Ms. Pac-Man", "Resident Evil", "Bomberman 64"],
    "Platform": ["Arcade", "Playstation", "Nintendo 64"],
    "Status": ["Unplayed", "Played", "Played"]
}
TEST_COLUMN_NAMES = list(TEST_DATA.keys())
DEFAULT_DATAFRAME = pd.DataFrame(TEST_DATA)

def empty_dataframe(column_names):
    return pd.DataFrame({ x: [] for x in column_names })

def empty_backlog(column_names):
    return bl.BacklogExport(empty_dataframe(column_names))

class TestBacklogExportConstructor:
    def test_default_constructor_creates_empty_dataframe(self):
        backlog = bl.BacklogExport()
        
        assert isinstance(backlog._data, pd.DataFrame)
        assert backlog._data.empty
        
    def test_constructor_loads_dataframe(self):
        backlog = bl.BacklogExport(DEFAULT_DATAFRAME)
        
        assert backlog.get_column_names() == TEST_COLUMN_NAMES
        
    def test_constructor_sets_generated_to_false(self):
        backlog = bl.BacklogExport(DEFAULT_DATAFRAME)
        
        assert backlog._generated == False

"""Map the columns using rename, throw an exception if one is not found"""
class TestColumnRenamer:
    @pytest.fixture
    def start_names(self) -> list[str]:
        return ["Game", "Platform", "Status"]
    
    @pytest.fixture
    def end_names(self) -> list[str]:
        return ["Modified Game", "Modified Platform", "Modified Status"]

    def test_renames_columns(self, start_names, end_names):
        backlog = empty_backlog(["Game", "Platform", "Status"])

        backlog._rename_columns(start_names, end_names)

        assert backlog.get_column_names() == [
            "Modified Game", 
            "Modified Platform", 
            "Modified Status"
        ]

    def test_leaves_nonmatching_columns(self, start_names, end_names):
        backlog = empty_backlog([
            "ID", 
            "Game", 
            "Platform", 
            "Completion", 
            "Status", 
            "Release Date"
        ])

        backlog._rename_columns(start_names, end_names)
        
        assert backlog.get_column_names() == [
            "ID", 
            "Modified Game", 
            "Modified Platform", 
            "Completion", 
            "Modified Status", 
            "Release Date"
        ]
        
    def test_raises_value_error_if_not_all_columns_renamed(
        self, start_names, end_names
    ):
        backlog = empty_backlog(["ID", "Game", "Completion"])
        
        with pytest.raises(ValueError) as exception_info:
            backlog._rename_columns(start_names, end_names)
        
        assert isinstance(exception_info.value, ValueError)
        
    def test_sets_value_error_message(self, start_names, end_names):
        backlog = empty_backlog(["ID", "Game", "Completion"])
        
        with pytest.raises(ValueError) as exception_info:
            backlog._rename_columns(start_names, end_names)
            
        assert str(exception_info.value) == "One or more source columns is missing."
        
    def test_keeps_original_data_if_value_error_is_raised(
        self, start_names, end_names
    ):
        backlog = empty_backlog(["ID", "Game", "Completion"])
        
        start_columns = backlog.get_column_names()
        
        with pytest.raises(ValueError) as _:
            backlog._rename_columns(start_names, end_names)
            
        assert backlog.get_column_names() == start_columns
        
class TestColumnNames:
    def test_returns_list_of_column_names(self):
        backlog = bl.BacklogExport(DEFAULT_DATAFRAME)
        
        assert backlog.get_column_names() == TEST_COLUMN_NAMES
        
class TestAllRenamedColumnsExist:
    def test_returns_true_if_all_columns_exist(self):
        backlog = empty_dataframe(["ID", "Game", "Completion"])
        target = ["ID", "Game", "Completion"]
        
        assert bl._all_renamed_columns_exist(backlog, target)
        
    def test_returns_false_if_a_column_is_missing_from_the_dataframe(self):
        backlog = empty_dataframe(["ID", "Not Game", "Completion"])
        target = ["ID", "Game", "Completion"]
        
        assert not bl._all_renamed_columns_exist(backlog, target)

    def test_disregards_extra_columns(self):
        backlog = empty_dataframe(["ID", "Another one", "Game", "This too", "Completion"])
        target = ["ID", "Game", "Completion"]
        
        assert bl._all_renamed_columns_exist(backlog, target)

class TestDropExtraColumns:
    def test_drops_columns_not_in_list(self):
        backlog = empty_backlog(["ID", "Another one", "Game", "This too", "Completion"])
        target = ["ID", "Game", "Completion"]
        
        backlog._drop_extra_columns(target)
        
        assert backlog.get_column_names() == target
        
    def test_throws_key_error_if_column_is_missing(self):
        backlog = empty_backlog(["ID", "Another one", "This too", "Completion"])
        target = ["ID", "Game", "Completion"]
        
        with pytest.raises(KeyError) as exception_info:
            backlog._drop_extra_columns(target)
        
        assert isinstance(exception_info.value, KeyError)
        
class TestGenerate:
    def test_renames_and_drops(self):
        backlog = empty_backlog(["ID", "Another one", "Game", "This too", "Completion"])
        rename_source = ["ID", "Game", "Completion"]
        target = ["IGDB ID", "Game Name", "Completion Status"]

        backlog.generate(rename_source, target)
        
        assert backlog.get_column_names() == target
        
    def test_sets_generated_to_true(self):
        backlog = empty_backlog(["ID", "Another one", "Game", "This too", "Completion"])
        rename_source = ["ID", "Game", "Completion"]
        target = ["IGDB ID", "Game Name", "Completion Status"]

        backlog.generate(rename_source, target)
        
        assert backlog._generated == True