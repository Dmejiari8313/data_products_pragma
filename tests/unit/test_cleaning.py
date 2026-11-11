"""Unit tests for the data cleaning logic."""

from __future__ import annotations

import pandas as pd

from movies_eda.data.cleaning import clean_movies, parse_genres


def test_clean_movies_converts_budget_zeros_to_nan(sample_raw_df: pd.DataFrame) -> None:
    """Zeros in budget are converted to NaN (treated as missing)."""
    cleaned = clean_movies(sample_raw_df)

    # Two rows have budget == 0 in the fixture.
    assert cleaned["budget"].isna().sum() == 2


def test_clean_movies_converts_revenue_zeros_to_nan(sample_raw_df: pd.DataFrame) -> None:
    """Zeros in revenue are converted to NaN (treated as missing)."""
    cleaned = clean_movies(sample_raw_df)

    # Two rows have revenue == 0 in the fixture.
    assert cleaned["revenue"].isna().sum() == 2


def test_clean_movies_parses_release_year(sample_raw_df: pd.DataFrame) -> None:
    """A release_year column is derived from valid release_date values."""
    cleaned = clean_movies(sample_raw_df)

    assert "release_year" in cleaned.columns
    # Row with "not-a-date" must become NaT -> year is NaN.
    assert cleaned["release_year"].isna().sum() == 1
    valid_years = cleaned["release_year"].dropna().astype(int).tolist()
    assert 2009 in valid_years
    assert 2007 in valid_years


def test_clean_movies_does_not_mutate_input(sample_raw_df: pd.DataFrame) -> None:
    """clean_movies returns a new DataFrame without mutating the input."""
    original_budget = sample_raw_df["budget"].tolist()

    clean_movies(sample_raw_df)

    assert sample_raw_df["budget"].tolist() == original_budget


def test_parse_genres_splits_multiple_genres() -> None:
    """parse_genres splits a space-separated string into a list of tokens."""
    assert parse_genres("Action Adventure Fantasy") == ["Action", "Adventure", "Fantasy"]


def test_parse_genres_handles_single_genre() -> None:
    """parse_genres returns a single-element list for one genre."""
    assert parse_genres("Drama") == ["Drama"]


def test_parse_genres_handles_missing_values() -> None:
    """parse_genres returns an empty list for missing or blank values."""
    assert parse_genres(None) == []
    assert parse_genres(float("nan")) == []
    assert parse_genres("") == []
    assert parse_genres("   ") == []
