# sentiment-app 1.0.0

Application de classification d’avis français : modèle, API FastAPI /v1 protégée,
Streamlit (avis/CSV, graphiques/export), client HTML /web et roue autonome.

Installation du livrable et lancement complet : [README-PAQUET.md](README-PAQUET.md).

## Développement (Python 3.11)

```powershell
py -3.11 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-app.txt -r requirements-dev.txt
.venv/Scripts/python.exe src/make_demo.py
.venv/Scripts/python.exe src/train.py
New-Item -ItemType Directory -Force src/sentiment_app/modele
Copy-Item models/sentiment.joblib src/sentiment_app/modele/
.venv/Scripts/python.exe -m pip install -e .
.venv/Scripts/python.exe -m pytest -q --cov=api --cov-fail-under=95
.venv/Scripts/python.exe -m ruff check .
.venv/Scripts/python.exe -m mypy api
.venv/Scripts/python.exe -m build
.venv/Scripts/python.exe scripts/verifier_livrable.py
```

Le rapport de vérification installe la roue dans un venv neuf hors du dépôt, puis teste
la commande, l’API, les rôles et Streamlit/CSV/export. Les tests du paquet installé sont
ignorés dans le mode éditable et sont obligatoires dans cette vérification isolée.
Le modèle et .env ne sont pas suivis dans Git ; metrics.json est versionné.
Les ressources avancées du semestre restent dans requirements.txt ; requirements-app.txt
suffit à cette application. Aucun besoin de Docker pour exécuter le livrable.

Les rapports sont dans docs/semaine3.md à semaine5.md. Le jeu d’or est une proposition
assistée à valider par le groupe, avec une erreur connue explicitement conservée.
La configuration CI est locale jusqu’au prochain push ; aucune publication distante n’est revendiquée.

## Membres du binôme

| Rôle | Nom | Identifiant GitHub | Travail de la semaine 1 |
| --- | --- | --- | --- |
| Membre A | KABIL Mohamed | @Mohamed-Kabil | |
| Membre B | ELGHARBAOUI Youssef| @YoussefElGharbaouiDevs | |
| Membre C | ELWAFI Ahmed Ziad | @elwafiZiad | Préparation de l’environnement Python 3.11, installation des dépendances et validation des 38 tests du TP1. |
