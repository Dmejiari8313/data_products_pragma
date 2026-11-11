"""Summary metrics (KPIs) logic for the Movies EDA dashboard."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from movies_eda.logging_config import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class SummaryMetrics:
    """Summary metrics describing the overall dataset.

    Attributes
    ----------
    total_movies : int
        Total number of movies (rows) in the dataset.
    avg_budget : float
        Mean budget over non-missing budget values.
    avg_revenue : float
        Mean revenue over non-missing revenue values.
    avg_runtime : float
        Mean runtime over non-missing runtime values.
    min_year : int
        Earliest release year present in the dataset.
    max_year : int
        Latest release year present in the dataset.
    """

    total_movies: int
    avg_budget: float
    avg_revenue: float
    avg_runtime: float
    min_year: int
    max_year: int


def _safe_mean(series: pd.Series) -> float:
    """Return the mean of a numeric series, or 0.0 when it is empty.

    Parameters
    ----------
    series : pandas.Series
        Numeric series that may contain missing values.

    Returns
    -------
    float
        The mean of non-missing values, or ``0.0`` when none are present.
    """
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return 0.0
    return float(numeric.mean())


def compute_summary_metrics(frame: pd.DataFrame) -> SummaryMetrics:
    """Compute the summary KPIs for the overview panel.

    Budget and revenue averages exclude values treated as missing. The year
    range is derived from the ``release_year`` column, ignoring missing years.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset (see :func:`movies_eda.data.cleaning.clean_movies`).

    Returns
    -------
    SummaryMetrics
        The computed summary metrics.
    """
    logger.info("Computing summary metrics")

    years = pd.to_numeric(frame.get("release_year"), errors="coerce").dropna()
    min_year = int(years.min()) if not years.empty else 0
    max_year = int(years.max()) if not years.empty else 0

    metrics = SummaryMetrics(
        total_movies=int(len(frame)),
        avg_budget=_safe_mean(frame.get("budget", pd.Series(dtype="float64"))),
        avg_revenue=_safe_mean(frame.get("revenue", pd.Series(dtype="float64"))),
        avg_runtime=_safe_mean(frame.get("runtime", pd.Series(dtype="float64"))),
        min_year=min_year,
        max_year=max_year,
    )
    logger.info("Summary metrics computed: %d movies", metrics.total_movies)
    return metrics
