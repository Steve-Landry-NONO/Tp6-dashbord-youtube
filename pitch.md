# Conducteur de pitch — 5 minutes

**Équipe :** Steve Landry KOUOKAM NONO · Stephane DOMI · Chantal CAMARA · Maeva QUENUM · Ludovic TUEKAM

## 0:00–0:45 · Chantal CAMARA — problème et message

« Nous avons analysé 161 470 instantanés de tendances YouTube issus de quatre pays. Notre conclusion est simple : la tendance est courte, la musique domine les mégasuccès et l’échelle d’audience change fortement selon le marché. Notre dashboard aide un responsable éditorial à décider quand promouvoir, quel KPI suivre et où fixer ses objectifs. »

Montrer le titre et les trois KPI de périmètre. Préciser que les filtres de gauche modifient toute l’analyse.

## 0:45–1:45 · Stephane DOMI — durée et fenêtre d’action

Ouvrir l’onglet **Durée**. Montrer qu’environ 59,5 % des couples pays + vidéo ne restent qu’un jour en tendance sur le périmètre complet.

Décision : concentrer la promotion dans les 24 premières heures et réévaluer vite les contenus qui ne décollent pas. Modifier un filtre de pays pour démontrer l’interactivité.

## 1:45–2:40 · Maeva QUENUM — mégasuccès et objectif de portée

Ouvrir **Mégasuccès**. Expliquer la définition du top 1 % et comparer la part de la musique dans l’ensemble avec sa part parmi les vidéos les plus vues.

Décision : la musique est un levier de portée, mais ce constat ne suffit pas à conclure sur l’engagement.

## 2:40–3:40 · Steve Landry KOUOKAM NONO — portée contre engagement

Ouvrir **Engagement**. Présenter le nuage de points : chaque bulle représente une catégorie ; l’axe horizontal porte les vues médianes et l’axe vertical les réactions pour 100 vues.

Décision : pour la notoriété, suivre la portée ; pour la communauté, suivre l’engagement normalisé. Insister sur l’absence de causalité.

## 3:40–4:25 · Ludovic TUEKAM — comparaison par pays

Ouvrir **Pays**. Montrer l’écart entre le Royaume-Uni et la France sur le périmètre complet.

Décision : ne pas imposer une cible globale unique ; définir des références, budgets et attentes par marché.

## 4:25–5:00 · Conclusion et justification de conception

« Nous avons limité chaque vue à trois KPI, utilisé des titres-conclusions et une seule couleur d’accent pour réduire la charge cognitive. Les barres partent de zéro, les filtres sont globaux et le chargement est mis en cache. La page Méthodologie rend nos définitions et limites explicites. »

Terminer par les trois actions : agir en 24 h, aligner le KPI sur l’objectif, localiser les cibles.

## Questions probables

- **Pourquoi la médiane ?** Les vues sont très asymétriques ; la médiane résiste mieux aux vidéos exceptionnellement virales.
- **Pourquoi une vidéo peut-elle compter plusieurs fois ?** Pour la durée et les pays, l’unité pertinente est le couple pays + vidéo. Pour l’analyse mondiale, elle est dédupliquée par `video_id`.
- **Comment est calculé l’engagement ?** `(likes + commentaires) / vues × 100`, hors évaluations ou commentaires désactivés.
- **Quelle limite principale ?** Les données sont historiques et ne contiennent que des vidéos déjà en tendance.
