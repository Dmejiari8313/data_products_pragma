"""Unit tests for the categorical aggregation logic."""

from __future__ import annotations

import pandas as pd

from movies_eda.analysis.categorical import (
    movies_per_year,
    top_genres,
    top_languages,
)
from movies_eda.data.cleaning import clean_movies


def test_top_genres_counts_exploded_genres(sample_raw_df: pd.DataFrame) -> None:
    """top_genres returns genre counts sorted descending."""
    cleaned = clean_movies(sample_raw_df)

    result = top_genres(cleaned, n=10)

    assert list(result.columns) == ["genre", "count"]
    counts = dict(zip(result["genre"], result["count"], strict=True))
    # "Action", "Adventure" and "Fantasy" each appear in multiple rows.
    assert counts["Action"] == 3
    assert counts["Adventure"] == 3
    assert counts["Fantasy"] == 2
    assert counts["Drama"] == 1


def test_top_genres_respects_n(sample_raw_df: pd.DataFrame) -> None:
    """top_genres limits the result to the top N categories."""
    cleaned = clean_movies(sample_raw_df)

    result = top_genres(cleaned, n=2)

    assert len(result) == 2


def test_top_genres_n_exceeds_categories_returns_all(sample_raw_df: pd.DataFrame) -> None:
    """When N exceeds available categories, all categories are returned."""
    cleaned = clean_movies(sample_raw_df)

    result = top_genres(cleaned, n=100)

    # Unique genres in fixture: Action, Adventure, Fantasy, Crime, Drama.
    assert len(result) == 5


def test_top_languages_counts(sample_raw_df: pd.DataFrame) -> None:
    """top_languages returns language counts sorted descending."""
    cleaned = clean_movies(sample_raw_df)

    result = top_languages(cleaned, n=10)

    assert list(result.columns) == ["language", "count"]
    counts = dict(zip(result["language"], result["count"], strict=True))
    assert counts["en"] == 3
    assert counts["fr"] == 1
    assert counts["es"] == 1


def test_movies_per_year_excludes_invalid_years(sample_raw_df: pd.DataFrame) -> None:
    """movies_per_year excludes rows whose release_year is missing."""
    cleaned = clean_movies(sample_raw_df)

    result = movies_per_year(cleaned, year_range=(1900, 2025))

    assert list(result.columns) == ["year", "count"]
    # Four rows have a valid year (one is "not-a-date").
    assert int(result["count"].sum()) == 4


def test_movies_per_year_respects_range(sample_raw_df: pd.DataFrame) -> None:
    """movies_per_year filters rows to the requested year range."""
    cleaned = clean_movies(sample_raw_df)

    result = movies_per_year(cleaned, year_range=(2008, 2016))

    # Valid years: 2009, 2007, 2015, 2012. Within [2008, 2016]: 2009, 2015, 2012.
    assert int(result["count"].sum()) == 3
    assert 2007 not in result["year"].tolist()
