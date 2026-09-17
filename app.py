"""TP6 — dashboard Streamlit interactif sur les tendances YouTube."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import (
    BLUE,
    GREEN,
    GREY,
    LIGHT_GREY,
    NAVY,
    YOUTUBE_RED,
    clean_figure,
    format_integer,
    format_pct,
    global_snapshot,
    load_data,
    page_footer,
    sidebar_filters,
)


st.set_page_config(
    page_title="Anatomie des tendances YouTube",
    page_icon="▶️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {background:#F6F8FB; border:1px solid #E7EBF0; padding:14px; border-radius:10px;}
    h1, h2, h3 {color:#18212F;}
    </style>
    """,
    unsafe_allow_html=True,
)


def duration_tab(data: pd.DataFrame) -> None:
    st.subheader("Sur YouTube, la tendance ne dure souvent qu’un jour")
    bands = pd.cut(
        data["trend_days"],
        bins=[0, 1, 3, 6, float("inf")],
        labels=["1 jour", "2 à 3 jours", "4 à 6 jours", "7 jours ou plus"],
    )
    summary = bands.value_counts(sort=False).rename_axis("durée").reset_index(name="vidéos")
    summary["part"] = summary["vidéos"] / summary["vidéos"].sum() * 100
    one_day = float(summary.loc[summary["durée"].eq("1 jour"), "part"].iloc[0])
    seven_plus = float(summary.loc[summary["durée"].eq("7 jours ou plus"), "part"].iloc[0])
    median_days = float(data["trend_days"].median())

    c1, c2, c3 = st.columns(3)
    c1.metric("Tendances d’un seul jour", format_pct(one_day), help="Couples pays + vidéo")
    c2.metric("Durée médiane", f"{median_days:.0f} jour(s)")
    c3.metric("Présence ≥ 7 jours", format_pct(seven_plus))

    fig = go.Figure()
    colors = [YOUTUBE_RED, "#8590A2", "#B8C0CC", "#D9DEE6"]
    for row, color in zip(summary.itertuples(index=False), colors):
        fig.add_bar(
            y=["Vidéos en tendance"],
            x=[row.part],
            name=str(row.durée),
            orientation="h",
            marker_color=color,
            text=f"{row.part:.1f} %".replace(".", ","),
            textposition="inside",
            hovertemplate=f"{row.durée}<br>{row.vidéos:,} vidéos<br>{row.part:.1f} %<extra></extra>".replace(",", " "),
        )
    fig.update_layout(barmode="stack", xaxis=dict(range=[0, 100], title="Part des couples pays–vidéo (%)"))
    clean_figure(fig, height=330)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.success("Décision : concentrer la promotion dans les 24 premières heures, puis réallouer rapidement si la vidéo ne décolle pas.")


def music_tab(data: pd.DataFrame) -> None:
    st.subheader("La musique concentre l’essentiel des mégasuccès")
    global_data = global_snapshot(data)
    threshold = float(global_data["views"].quantile(0.99))
    top = global_data[global_data["views"].ge(threshold)]
    share_all = float(global_data["category"].eq("Musique").mean() * 100)
    share_top = float(top["category"].eq("Musique").mean() * 100) if len(top) else 0.0
    ratio = share_top / share_all if share_all else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Seuil du top 1 %", f"{format_integer(threshold)} vues")
    c2.metric("Musique dans le top 1 %", format_pct(share_top), delta=f"{share_top-share_all:+.1f} pts")
    c3.metric("Surreprésentation", f"× {ratio:.1f}".replace(".", ","))

    comparison = pd.DataFrame(
        {
            "Groupe": ["Toutes les vidéos", "Top 1 % des vues"],
            "Musique": [share_all, share_top],
        }
    )
    comparison["Autres catégories"] = 100 - comparison["Musique"]
    fig = go.Figure()
    fig.add_bar(
        y=comparison["Groupe"], x=comparison["Musique"], orientation="h",
        name="Musique", marker_color=YOUTUBE_RED,
        text=comparison["Musique"].map(lambda x: f"{x:.1f} %".replace(".", ",")), textposition="inside",
    )
    fig.add_bar(
        y=comparison["Groupe"], x=comparison["Autres catégories"], orientation="h",
        name="Autres catégories", marker_color=LIGHT_GREY,
        text=comparison["Autres catégories"].map(lambda x: f"{x:.1f} %".replace(".", ",")), textposition="inside",
    )
    fig.update_layout(barmode="stack", xaxis=dict(range=[0, 100], title="Composition (%)"))
    clean_figure(fig, height=350)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.success("Décision : pour maximiser la portée brute, prioriser les formats et collaborations musicales — sans confondre portée et engagement.")


