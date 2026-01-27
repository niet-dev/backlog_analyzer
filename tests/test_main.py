import pandas as pd
import pytest

from main import BacklogExport, INFINITE_BACKLOG_COLUMNS

TEST_CSV_PATH = "tests/data/test_infinitebacklog.csv"

class TestReadBacklogFile:
    @pytest.fixture
    def backlog(self):
        return BacklogExport()

    def test_creates_dataframe(self, backlog):
        backlog_file = backlog.read_backlog_file(TEST_CSV_PATH)
        
        assert isinstance(backlog_file, pd.DataFrame)
        
    def test_reads_file_at_path(self, backlog):
        backlog_file = backlog.read_backlog_file(TEST_CSV_PATH)
        header_line = None
        
        with open(TEST_CSV_PATH) as file:
            header_line = file.readline().strip()
        header_array = header_line.split(",")
        
        assert header_array == backlog_file.columns.to_list()
