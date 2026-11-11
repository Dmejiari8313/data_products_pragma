"""Categorical and temporal aggregation logic for the Movies EDA dashboard."""

from __future__ import annotations

import pandas as pd

from movies_eda.data.cleaning import parse_genres
from movies_eda.logging_config import get_logger

logger = get_logger(__name__)


def top_genres(frame: pd.DataFrame, n: int) -> pd.DataFrame:
    """Return the top ``n`` most frequent genres.

    The ``genres`` column is parsed and exploded so each genre is counted
    independently. When ``n`` exceeds the number of distinct genres, all genres
    are returned.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset containing a ``genres`` column.
    n : int
        Maximum number of genres to return.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns ``genre`` and ``count``, sorted by ``count``
        in descending order.
    """
    logger.info("Computing top %d genres", n)
    exploded = frame["genres"].apply(parse_genres).explode().dropna()
    counts = exploded.value_counts().head(n)
    result = counts.reset_index()
    result.columns = ["genre", "count"]
    return result


def top_languages(frame: pd.DataFrame, n: int) -> pd.DataFrame:
    """Return the top ``n`` most frequent original languages.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset containing an ``original_language`` column.
    n : int
        Maximum number of languages to return.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns ``language`` and ``count``, sorted by ``count``
        in descending order.
    """
    logger.info("Computing top %d languages", n)
    counts = frame["original_language"].dropna().value_counts().head(n)
    result = counts.reset_index()
    result.columns = ["language", "count"]
    return result


def movies_per_year(frame: pd.DataFrame, year_range: tuple[int, int]) -> pd.DataFrame:
    """Return the number of movies per release year within a range.

    Rows with a missing ``release_year`` are excluded.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset containing a ``release_year`` column.
    year_range : tuple of int
        Inclusive ``(min_year, max_year)`` range to filter on.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns ``year`` and ``count``, sorted by ``year``.
    """
    min_year, max_year = year_range
    logger.info("Computing movies per year in range [%d, %d]", min_year, max_year)

    years = pd.to_numeric(frame["release_year"], errors="coerce").dropna().astype(int)
    mask = (years >= min_year) & (years <= max_year)
    counts = years[mask].value_counts().sort_index()
    result = counts.reset_index()
    result.columns = ["year", "count"]
    return result