def engagement_tab(data: pd.DataFrame) -> None:
    st.subheader("Les vidéos les plus vues ne sont pas celles qui font le plus réagir")
    global_data = global_snapshot(data)
    valid = global_data[
        ~global_data["comments_disabled"]
        & ~global_data["ratings_disabled"]
        & global_data["views"].gt(0)
    ].copy()
    by_category = (
        valid.groupby("category", as_index=False)
        .agg(
            vues_medianes=("views", "median"),
            engagement_median=("engagement_rate", "median"),
            videos=("video_id", "nunique"),
        )
        .sort_values("vues_medianes")
    )
    best_engagement = by_category.loc[by_category["engagement_median"].idxmax()]
    best_reach = by_category.loc[by_category["vues_medianes"].idxmax()]
    correlation = (
        float(by_category["vues_medianes"].corr(by_category["engagement_median"]))
        if len(by_category) > 1
        else None
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Engagement le plus élevé", str(best_engagement["category"]), format_pct(best_engagement["engagement_median"]))
    c2.metric("Audience médiane la plus forte", str(best_reach["category"]), f"{format_integer(best_reach['vues_medianes'])} vues")
    correlation_label = f"{correlation:.2f}".replace(".", ",") if correlation is not None else "n.d."
    c3.metric("Corrélation portée–engagement", correlation_label, help="Corrélation entre les médianes par catégorie ; nécessite au moins deux catégories")

    focus = {"Musique", "Tutoriels et style", "Jeux vidéo"}
    by_category["focus"] = by_category["category"].where(by_category["category"].isin(focus), "Autres")
    by_category["label"] = by_category["category"].where(by_category["category"].isin(focus), "")
    color_map = {"Musique": YOUTUBE_RED, "Tutoriels et style": GREEN, "Jeux vidéo": BLUE, "Autres": GREY}
    fig = px.scatter(
        by_category,
        x="vues_medianes",
        y="engagement_median",
        size="videos",
        color="focus",
        text="label",
        color_discrete_map=color_map,
        hover_name="category",
        custom_data=["videos"],
        labels={"vues_medianes": "Vues médianes", "engagement_median": "Réactions pour 100 vues"},
    )
    fig.update_traces(textposition="top center", hovertemplate="<b>%{hovertext}</b><br>Vues médianes : %{x:,.0f}<br>Réactions / 100 vues : %{y:.2f}<br>Vidéos : %{customdata[0]:,.0f}<extra></extra>")
    clean_figure(fig, height=510)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.success("Décision : choisir le KPI principal selon l’objectif — portée pour la notoriété, réactions pour la communauté.")


def country_tab(data: pd.DataFrame) -> None:
    st.subheader("L’échelle d’audience varie fortement selon le pays")
    by_country = (
        data.groupby("country", as_index=False)
        .agg(vues_medianes=("views", "median"), videos=("video_id", "nunique"))
        .sort_values("vues_medianes", ascending=True)
    )
    high = by_country.iloc[-1]
    low = by_country.iloc[0]
    ratio = float(high["vues_medianes"] / low["vues_medianes"]) if low["vues_medianes"] else 0.0
    overall = float(data["views"].median())

    c1, c2, c3 = st.columns(3)
    c1.metric("Marché au plus fort potentiel", str(high["country"]), f"{format_integer(high['vues_medianes'])} vues médianes")
    c2.metric("Écart entre extrêmes", f"× {ratio:.1f}".replace(".", ","))
    c3.metric("Médiane du périmètre", f"{format_integer(overall)} vues")

    colors = [YOUTUBE_RED if country == high["country"] else BLUE if country == low["country"] else GREY for country in by_country["country"]]
    fig = go.Figure(
        go.Bar(
            x=by_country["vues_medianes"],
            y=by_country["country"],
            orientation="h",
            marker_color=colors,
            text=by_country["vues_medianes"].map(format_integer),
            textposition="outside",
            customdata=by_country[["videos"]],
            hovertemplate="<b>%{y}</b><br>Vues médianes : %{x:,.0f}<br>Vidéos : %{customdata[0]:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(xaxis_title="Maximum de vues médian par vidéo", yaxis_title="")
    fig.update_xaxes(rangemode="tozero")
    clean_figure(fig, height=420)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.success("Décision : fixer des objectifs et budgets par marché ; une cible unique de vues serait trompeuse.")


df = load_data()
filtered = sidebar_filters(df)

st.title("▶ Anatomie d’une tendance YouTube")
st.markdown(
    "**Les tendances sont brèves, dominées par la musique et très inégales selon les marchés.** "
    "Ce dashboard transforme ces constats en décisions de contenu et de diffusion."
)

if filtered.empty:
    st.warning("Aucune donnée ne correspond aux filtres. Élargissez le périmètre dans la barre latérale.")
    st.stop()

global_filtered = global_snapshot(filtered)
k1, k2, k3 = st.columns(3)
k1.metric("Vidéos distinctes", format_integer(global_filtered["video_id"].nunique()))
k2.metric("Pays sélectionnés", str(filtered["country"].nunique()))
k3.metric("Vues médianes", format_integer(global_filtered["views"].median()))

tabs = st.tabs(["⏱ Durée", "🎵 Mégasuccès", "💬 Engagement", "🌍 Pays"])
with tabs[0]:
    duration_tab(filtered)
with tabs[1]:
    music_tab(filtered)
with tabs[2]:
    engagement_tab(filtered)
with tabs[3]:
    country_tab(filtered)

page_footer()
