"""Shared pytest fixtures for the logic-layer unit tests."""

from __future__ import annotations

import pandas as pd
import pytest

# Columns expected by the loader/cleaning logic for the overview page.
EXPECTED_COLUMNS: list[str] = [
    "budget",
    "revenue",
    "runtime",
    "vote_average",
    "vote_count",
    "popularity",
    "genres",
    "original_language",
    "release_date",
    "title",
]


@pytest.fixture
def sample_raw_df() -> pd.DataFrame:
    """Return a small, representative raw dataset for the logic layer.

    The sample intentionally includes the edge cases the cleaning and analysis
    functions must handle:

    - Zeros in ``budget`` and ``revenue`` (meaning "unknown").
    - An invalid/empty ``release_date`` value.
    - Rows with multiple genres and a missing genres value.
    - A missing ``runtime`` value.

    Returns
    -------
    pandas.DataFrame
        A raw-like DataFrame with the columns expected from ``movies.csv``.
    """
    data = {
        "budget": [237000000, 0, 150000000, 0, 50000000],
        "revenue": [2787965087, 961000000, 0, 0, 120000000],
        "runtime": [162.0, 169.0, None, 100.0, 95.0],
        "vote_average": [7.2, 6.9, 6.3, 5.0, 8.1],
        "vote_count": [11800, 4500, 4466, 120, 3000],
        "popularity": [150.4, 139.1, 107.4, 10.0, 80.0],
        "genres": [
            "Action Adventure Fantasy",
            "Adventure Fantasy Action",
            "Action Adventure Crime",
            None,
            "Drama",
        ],
        "original_language": ["en", "en", "en", "fr", "es"],
        "release_date": [
            "2009-12-10",
            "2007-05-19",
            "2015-10-26",
            "not-a-date",
            "2012-03-01",
        ],
        "title": ["Avatar", "Pirates", "Spectre", "Broken Row", "Indie Film"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def expected_columns() -> list[str]:
    """Return the list of columns expected by the loader.

    Returns
    -------
    list of str
        Expected column names for the overview page logic.
    """
    return list(EXPECTED_COLUMNS)
