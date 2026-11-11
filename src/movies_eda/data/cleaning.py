"""Data cleaning logic for the Movies EDA dashboard.

Pure functions that normalize the raw dataset: treat sentinel zeros as missing,
parse release dates and derive the release year, and parse the genres column.
"""

from __future__ import annotations

import pandas as pd

from movies_eda.logging_config import get_logger

logger = get_logger(__name__)

#: Columns whose zero values represent "unknown" and must be treated as missing.
ZERO_AS_MISSING_COLUMNS: tuple[str, ...] = ("budget", "revenue")


def clean_movies(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the movies dataset.

    The following transformations are applied without mutating the input:

    - Zeros in ``budget`` and ``revenue`` are replaced with ``NaN``.
    - ``release_date`` is parsed to datetime (invalid values become ``NaT``).
    - A ``release_year`` column is derived from ``release_date``.

    Parameters
    ----------
    frame : pandas.DataFrame
        Raw dataset as returned by :func:`movies_eda.data.loader.load_movies`.

    Returns
    -------
    pandas.DataFrame
        A new, cleaned DataFrame.
    """
    logger.info("Starting dataset cleaning on %d rows", len(frame))
    cleaned = frame.copy()

    for column in ZERO_AS_MISSING_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].where(cleaned[column] != 0, other=pd.NA)

    if "release_date" in cleaned.columns:
        parsed_dates = pd.to_datetime(cleaned["release_date"], errors="coerce")
        cleaned["release_date"] = parsed_dates
        cleaned["release_year"] = parsed_dates.dt.year

    logger.info("Dataset cleaning complete")
    return cleaned


def parse_genres(value: object) -> list[str]:
    """Parse a raw genres value into a normalized list of genre names.

    The dataset stores genres as a space-separated string (e.g.
    ``"Action Adventure Fantasy"``). Compound genre words are kept as provided
    by the token split.

    Parameters
    ----------
    value : object
        The raw genres cell value. May be a string or a missing value.

    Returns
    -------
    list of str
        The list of genre tokens. Empty when the value is missing or blank.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)) or pd.isna(value):
        return []
    text = str(value).strip()
    if not text:
        return []
    return text.split()
