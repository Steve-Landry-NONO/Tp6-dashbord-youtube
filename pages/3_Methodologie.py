"""Third Streamlit page — methods, definitions and limitations."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from utils import inject_global_styles, page_footer


st.set_page_config(page_title="Méthodologie", page_icon="🧭", layout="wide")
inject_global_styles()

metadata_path = Path(__file__).resolve().parents[1] / "data" / "metadata.json"
metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

st.title("🧭 Méthodologie et limites")
st.markdown(
    """
    Le dashboard répond à une question de décision : **comment adapter une stratégie de contenu
    à la brièveté des tendances, au type de contenu et au marché ciblé ?**

    ### Unités d’analyse

    - **Durée et pays** : un couple *pays + vidéo* ; une vidéo présente dans deux pays compte donc deux fois.
    - **Mégasuccès et engagement** : une vidéo mondiale distincte ; on conserve l’observation ayant le plus de vues dans le périmètre filtré.
    - **Audience** : maximum de vues observé pendant la période de présence en tendance, et non vues à date aujourd’hui.

    ### Définitions

    - **Tendance d’un jour** : une seule date de tendance distincte pour le couple pays + vidéo.
    - **Mégasuccès** : vidéo située dans le premier centile des vues du périmètre sélectionné.
    - **Engagement** : `(likes + commentaires) / vues × 100`, soit les réactions pour 100 vues.
    - Les observations où les commentaires ou évaluations sont désactivés sont exclues du calcul d’engagement.

    ### Choix graphiques

    - Barre empilée à 100 % pour lire une composition.
    - Barres horizontales avec base zéro pour comparer des pays.
    - Nuage de points pour confronter portée et engagement sans suggérer une causalité.
    - Une couleur rouge sert de canal pré-attentif pour le constat principal ; les éléments de contexte restent neutres.

    ### Limites à annoncer au jury

    1. Les données couvrent uniquement novembre 2017 à juin 2018.
    2. Le fichier contient des vidéos déjà entrées en tendance : il ne décrit pas tout YouTube.
    3. Les écarts entre pays sont descriptifs et ne prouvent aucune causalité nationale.
    4. Les vues et réactions évoluent pendant la période de tendance ; l’analyse retient le maximum observé.
    5. Une corrélation entre portée et engagement ne signifie pas que l’un provoque l’autre.
    """
)

c1, c2, c3 = st.columns(3)
c1.metric("Lignes sources", f"{metadata['raw_rows']:,}".replace(",", " "))
c2.metric("Vidéos distinctes", f"{metadata['unique_videos']:,}".replace(",", " "))
c3.metric("Couples pays–vidéo", f"{metadata['country_video_rows']:,}".replace(",", " "))

with st.expander("Traçabilité de la source"):
    st.write(metadata["source"])
    st.write(f"Période : {metadata['period_start']} au {metadata['period_end']}")
    st.link_button("Consulter la source Kaggle", metadata["source_url"])

st.info(
    "Usage de l’IA : l’équipe a utilisé une assistance IA pour structurer et relire le code. "
    "Les membres doivent pouvoir expliquer les filtres, les agrégations, les KPIs et chaque graphique."
)

page_footer()
