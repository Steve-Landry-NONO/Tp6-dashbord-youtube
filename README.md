# TP6 — Dashboard interactif Streamlit

## Membres du groupe

- Steve Landry KOUOKAM NONO
- Stephane DOMI
- Chantal CAMARA
- Maeva QUENUM

## Application en ligne

▶️ **[Ouvrir le dashboard Streamlit](https://tp6-dashbord-youtube-ghmbt4sv7joo5kbcy6t6f3.streamlit.app/)**

Dépôt source : [Steve-Landry-NONO/Tp6-dashbord-youtube](https://github.com/Steve-Landry-NONO/Tp6-dashbord-youtube)

## Message du projet

Les tendances YouTube sont brèves, dominées par la musique et très inégales selon les marchés : la stratégie de contenu doit donc être rapide, adaptée à l’objectif et localisée.

## Contenu du rendu

- `app.py` : page principale, quatre onglets narratifs et filtres.
- `pages/2_Exploration_detaillee.py` : vue exploratoire réactive et export CSV.
- `pages/3_Methodologie.py` : définitions, choix et limites.
- `utils.py` : chargement avec `@st.cache_data`, filtres et formatage.
- `data/youtube_prepared.csv.gz` : données utilisées.
- `data/metadata.json` : traçabilité de la préparation.
- `cadrage.md` : cadrage écrit d’une page.
- `pitch.md` : conducteur de soutenance.
- `.streamlit/config.toml` : thème fourni en cours.
- `requirements.txt` : dépendances de déploiement.
- `LIEN_STREAMLIT.txt` : lien public de l’application déployée.

## Lancer en local

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Déploiement

L’application est déployée sur Streamlit Community Cloud :

- **Application :** https://tp6-dashbord-youtube-ghmbt4sv7joo5kbcy6t6f3.streamlit.app/
- **Dépôt GitHub :** https://github.com/Steve-Landry-NONO/Tp6-dashbord-youtube

Le CSV compressé reste sous la limite de GitHub et accélère le chargement de l’application.
