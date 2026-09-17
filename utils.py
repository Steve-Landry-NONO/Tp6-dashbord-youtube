"""Shared data loading, filtering and formatting helpers."""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "data" / "youtube_prepared.csv.gz"

YOUTUBE_RED = "#E62117"
NAVY = "#172033"
BLUE = "#2457C5"
GREY = "#8792A2"
LIGHT_GREY = "#E7EAF0"

GROUP_MEMBERS = (
    "Steve Landry KOUOKAM NONO",
    "Stephane DOMI",
    "Chantal CAMARA",
    "Maeva QUENUM",
    "Ludovic TUEKAM",
)


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
    st.sidebar.markdown("### Filtres")
    st.sidebar.caption("Les graphiques et les KPI se mettent à jour automatiquement.")
    countries = sorted(df["country"].dropna().unique().tolist())
    categories = sorted(df["category"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Pays",
        countries,
        default=countries,
        key=f"{key_prefix}_countries",
    )
    selected_categories = st.sidebar.multiselect(
        "Catégories à isoler",
        categories,
        default=[],
        placeholder="Toutes les catégories",
        help="Laissez vide pour conserver toutes les catégories.",
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

    active_categories = selected_categories or categories
    filtered = df[
        df["country"].isin(selected_countries)
        & df["category"].isin(active_categories)
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
        template="plotly_white",
        height=height,
        margin=dict(l=20, r=20, t=45, b=20),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color=NAVY, size=13),
        hoverlabel=dict(bgcolor="white", font_color=NAVY),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(color=NAVY),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        tickfont=dict(color=NAVY),
        title_font=dict(color=NAVY),
        linecolor="#D9DEE7",
    )
    fig.update_yaxes(
        gridcolor="#E9EDF3",
        zeroline=False,
        tickfont=dict(color=NAVY),
        title_font=dict(color=NAVY),
    )
    return fig


def inject_global_styles() -> None:
    """Apply the same accessible hierarchy to every page."""
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1440px;
            padding-top: 1.6rem;
            padding-bottom: 2.5rem;
        }
        h1, h2, h3 {
            color: #172033 !important;
            letter-spacing: -0.02em;
        }
        p, li, label, [data-testid="stCaptionContainer"] {
            color: #465267;
        }
        [data-testid="stSidebar"] {
            background: #F6F7F9;
            border-right: 1px solid #E0E4EA;
        }
        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #DDE2EA;
            border-radius: 12px;
            padding: 0.9rem 1.05rem;
            box-shadow: 0 1px 2px rgba(23, 32, 51, 0.04);
        }
        [data-testid="stMetricLabel"] p {
            color: #596579 !important;
            font-size: 0.9rem;
            font-weight: 600;
        }
        [data-testid="stMetricValue"] {
            color: #172033 !important;
        }
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        [data-testid="stMetricDelta"] > div {
            color: #596579 !important;
        }
        button[data-baseweb="tab"] {
            color: #596579;
            font-weight: 600;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #C81E1E;
        }
        .decision-callout {
            margin-top: 0.65rem;
            padding: 0.9rem 1rem;
            background: #FFF7F6;
            border-left: 4px solid #E62117;
            border-radius: 6px;
            color: #293348;
            line-height: 1.45;
        }
        .decision-callout strong {
            color: #B42318;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def decision_callout(message: str) -> None:
    """Highlight the action without relying on green success styling."""
    st.markdown(
        f'<div class="decision-callout"><strong>Décision</strong> — {escape(message)}</div>',
        unsafe_allow_html=True,
    )


def team_byline() -> None:
    """Display the complete project team consistently on every page."""
    st.caption("Équipe du projet : " + " · ".join(GROUP_MEMBERS))


def page_footer() -> None:
    st.divider()
    st.caption(
        "Source : YouTube Trending Videos (Kaggle), 14/11/2017–14/06/2018. "
        "Une ligne préparée = un couple pays + vidéo ; l’audience correspond au maximum observé."
    )
