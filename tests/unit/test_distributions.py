"""Unit tests for the distribution series logic."""

from __future__ import annotations

import pandas as pd

from movies_eda.analysis.distributions import distribution_series
from movies_eda.data.cleaning import clean_movies


def test_distribution_series_excludes_missing_budget(sample_raw_df: pd.DataFrame) -> None:
    """The budget distribution excludes values treated as missing (zeros)."""
    cleaned = clean_movies(sample_raw_df)

    series = distribution_series(cleaned, "budget")

    assert series.isna().sum() == 0
    # Only 3 non-zero budget values remain.
    assert len(series) == 3


def test_distribution_series_excludes_missing_runtime(sample_raw_df: pd.DataFrame) -> None:
    """The runtime distribution excludes missing values."""
    cleaned = clean_movies(sample_raw_df)

    series = distribution_series(cleaned, "runtime")

    assert series.isna().sum() == 0
    # One runtime is None in the fixture.
    assert len(series) == 4


def test_distribution_series_vote_average_keeps_all(sample_raw_df: pd.DataFrame) -> None:
    """vote_average has no missing values, so all rows are kept."""
    cleaned = clean_movies(sample_raw_df)

    series = distribution_series(cleaned, "vote_average")

    assert len(series) == len(sample_raw_df)


def test_distribution_series_empty_when_all_missing() -> None:
    """distribution_series returns an empty series when no data is available."""
    df = pd.DataFrame({"budget": [0, 0, 0]})

    # clean_movies is not used here on purpose: emulate an all-missing column.
    df["budget"] = pd.NA

    series = distribution_series(df, "budget")

    assert series.empty
