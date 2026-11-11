"""Data quality logic for the Movies EDA dashboard."""

from __future__ import annotations

import pandas as pd

from movies_eda.logging_config import get_logger

logger = get_logger(__name__)


def compute_data_quality(frame: pd.DataFrame) -> pd.DataFrame:
    """Compute per-column data quality metrics.

    For each column, the number of null values and the number of zero values is
    reported. Zeros are especially relevant for ``budget`` and ``revenue``,
    where a zero means "unknown".

    Parameters
    ----------
    frame : pandas.DataFrame
        Dataset to evaluate. Typically the raw dataset, so sentinel zeros are
        still visible.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns ``column``, ``null_count`` and ``zero_count``,
        one row per column of the input.
    """
    logger.info("Computing data quality for %d columns", frame.shape[1])

    records: list[dict[str, object]] = []
    for column in frame.columns:
        series = frame[column]
        null_count = int(series.isna().sum())
        numeric = pd.to_numeric(series, errors="coerce")
        zero_count = int((numeric == 0).sum())
        records.append({"column": column, "null_count": null_count, "zero_count": zero_count})

    result = pd.DataFrame.from_records(records, columns=["column", "null_count", "zero_count"])
    logger.info("Data quality computed")
    return result
