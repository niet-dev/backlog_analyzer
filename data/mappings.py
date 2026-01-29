from dataclasses import dataclass


@dataclass(frozen=True)
class ColumnMapping:
    source_names: list[str]
    target_names: list[str]


INFINITE_BACKLOG_MAPPING = ColumnMapping(
    source_names=[
        "IGDB ID",
        "Game name",
        "Game release date",
        "Platform",
        "Status",
        "Completion",
        "Playtime",
        "Rating (Score)",
        "Tags",
        "Date added",
        "Last updated"
    ],
    target_names=[
        "IGDB ID",
        "Game Name",
        "Release Date",
        "Platform",
        "Status",
        "Completion",
        "Playtime",
        "Rating",
        "Tags",
        "Date Added",
        "Last Updated"
    ]
)
