# sentiment-app

Classifieur TF-IDF et régression logistique pour des avis clients en français. Le modèle est inclus dans le paquet et la prédiction fonctionne hors ligne après installation.

Avec Python 3.11 ou 3.12 :

```powershell
python -m pip install sentiment_app-1.0.0-py3-none-any.whl
sentiment "Livraison rapide, produit conforme, très satisfait" --json
```

```python
from sentiment_app import predict

print(predict("Produit cassé et service injoignable"))
```

Le paquet donne un verdict binaire et un score. L’API applique en plus un seuil de 0,60 sous lequel elle renvoie `INDETERMINE`. Le modèle de démonstration est entraîné sur 290 avis synthétiques. Les formulations ambiguës, le sarcasme et les avis hors du vocabulaire peuvent donner des prédictions erronées.
