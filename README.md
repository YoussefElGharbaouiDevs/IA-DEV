# sentiment-app : dépôt du binôme

Application fil rouge du cours *Développement et déploiement d'applications intelligentes*.
Ce dépôt grandit chaque semaine ; la semaine 1 met en place le cadrage et l'environnement.

## Installation (3 commandes)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Vérifier son installation

```bash
python scripts/check_setup.py    # diagnostic lisible : versions, dossiers, Git
pytest -q                        # mêmes vérifications sous forme de tests
```

La démarche complète de test, étape par étape, est dans `TESTS.md`.

## Structure

```text
sentiment-app/
├── README.md
├── TP1-ENONCE.md    # énoncé du TP de la semaine 1
├── TESTS.md         # démarche à suivre pour le test
├── requirements.txt
├── .gitignore
├── data/            # jeux de données (versionnés par DVC à partir de la semaine 7)
├── models/          # modèles entraînés (jamais dans Git)
├── app/             # API FastAPI (semaine 3)
├── ui/              # Streamlit (semaine 5)
├── tests/           # pytest (semaine 1 : tests d'environnement)
├── scripts/         # utilitaires (check_setup, nouveau cas de cadrage)
└── docs/cadrage/    # fiches de cadrage du TP1
```

## Membres du binôme

| Rôle | Nom | Identifiant GitHub | Travail de la semaine 1 |
| --- | --- | --- | --- |
| Membre A | KABIL Mohamed | @Mohamed-Kabil | Fiches de cadrage rédigées dans le premier dépôt du groupe, reprises ici. |
| Membre B | ELGHARBAOUI Youssef | @YoussefElGharbaouiDevs | Préparation du premier dépôt du groupe. Contribution dans ce nouveau dépôt à réaliser. |
| Membre C | ELWAFI Ahmed Ziad | @elwafiZiad | Reprise du kit vierge dans 5IADO-tp2, préparation de Python 3.11 et vérification des contrôles. |

## Reprise du TP1 puis TP2

Ce dossier provient de l’archive `sentiment-app.zip` du cours. Conformément à la consigne du professeur, le groupe reprend le TP1 dans un nouveau dossier avant d’appliquer le kit TP2. Les fiches de cadrage sont reprises du travail du groupe dans `YoussefElGharbaouiDevs/IA-DEV`.

Sous Windows, les commandes peuvent être exécutées directement avec `.\.venv\Scripts\python.exe`, sans modifier la politique PowerShell. Python 3.11.15 est utilisé ; NumPy 1.26.4 est retenu pour conserver l’environnement déjà validé par le groupe. Le journal est dans `docs/journal-tp1-tp6.md` et les sorties réelles dans `docs/preuves/`.

Les dépendances utilisées aux TP1 et TP2 sont installées. Les autres bibliothèques de `requirements.txt` seront ajoutées avant les TP qui les utilisent.
