"""Plotly chart builders for the Movies EDA dashboard presentation layer.

These functions turn logic-layer outputs (series and frames) into Plotly
figures. They contain no business logic.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def histogram_figure(series: pd.Series, title: str, x_label: str) -> go.Figure:
    """Build a histogram figure for a numeric distribution.

    Parameters
    ----------
    series : pandas.Series
        Non-missing numeric values to plot.
    title : str
        Chart title.
    x_label : str
        Label for the x axis.

    Returns
    -------
    plotly.graph_objects.Figure
        The histogram figure.
    """
    fig = px.histogram(series, nbins=40, title=title)
    fig.update_layout(xaxis_title=x_label, yaxis_title="Cantidad", showlegend=False)
    return fig


def bar_figure(frame: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    """Build a horizontal bar figure for a Top-N ranking.

    Parameters
    ----------
    frame : pandas.DataFrame
        Data with the category and count columns.
    x : str
        Column with the count (numeric) values.
    y : str
        Column with the category labels.
    title : str
        Chart title.

    Returns
    -------
    plotly.graph_objects.Figure
        The bar figure, sorted with the largest category on top.
    """
    fig = px.bar(frame, x=x, y=y, orientation="h", title=title)
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def line_figure(frame: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    """Build a line figure for a time series (e.g. movies per year).

    Parameters
    ----------
    frame : pandas.DataFrame
        Data with the x (year) and y (count) columns.
    x : str
        Column for the x axis.
    y : str
        Column for the y axis.
    title : str
        Chart title.

    Returns
    -------
    plotly.graph_objects.Figure
        The line figure.
    """
    fig = px.line(frame, x=x, y=y, markers=True, title=title)
    fig.update_layout(xaxis_title="Año", yaxis_title="Cantidad")
    return fig


def scatter_figure(
    frame: pd.DataFrame, x: str, y: str, title: str, x_label: str, y_label: str
) -> go.Figure:
    """Build a scatter figure relating two numeric variables.

    Parameters
    ----------
    frame : pandas.DataFrame
        Data with the two numeric columns to relate.
    x : str
        Column for the x axis.
    y : str
        Column for the y axis.
    title : str
        Chart title.
    x_label : str
        Label for the x axis.
    y_label : str
        Label for the y axis.

    Returns
    -------
    plotly.graph_objects.Figure
        The scatter figure.
    """
    fig = px.scatter(frame, x=x, y=y, opacity=0.6, title=title)
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    return fig
