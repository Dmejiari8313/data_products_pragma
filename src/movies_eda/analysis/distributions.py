"""Distribution series logic for the Movies EDA dashboard."""

from __future__ import annotations

import pandas as pd

from movies_eda.logging_config import get_logger

logger = get_logger(__name__)


def distribution_series(frame: pd.DataFrame, column: str) -> pd.Series:
    """Return a numeric series ready for a distribution histogram.

    Missing values (``NaN``/``NA``) are excluded, so columns whose sentinel
    zeros were converted to missing during cleaning yield only real values.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset.
    column : str
        Name of the numeric column to extract.

    Returns
    -------
    pandas.Series
        The non-missing numeric values of ``column``. Empty when no data is
        available or the column is absent.

    Raises
    ------
    KeyError
        If ``column`` is not present in ``frame``.
    """
    if column not in frame.columns:
        logger.error("Column not found for distribution: %s", column)
        raise KeyError(f"Column not found: {column}")

    numeric = pd.to_numeric(frame[column], errors="coerce").dropna()
    logger.info("Distribution series for '%s': %d values", column, len(numeric))
    return numeric
