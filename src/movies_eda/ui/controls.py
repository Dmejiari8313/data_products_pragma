"""Streamlit basic controls for the Movies EDA dashboard."""

from __future__ import annotations

import streamlit as st

from movies_eda.config import DEFAULT_TOP_N, TOP_N_MAX, TOP_N_MIN


def top_n_control() -> int:
    """Render a slider to choose the Top-N value for rankings.

    Returns
    -------
    int
        The selected Top-N value.
    """
    return int(
        st.slider(
            "Top N categorías",
            min_value=TOP_N_MIN,
            max_value=TOP_N_MAX,
            value=DEFAULT_TOP_N,
        )
    )


def year_range_control(min_year: int, max_year: int) -> tuple[int, int]:
    """Render a slider to choose an inclusive year range.

    Parameters
    ----------
    min_year : int
        Smallest selectable year (dataset minimum).
    max_year : int
        Largest selectable year (dataset maximum).

    Returns
    -------
    tuple of int
        The selected ``(start_year, end_year)`` range.
    """
    start, end = st.slider(
        "Rango de años",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
    return int(start), int(end)
