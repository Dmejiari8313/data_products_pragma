"""Unit tests for the data quality logic."""

from __future__ import annotations

import pandas as pd

from movies_eda.analysis.quality import compute_data_quality


def test_compute_data_quality_columns(sample_raw_df: pd.DataFrame) -> None:
    """compute_data_quality returns the expected column structure."""
    result = compute_data_quality(sample_raw_df)

    assert list(result.columns) == ["column", "null_count", "zero_count"]


def test_compute_data_quality_counts_zeros(sample_raw_df: pd.DataFrame) -> None:
    """Zero counts are reported per column on the raw dataset."""
    result = compute_data_quality(sample_raw_df)
    zero_by_column = dict(zip(result["column"], result["zero_count"], strict=True))

    # Fixture has two zeros in budget and two in revenue.
    assert zero_by_column["budget"] == 2
    assert zero_by_column["revenue"] == 2


def test_compute_data_quality_counts_nulls(sample_raw_df: pd.DataFrame) -> None:
    """Null counts are reported per column."""
    result = compute_data_quality(sample_raw_df)
    null_by_column = dict(zip(result["column"], result["null_count"], strict=True))

    # Fixture has one missing runtime and one missing genres value.
    assert null_by_column["runtime"] == 1
    assert null_by_column["genres"] == 1


def test_compute_data_quality_has_row_per_column(sample_raw_df: pd.DataFrame) -> None:
    """There is exactly one quality row per dataset column."""
    result = compute_data_quality(sample_raw_df)

    assert len(result) == sample_raw_df.shape[1]
