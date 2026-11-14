# sentiment-app 1.0.0

Classifie un avis français en `positive` ou `negative`, avec un score de confiance.
Python 3.11 recommandé (minimum 3.11). Le modèle TF-IDF + régression logistique
est inclus dans la roue ; aucun dépôt, serveur, clé d'API ou entraînement requis.

## Installation depuis le fichier reçu

Dans un dossier vide, avec Python 3.11 et un accès Internet pour les dépendances :

```powershell
py -3.11 -m venv .venv
.venv/Scripts/python.exe -m pip install ./sentiment_app-1.0.0-py3-none-any.whl
.venv/Scripts/sentiment.exe --version
.venv/Scripts/sentiment.exe "Livraison rapide, très satisfait"
.venv/Scripts/sentiment.exe --json "Produit cassé, à fuir"
.venv/Scripts/python.exe -c "from sentiment_app import predict; print(predict('Produit conforme'))"
.venv/Scripts/python.exe -m pip check
```

Sur Linux/macOS : `python3.11 -m venv .venv`, puis remplacer `.venv/Scripts/`
par `.venv/bin/` et supprimer `.exe` dans les commandes.

Un texte vide renvoie `erreur : texte vide`, code 2, sans traceback.
Sans argument, la commande affiche l'aide. Pour désinstaller :
`python -m pip uninstall sentiment-app` dans l'environnement activé.
Ne pas renommer la roue. `SENTIMENT_MODELE` permet un remplacement explicite
par un fichier Joblib de confiance compatible ; normalement cette variable est absente.

## Limites

Modèle pédagogique sur 290 avis synthétiques, non validé pour une décision réelle.
Ironie, négation, avis mitigés et changement de domaine peuvent produire des erreurs.
Le score n'est pas une probabilité calibrée. L'API ajoute une abstention sous 0,60 ;
la fonction publique du paquet conserve le contrat binaire du manuel actuel.
Ce paquet suit le manuel du 14 novembre (1.0.0, modèle inclus), pas l'ancien
TP6 0.6.0 qui distribuait le modèle séparément.

## Application complète : API, navigateur et Streamlit

La roue installe aussi les paquets `api` et `ui`, leurs dépendances et le client web.
Après installation, activer le venv (`.venv/Scripts/Activate.ps1` sous PowerShell ;
`source .venv/bin/activate` sous Linux/macOS). Les commandes suivantes sont identiques
sur les deux systèmes.

Dans le dossier de travail vide, créer une configuration locale une seule fois :

```text
python -c "import secrets; from pathlib import Path; k=secrets.token_urlsafe(24); a=secrets.token_urlsafe(24); p=Path('.env'); assert not p.exists(), '.env existe déjà'; p.write_text('API_KEYS='+k+':client,'+a+':admin\nAPI_KEY='+k+'\nAPI_URL=http://127.0.0.1:8000\n', encoding='utf-8')"
sentiment serve
```

Laisser ce terminal ouvert. Dans un deuxième terminal, même dossier, même venv activé :

```text
sentiment ui
```

- Interface : http://127.0.0.1:8501 (avis, CSV avec colonne `text`, deux graphiques, export).
- Client web : http://127.0.0.1:8000/web ; copier la valeur `API_KEY` du `.env` dans le champ clé.
- Documentation interactive : http://127.0.0.1:8000/docs ; utiliser l'en-tête `X-API-Key` sur `/v1`.
- Test public : http://127.0.0.1:8000/v1/health.
- `sentiment serve --port 8001` et `sentiment ui --port 8502` changent les ports ; adapter `API_URL`.
- Arrêt : Ctrl+C dans chaque terminal.

Un CSV d'exemple :

```csv
text
"Livraison rapide, très satisfait"
"Produit cassé, à fuir"
"xqzvb wlkptr grombu"
```

Clés manquantes/invalides : l'interface indique un refus d'accès. API arrêtée : message lisible.
CSV vide, mal encodé, sans colonne `text` ou de plus de 1000 lignes : refus lisible.
Les anciennes routes `/predict` et `/health` sont conservées pour les TP historiques ;
elles ne sont pas authentifiées. Le serveur écoute uniquement sur 127.0.0.1 et est prévu
pour une démonstration locale. Ne pas publier le fichier `.env`.
