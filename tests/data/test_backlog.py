import pandas as pd
import pytest

from data import backlog as bl
from data import mappings


TEST_DATA = {
    "ID": [5, 6, 7],
    "Game": ["Ms. Pac-Man", "Resident Evil", "Bomberman 64"],
    "Completion": ["Unplayed", "Played", "Played"]
}
TEST_COLUMN_NAMES = list(TEST_DATA.keys())
DEFAULT_DATAFRAME = pd.DataFrame(TEST_DATA)

TEST_SOURCE_COLUMNS = ["ID", "Game", "Completion"]
TEST_TARGET_COLUMNS = ["IGDB ID", "Game Name", "Completion Status"]
DEFAULT_MAPPING = mappings.ColumnMapping(TEST_SOURCE_COLUMNS, TEST_TARGET_COLUMNS)

def empty_dataframe(column_names):
    return pd.DataFrame({ x: [] for x in column_names })

def empty_backlog(column_names):
    return bl.BacklogExport(empty_dataframe(column_names), DEFAULT_MAPPING)

@pytest.fixture
def default_backlog():
    return bl.BacklogExport(DEFAULT_DATAFRAME, DEFAULT_MAPPING)

class TestBacklogExportConstructor:
    def test_constructor_initializes_dataframe(self, default_backlog):
        assert isinstance(default_backlog._data, pd.DataFrame)
        
    def test_constructor_initializes_mapping(self, default_backlog):
        assert isinstance(default_backlog._mapping, mappings.ColumnMapping)
        
    def test_constructor_loads_dataframe(self, default_backlog):        
        assert default_backlog._data.equals(DEFAULT_DATAFRAME)
        
    def test_constructor_loads_mapping(self, default_backlog):
        assert default_backlog._mapping == DEFAULT_MAPPING
        
    def test_constructor_sets_generated_to_false(self, default_backlog):        
        assert default_backlog._generated == False

class TestColumnRenamer:
    def test_renames_columns(self, default_backlog):
        default_backlog._rename_columns()

        assert default_backlog.get_column_names() == TEST_TARGET_COLUMNS

    def test_leaves_nonmatching_columns(self):
        backlog = empty_backlog([
            "ID", 
            "Game", 
            "Platform", 
            "Completion", 
            "Status", 
            "Release Date"
        ])

        backlog._rename_columns()
        
        assert backlog.get_column_names() == [
            "IGDB ID", 
            "Game Name", 
            "Platform", 
            "Completion Status", 
            "Status", 
            "Release Date"
        ]
        
    def test_raises_value_error_if_not_all_columns_renamed(self):
        backlog = empty_backlog(["ID", "Platform", "Completion"])
        
        with pytest.raises(ValueError) as exception_info:
            backlog._rename_columns()
        
        assert isinstance(exception_info.value, ValueError)
        
    def test_sets_value_error_message(self):
        backlog = empty_backlog(["ID", "Platform", "Completion"])
        
        with pytest.raises(ValueError) as exception_info:
            backlog._rename_columns()
            
        assert str(exception_info.value) == "One or more source columns is missing."
        
    def test_keeps_original_data_if_value_error_is_raised(self):
        backlog = empty_backlog(["ID", "Platform", "Completion"])
        original_data = backlog._data
        
        with pytest.raises(ValueError) as _:
            backlog._rename_columns()
            
        assert backlog._data.equals(original_data)
        
class TestColumnNames:
    def test_returns_list_of_column_names(self, default_backlog):
        assert default_backlog.get_column_names() == TEST_COLUMN_NAMES
        
class TestAllRenamedColumnsExist:
    def test_returns_true_if_all_columns_exist(self, default_backlog):
        test_data = empty_dataframe(["IGDB ID", "Game Name", "Completion Status"])
        
        assert default_backlog._all_renamed_columns_exist(test_data)
        
    def test_returns_false_if_a_column_is_missing_from_the_dataframe(self, default_backlog):
        test_data = empty_dataframe(["IGDB ID", "Not Game", "Completion Status"])
        
        assert not default_backlog._all_renamed_columns_exist(test_data)

    def test_disregards_extra_columns(self, default_backlog):
        test_data = empty_dataframe(["IGDB ID", "Another one", "Game Name", "This too", "Completion Status"])
        
        assert default_backlog._all_renamed_columns_exist(test_data)

class TestDropExtraColumns:
    def test_drops_columns_not_in_list(self):
        backlog = empty_backlog(["IGDB ID", "Another one", "Game Name", "This too", "Completion Status"])

        backlog._drop_extra_columns()
        
        assert backlog.get_column_names() == TEST_TARGET_COLUMNS
        
    def test_throws_key_error_if_column_is_missing(self):
        backlog = empty_backlog(["ID", "Another one", "This too", "Completion"])
        
        with pytest.raises(KeyError) as exception_info:
            backlog._drop_extra_columns()
        
        assert isinstance(exception_info.value, KeyError)
        
class TestGenerate:
    def test_renames_and_drops(self):
        backlog = empty_backlog(["ID", "Another one", "Game", "This too", "Completion"])

        backlog.generate()
        
        assert backlog.get_column_names() == TEST_TARGET_COLUMNS
        
    def test_sets_generated_to_true(self):
        backlog = empty_backlog(["ID", "Another one", "Game", "This too", "Completion"])

        backlog.generate()
        
        assert backlog._generated == True

class TestGetDataframe:
    def test_returns_dataframe(self, default_backlog):
        result = default_backlog.get_dataframe()
        
        assert isinstance(result, pd.DataFrame)
        
    def test_returns_the_correct_dataframe(self, default_backlog):
        result = default_backlog.get_dataframe()
        
        assert result.equals(default_backlog._data)
