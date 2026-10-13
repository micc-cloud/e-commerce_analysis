"""Reusable, business-readable matplotlib visualisations for Phase 2 EDA."""

from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd


def apply_business_style() -> None:
    """Apply a restrained style shared by notebook charts."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({"figure.figsize": (10, 5), "axes.titlesize": 13, "axes.labelsize": 10})


def _finish(ax: plt.Axes, title: str, xlabel: str, ylabel: str) -> plt.Axes:
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", labelrotation=35)
    return ax


def plot_missingness(missing: pd.Series, title: str = "Missing values by field") -> plt.Axes:
    values = missing[missing > 0].sort_values(ascending=True)
    ax = values.plot.barh(color="#486581")
    return _finish(ax, title, "Missing cell count", "Field")


def plot_distribution(series: pd.Series, title: str, xlabel: str, bins: int = 40) -> plt.Axes:
    ax = series.dropna().plot.hist(bins=bins, color="#2f6690", edgecolor="white")
    return _finish(ax, title, xlabel, "Rows")


def plot_top_categories(series: pd.Series, title: str, xlabel: str, top_n: int = 10) -> plt.Axes:
    counts = series.dropna().astype(str).value_counts().head(top_n).sort_values()
    ax = counts.plot.barh(color="#3a7d44")
    return _finish(ax, title, "Row count", xlabel)


def plot_monthly_trend(monthly: pd.Series, title: str, ylabel: str) -> plt.Axes:
    values = monthly.copy()
    values.index = values.index.astype(str)
    ax = values.plot.line(marker="o", color="#d1495b")
    return _finish(ax, title, "Month", ylabel)


def plot_status_mix(status_counts: pd.Series, title: str = "Order-line status mix") -> plt.Axes:
    counts = status_counts.sort_values()
    ax = counts.plot.barh(color="#7b2cbf")
    return _finish(ax, title, "Row count", "Status")


def plot_boxplot(series: pd.Series, title: str, ylabel: str) -> plt.Axes:
    ax = series.dropna().plot.box(color="#2f6690")
    return _finish(ax, title, "", ylabel)


def plot_grouped_comparison(frame: pd.DataFrame, title: str, xlabel: str, ylabel: str, columns: Iterable[str]) -> plt.Axes:
    ax = frame[list(columns)].plot.bar(color=["#2f6690", "#d1495b"])
    return _finish(ax, title, xlabel, ylabel)
