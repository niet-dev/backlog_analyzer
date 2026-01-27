import pandas as pd
import pytest

from data.backlog import BacklogExport

TEST_CSV_PATH = "tests/data/test_infinitebacklog.csv"
TEST_DATA = {
    "Game": ["Ms. Pac-Man", "Resident Evil", "Bomberman 64"],
    "Platform": ["Arcade", "Playstation", "Nintendo 64"],
    "Status": ["Unplayed", "Played", "Played"]
}
TEST_COLUMN_NAMES = list(TEST_DATA.keys())

class TestBacklogExportConstructor:
    def test_default_constructor_creates_empty_dataframe(self):
        backlog = BacklogExport()
        
        assert isinstance(backlog.data, pd.DataFrame)
        assert backlog.data.empty
        
    def test_constructor_loads_csv_at_path(self, monkeypatch):
        self._mock_read_csv(monkeypatch)
        
        backlog = BacklogExport(TEST_CSV_PATH)
        
        assert backlog.data.columns.to_list() == TEST_COLUMN_NAMES
        
    def _mock_read_csv(self, monkeypatch):
        def mockreturn(_):
            return pd.DataFrame(TEST_DATA)
        
        monkeypatch.setattr(pd, "read_csv", mockreturn)


"""Map the columns using rename, throw an exception if one is not found"""
class TestColumnRenamer:
    @pytest.fixture
    def test_backlog(self, mock_read_csv):
        return BacklogExport("fake file path")    

    @pytest.fixture
    def mock_read_csv(self, monkeypatch):
        def return_test_dataframe(_):
            return pd.DataFrame(TEST_DATA)
        
        monkeypatch.setattr(pd, "read_csv", return_test_dataframe)
        
    def test_renames_columns(self, test_backlog):
        test_backlog._map_column_names(["Game", "Platform", "Status"], ["Game Name", "Platform Name", "Status Name"])
        
        assert test_backlog.data.columns.to_list() == ["Game Name", "Platform Name", "Status Name"]
