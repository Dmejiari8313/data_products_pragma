"""Dataset loading logic for the Movies EDA dashboard.

Pure, Streamlit-independent functions to read ``movies.csv`` and validate that
the columns required by the overview page are present.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from movies_eda.logging_config import get_logger

logger = get_logger(__name__)

#: Columns required by the overview page logic.
REQUIRED_COLUMNS: tuple[str, ...] = (
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
)


class MissingColumnsError(ValueError):
    """Raised when the dataset is missing one or more required columns."""


def load_movies(path: str | Path) -> pd.DataFrame:
    """Load the movies dataset from a CSV file.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV dataset.

    Returns
    -------
    pandas.DataFrame
        The loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at ``path``.
    MissingColumnsError
        If one or more columns in :data:`REQUIRED_COLUMNS` are absent.
    """
    csv_path = Path(path)
    logger.info("Starting dataset load from %s", csv_path)

    if not csv_path.is_file():
        logger.error("Dataset file not found: %s", csv_path)
        raise FileNotFoundError(f"Dataset file not found: {csv_path}")

    frame = pd.read_csv(csv_path)
    _validate_columns(frame)

    logger.info("Dataset loaded successfully: %d rows, %d columns", len(frame), frame.shape[1])
    return frame


def _validate_columns(frame: pd.DataFrame) -> None:
    """Validate that all required columns are present in the DataFrame.

    Parameters
    ----------
    frame : pandas.DataFrame
        The loaded dataset to validate.

    Raises
    ------
    MissingColumnsError
        If one or more required columns are missing.
    """
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        logger.error("Dataset is missing required columns: %s", missing)
        raise MissingColumnsError(f"Missing required columns: {', '.join(missing)}")
