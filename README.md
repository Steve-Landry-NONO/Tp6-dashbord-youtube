# TP6 — Dashboard interactif Streamlit

Groupe : Chantal CAMARA · Stéphane DOMI · Maeva QUENUM · Steve Landry KOUOKAM

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
- `LIEN_STREAMLIT.txt` : emplacement du lien public après publication.

## Lancer en local

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Déployer sur Streamlit Community Cloud

1. Créer un dépôt GitHub, par exemple `tp6-youtube-dashboard`.
2. Copier tout le contenu de ce dossier à la racine du dépôt, y compris `.streamlit/`, `pages/` et `data/`.
3. Envoyer les fichiers sur la branche `main`.
4. Ouvrir `https://share.streamlit.io/` et cliquer sur **Create app**.
5. Sélectionner le dépôt, la branche `main` et le fichier principal `app.py`.
6. Cliquer sur **Deploy** puis tester les filtres et les trois pages.
7. Copier l’URL publique dans `LIEN_STREAMLIT.txt` et dans le dossier Drive du rendu.

Le CSV compressé reste sous la limite de GitHub et accélère le chargement de l’application.

