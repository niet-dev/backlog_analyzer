import dataclasses
import pytest

from data import mappings


class TestColumnMapping:
    def test_contains_source_names(self):
        new_mapping = mappings.ColumnMapping(
            source_names=["Source"],
            target_names=["Target"])

        assert new_mapping.source_names == ["Source"]

    def test_contains_target_names(self):
        new_mapping = mappings.ColumnMapping(
            source_names=["Source"],
            target_names=["Target"])

        assert new_mapping.target_names == ["Target"]

    def test_assigning_after_initialization_throws_exception(self):
        new_mapping = mappings.ColumnMapping(
            source_names=["Source"],
            target_names=["Target"])
        
        with pytest.raises(dataclasses.FrozenInstanceError) as exception_info:
            new_mapping.source_names = ["Uh Oh"] # type: ignore

        assert isinstance(
            exception_info.value,
            dataclasses.FrozenInstanceError)
