"""Shared data loading, filtering and formatting helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "data" / "youtube_prepared.csv.gz"

YOUTUBE_RED = "#FF0033"
NAVY = "#18212F"
BLUE = "#2F6BFF"
GREY = "#A9B0BB"
LIGHT_GREY = "#E9EDF3"
GREEN = "#00A878"


@st.cache_data(show_spinner="Chargement des données YouTube…")
def load_data(path: str = str(DATA_PATH)) -> pd.DataFrame:
    """Load the prepared country-video table once per Streamlit session."""
    frame = pd.read_csv(
        path,
        compression="gzip",
        parse_dates=["first_trending_date", "last_trending_date"],
    )
    frame["category"] = frame["category"].fillna("Autre")
    return frame


def sidebar_filters(df: pd.DataFrame, key_prefix: str = "main") -> pd.DataFrame:
    """Render three filters and return the matching analytical perimeter."""
    st.sidebar.header("Périmètre de l’analyse")
    countries = sorted(df["country"].dropna().unique().tolist())
    categories = sorted(df["category"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Pays",
        countries,
        default=countries,
        key=f"{key_prefix}_countries",
    )
    selected_categories = st.sidebar.multiselect(
        "Catégories",
        categories,
        default=categories,
        key=f"{key_prefix}_categories",
    )
    min_date = df["first_trending_date"].min().date()
    max_date = df["first_trending_date"].max().date()
    selected_dates = st.sidebar.date_input(
        "Première apparition en tendance",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key=f"{key_prefix}_dates",
    )
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = end_date = selected_dates[0] if isinstance(selected_dates, tuple) else selected_dates

    filtered = df[
        df["country"].isin(selected_countries)
        & df["category"].isin(selected_categories)
        & df["first_trending_date"].dt.date.between(start_date, end_date)
    ].copy()
    st.sidebar.caption(
        f"{len(filtered):,} couples pays–vidéo retenus".replace(",", " ")
    )
    return filtered


def global_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    """Keep, for each video, the selected-country observation with most views."""
    if df.empty:
        return df.copy()
    return df.loc[df.groupby("video_id")["views"].idxmax()].copy()


def format_integer(value: float | int) -> str:
    return f"{value:,.0f}".replace(",", " ")


def format_pct(value: float) -> str:
    return f"{value:.1f} %".replace(".", ",")


def clean_figure(fig, *, height: int = 440):
    """Apply a restrained visual system shared by every Plotly chart."""
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=45, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial", color=NAVY),
        hoverlabel=dict(bgcolor="white", font_color=NAVY),
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(24,33,47,0.10)", zeroline=False)
    return fig


def page_footer() -> None:
    st.divider()
    st.caption(
        "Source : YouTube Trending Videos (Kaggle), 14/11/2017–14/06/2018. "
        "Une ligne préparée = un couple pays + vidéo ; l’audience correspond au maximum observé."
    )

