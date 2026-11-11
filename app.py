"""Streamlit entry point for the Movies EDA dashboard (overview page).

This module is the presentation layer: it orchestrates the logic layer and
renders the overview page. It contains no business logic.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from movies_eda.analysis.categorical import movies_per_year, top_genres, top_languages
from movies_eda.analysis.distributions import distribution_series
from movies_eda.analysis.metrics import SummaryMetrics, compute_summary_metrics
from movies_eda.analysis.quality import compute_data_quality
from movies_eda.config import get_csv_path
from movies_eda.data.cleaning import clean_movies
from movies_eda.data.loader import MissingColumnsError, load_movies
from movies_eda.logging_config import configure_logging, get_logger
from movies_eda.ui import charts, controls

configure_logging()
logger = get_logger(__name__)


@st.cache_data(show_spinner="Cargando dataset...")
def _load_raw(path_str: str) -> pd.DataFrame:
    """Load the raw dataset, cached by path for performance.

    Parameters
    ----------
    path_str : str
        String path to the CSV dataset (string for cache hashing).

    Returns
    -------
    pandas.DataFrame
        The raw dataset (sentinel zeros still present).
    """
    return load_movies(Path(path_str))


def _render_kpis(metrics: SummaryMetrics) -> None:
    """Render the summary metrics (KPI) panel.

    Parameters
    ----------
    metrics : SummaryMetrics
        Computed summary metrics.

    Returns
    -------
    None
    """
    st.subheader("Métricas resumen")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total de películas", f"{metrics.total_movies:,}")
    col2.metric("Presupuesto promedio", f"${metrics.avg_budget:,.0f}")
    col3.metric("Ingreso promedio", f"${metrics.avg_revenue:,.0f}")
    col4.metric("Duración media (min)", f"{metrics.avg_runtime:,.0f}")
    col5.metric("Rango de años", f"{metrics.min_year} - {metrics.max_year}")


def _render_distributions(frame: pd.DataFrame) -> None:
    """Render the distribution histograms for the key numeric variables.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset.

    Returns
    -------
    None
    """
    st.subheader("Distribuciones")
    specs = [
        ("vote_average", "Distribución de calificación", "Calificación promedio"),
        ("runtime", "Distribución de duración", "Duración (min)"),
        ("budget", "Distribución de presupuesto", "Presupuesto"),
        ("revenue", "Distribución de ingresos", "Ingresos"),
    ]
    left, right = st.columns(2)
    for index, (column, title, x_label) in enumerate(specs):
        series = distribution_series(frame, column)
        target = left if index % 2 == 0 else right
        if series.empty:
            target.info(f"No hay datos disponibles para '{column}'.")
        else:
            target.plotly_chart(
                charts.histogram_figure(series, title, x_label),
                use_container_width=True,
            )


def _render_categorical(frame: pd.DataFrame, top_n: int) -> None:
    """Render the Top-N genre and language ranking charts.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset.
    top_n : int
        Number of categories to display in each ranking.

    Returns
    -------
    None
    """
    st.subheader("Rankings de categorías")
    left, right = st.columns(2)
    genres = top_genres(frame, top_n)
    left.plotly_chart(
        charts.bar_figure(genres, x="count", y="genre", title=f"Top {top_n} géneros"),
        use_container_width=True,
    )
    languages = top_languages(frame, top_n)
    right.plotly_chart(
        charts.bar_figure(languages, x="count", y="language", title=f"Top {top_n} idiomas"),
        use_container_width=True,
    )


def _render_movies_per_year(frame: pd.DataFrame, year_range: tuple[int, int]) -> None:
    """Render the movies-per-year line chart for a year range.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset.
    year_range : tuple of int
        Inclusive ``(start_year, end_year)`` range.

    Returns
    -------
    None
    """
    st.subheader("Evolución temporal")
    yearly = movies_per_year(frame, year_range)
    if yearly.empty:
        st.info("No hay datos disponibles para el rango de años seleccionado.")
    else:
        st.plotly_chart(
            charts.line_figure(yearly, x="year", y="count", title="Películas por año"),
            use_container_width=True,
        )


def _render_scatter(frame: pd.DataFrame) -> None:
    """Render a scatter chart relating budget and revenue.

    Parameters
    ----------
    frame : pandas.DataFrame
        Cleaned dataset.

    Returns
    -------
    None
    """
    st.subheader("Relación entre variables")
    scatter_data = frame[["budget", "revenue"]].dropna()
    if scatter_data.empty:
        st.info("No hay datos suficientes para la relación presupuesto vs. ingresos.")
    else:
        st.plotly_chart(
            charts.scatter_figure(
                scatter_data,
                x="budget",
                y="revenue",
                title="Presupuesto vs. Ingresos",
                x_label="Presupuesto",
                y_label="Ingresos",
            ),
            use_container_width=True,
        )


def _render_data_quality(raw_frame: pd.DataFrame) -> None:
    """Render the data quality panel (nulls and zeros per column).

    Parameters
    ----------
    raw_frame : pandas.DataFrame
        Raw dataset, so sentinel zeros are still visible.

    Returns
    -------
    None
    """
    st.subheader("Calidad de datos")
    quality = compute_data_quality(raw_frame)
    st.dataframe(quality, use_container_width=True, hide_index=True)


def main() -> None:
    """Render the Movies EDA overview page.

    Returns
    -------
    None
    """
    st.set_page_config(page_title="Movies EDA Dashboard", layout="wide")
    st.title("Movies EDA Dashboard")
    st.caption("Análisis exploratorio del dataset de películas")

    csv_path = get_csv_path()
    try:
        raw_frame = _load_raw(str(csv_path))
        frame = clean_movies(raw_frame)
    except FileNotFoundError:
        logger.error("Dataset not found at %s", csv_path)
        st.error(
            f"No se encontró el archivo de datos en: {csv_path}. "
            "Configure la variable de entorno MOVIES_CSV_PATH o coloque movies.csv "
            "en la raíz del proyecto."
        )
        return
    except MissingColumnsError as error:
        logger.error("Dataset is missing required columns: %s", error)
        st.error(f"El dataset no tiene las columnas requeridas: {error}")
        return

    metrics = compute_summary_metrics(frame)

    st.sidebar.header("Controles")
    with st.sidebar:
        top_n = controls.top_n_control()
        year_range = controls.year_range_control(metrics.min_year, metrics.max_year)

    _render_kpis(metrics)
    st.divider()
    _render_distributions(frame)
    st.divider()
    _render_categorical(frame, top_n)
    st.divider()
    _render_movies_per_year(frame, year_range)
    st.divider()
    _render_scatter(frame)
    st.divider()
    _render_data_quality(raw_frame)


if __name__ == "__main__":
    main()
