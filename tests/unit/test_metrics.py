"""Unit tests for the summary metrics (KPIs) logic."""

from __future__ import annotations

import math

import pandas as pd

from movies_eda.analysis.metrics import SummaryMetrics, compute_summary_metrics
from movies_eda.data.cleaning import clean_movies


def test_compute_summary_metrics_returns_dataclass(sample_raw_df: pd.DataFrame) -> None:
    """compute_summary_metrics returns a SummaryMetrics instance."""
    cleaned = clean_movies(sample_raw_df)

    metrics = compute_summary_metrics(cleaned)

    assert isinstance(metrics, SummaryMetrics)


def test_total_movies_counts_all_rows(sample_raw_df: pd.DataFrame) -> None:
    """total_movies equals the number of rows in the dataset."""
    cleaned = clean_movies(sample_raw_df)

    metrics = compute_summary_metrics(cleaned)

    assert metrics.total_movies == len(sample_raw_df)


def test_avg_budget_excludes_missing(sample_raw_df: pd.DataFrame) -> None:
    """avg_budget is computed only over non-missing (non-zero) budget values."""
    cleaned = clean_movies(sample_raw_df)

    metrics = compute_summary_metrics(cleaned)

    # Non-zero budgets in the fixture: 237000000, 150000000, 50000000.
    expected = (237000000 + 150000000 + 50000000) / 3
    assert math.isclose(metrics.avg_budget, expected, rel_tol=1e-6)


def test_year_range(sample_raw_df: pd.DataFrame) -> None:
    """min_year and max_year reflect the valid release years."""
    cleaned = clean_movies(sample_raw_df)

    metrics = compute_summary_metrics(cleaned)

    assert metrics.min_year == 2007
    assert metrics.max_year == 2015
