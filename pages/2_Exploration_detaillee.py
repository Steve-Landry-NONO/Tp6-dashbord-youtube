"""Second Streamlit page — detailed exploration and data export."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils import BLUE, GREY, YOUTUBE_RED, clean_figure, load_data, page_footer, sidebar_filters


st.set_page_config(page_title="Exploration détaillée", page_icon="🔎", layout="wide")

df = load_data()
filtered = sidebar_filters(df, key_prefix="detail")

st.title("🔎 Explorer les signaux derrière le message")
st.write(
    "Cette page permet de vérifier si les constats restent valables lorsque le périmètre "
    "change. Les filtres agissent sur les graphiques et sur le fichier exportable."
)

if filtered.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()

metric = st.radio(
    "Indicateur à suivre",
    ["Nombre de vidéos", "Vues médianes", "Engagement médian"],
    horizontal=True,
)
filtered["mois"] = filtered["first_trending_date"].dt.to_period("M").dt.to_timestamp()
monthly = (
    filtered.groupby("mois", as_index=False)
    .agg(
        videos=("video_id", "nunique"),
        vues_medianes=("views", "median"),
        engagement_median=("engagement_rate", "median"),
    )
)

metric_map = {
    "Nombre de vidéos": ("videos", "Vidéos distinctes"),
    "Vues médianes": ("vues_medianes", "Vues médianes"),
    "Engagement médian": ("engagement_median", "Réactions pour 100 vues"),
}
column, axis_title = metric_map[metric]
fig = px.line(
    monthly,
    x="mois",
    y=column,
    markers=True,
    labels={"mois": "Mois de première apparition", column: axis_title},
)
fig.update_traces(line_color=YOUTUBE_RED, line_width=3, marker_size=8)
clean_figure(fig, height=430)
st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

left, right = st.columns([1.3, 1])
with left:
    st.subheader("Comparaison des catégories")
    ranking = (
        filtered.groupby("category", as_index=False)
        .agg(
            videos=("video_id", "nunique"),
            vues_medianes=("views", "median"),
            engagement_median=("engagement_rate", "median"),
            duree_mediane=("trend_days", "median"),
        )
        .sort_values(column, ascending=False)
    )
    bar = px.bar(
        ranking.head(10).sort_values(column),
        x=column,
        y="category",
        orientation="h",
        labels={column: axis_title, "category": ""},
        color_discrete_sequence=[BLUE],
    )
    clean_figure(bar, height=480)
    st.plotly_chart(bar, width="stretch", config={"displayModeBar": False})

with right:
    st.subheader("Top vidéos du périmètre")
    top_videos = (
        filtered.sort_values("views", ascending=False)
        .drop_duplicates("video_id")
        .loc[:, ["title", "channel_title", "country", "category", "views", "engagement_rate"]]
        .head(12)
    )
    st.dataframe(
        top_videos,
        width="stretch",
        hide_index=True,
        column_config={
            "title": "Vidéo",
            "channel_title": "Chaîne",
            "country": "Pays",
            "category": "Catégorie",
            "views": st.column_config.NumberColumn("Vues", format="%d"),
            "engagement_rate": st.column_config.NumberColumn("Réactions / 100 vues", format="%.2f"),
        },
    )

st.download_button(
    "Télécharger le périmètre filtré (.csv)",
    data=filtered.drop(columns=["mois"]).to_csv(index=False).encode("utf-8"),
    file_name="youtube_perimetre_filtre.csv",
    mime="text/csv",
)

st.caption(
    "Lecture : une évolution mensuelle reflète la composition des vidéos qui entrent en tendance, "
    "pas l’activité totale de YouTube."
)
page_footer()
