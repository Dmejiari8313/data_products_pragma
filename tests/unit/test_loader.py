"""Unit tests for the dataset loader (logic layer)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from movies_eda.data.loader import MissingColumnsError, load_movies


def _write_csv(path: Path, df: pd.DataFrame) -> Path:
    """Write a DataFrame to CSV and return the path."""
    df.to_csv(path, index=False)
    return path


def test_load_movies_reads_expected_columns(
    tmp_path: Path, sample_raw_df: pd.DataFrame, expected_columns: list[str]
) -> None:
    """load_movies returns a DataFrame containing all expected columns."""
    csv_path = _write_csv(tmp_path / "movies.csv", sample_raw_df)

    result = load_movies(csv_path)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == len(sample_raw_df)
    for column in expected_columns:
        assert column in result.columns


def test_load_movies_missing_file_raises(tmp_path: Path) -> None:
    """load_movies raises FileNotFoundError when the CSV does not exist."""
    missing = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        load_movies(missing)


def test_load_movies_missing_column_raises(tmp_path: Path, sample_raw_df: pd.DataFrame) -> None:
    """load_movies raises MissingColumnsError when an expected column is absent."""
    incomplete = sample_raw_df.drop(columns=["revenue"])
    csv_path = _write_csv(tmp_path / "incomplete.csv", incomplete)

    with pytest.raises(MissingColumnsError) as exc_info:
        load_movies(csv_path)

    assert "revenue" in str(exc_info.value)
