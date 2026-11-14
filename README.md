# sentiment-app : dépôt du trinôme

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

## Membres du trinôme

| Rôle | Nom | Identifiant GitHub | Travail de la semaine 1 |
| --- | --- | --- | --- |
| Membre A | KABIL Mohamed | @Mohamed-Kabil | Fiches de cadrage rédigées dans le premier dépôt du groupe, reprises ici. |
| Membre B | ELGHARBAOUI Youssef | @YoussefElGharbaouiDevs | Préparation du premier dépôt du groupe. Contribution dans ce nouveau dépôt à réaliser. |
| Membre C | ELWAFI Ahmed Ziad | @elwafiZiad | Reprise du kit vierge dans 5IADO-tp2, préparation de Python 3.11 et vérification des contrôles. |

## Reprise du TP1 puis TP2

Ce dossier provient de l’archive `sentiment-app.zip` du cours. Conformément à la consigne du professeur, le groupe reprend le TP1 dans un nouveau dossier avant d’appliquer le kit TP2. Les fiches de cadrage sont reprises du travail du groupe dans `YoussefElGharbaouiDevs/IA-DEV`.

Sous Windows, les commandes peuvent être exécutées directement avec `.\.venv\Scripts\python.exe`, sans modifier la politique PowerShell. Python 3.11.15 est utilisé ; NumPy 1.26.4 est retenu pour conserver l’environnement déjà validé par le groupe. Le journal est dans `docs/journal-tp1-tp6.md` et les sorties réelles dans `docs/preuves/`.

Toutes les dépendances de `requirements.txt` sont installées dans le venv Python 3.11.15. Le contrôle `uv pip check` ne signale aucun conflit ; les versions effectivement installées sont consignées dans `requirements.lock`.

## Rejouer le rendu

Avec Python 3.11, depuis la racine du dépôt sous PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-tp.txt
.\.venv\Scripts\python.exe scripts/configurer_env.py
.\.venv\Scripts\python.exe src/make_demo.py
.\.venv\Scripts\python.exe src/train.py
```

Lancez l’API et l’interface dans deux terminaux distincts.

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --port 8000
```

```powershell
.\.venv\Scripts\python.exe -m streamlit run ui/app.py
```

Ouvrez http://127.0.0.1:8501 et importez `data/avis_exemple.csv`. La documentation de l’API est à http://127.0.0.1:8000/docs. Pour le client web, lancez `python -m http.server 5500 --directory web` et saisissez la valeur de `API_KEY` de votre fichier local `.env` dans la page.

```powershell
.\.venv\Scripts\python.exe -m pytest -q --cov=api --cov-fail-under=95
node --test web/client.test.mjs
mvn -f java/avis-service/pom.xml package
```

Pour lancer le service Java avec JDK 21, définissez `SENTIMENT_API_KEY` à la valeur locale de `API_KEY`, puis lancez `java -jar java/avis-service/target/avis-service-1.0.0.jar`. Le service expose `POST /avis` sur le port 8080 et transmet le champ JSON `text` à l’API.

Le [compte rendu](docs/compte-rendu.md) contient les observations et la capture Streamlit. Le [guide du paquet](README-PAQUET.md) donne les commandes d’installation et d’utilisation.

Pour reconstruire les archives dans un dossier `dist/` vide :

```powershell
New-Item -ItemType Directory -Force src/sentiment_app/modele
Copy-Item models/sentiment.joblib src/sentiment_app/modele/
.\.venv\Scripts\python.exe -m build
.\.venv\Scripts\python.exe scripts/verifier_livrable.py
```
