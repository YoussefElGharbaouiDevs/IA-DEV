"""Prédiction indépendante du dossier courant et de l'API."""
import os
from functools import lru_cache
from importlib.resources import as_file, files
from pathlib import Path
from typing import Literal, TypedDict, cast

import joblib


class Resultat(TypedDict):
    label: Literal["positive", "negative"]
    score: float


@lru_cache(maxsize=1)
def charger_modele():
    override = os.environ.get("SENTIMENT_MODELE")
    if override:
        path = Path(override)
        if not path.is_file():
            raise FileNotFoundError("Modèle configuré introuvable")
        return joblib.load(path)
    resource = files("sentiment_app").joinpath("modele/sentiment.joblib")
    if not resource.is_file():
        raise FileNotFoundError("Modèle absent du paquet : reconstruisez la distribution")
    with as_file(resource) as path:
        return joblib.load(path)


def predict(texte: str) -> Resultat:
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    label = str(pipeline.predict([texte])[0])
    if label not in {"positive", "negative"}:
        raise ValueError("Classe du modèle non prise en charge")
    return {"label": cast(Literal["positive", "negative"], label),
            "score": round(float(pipeline.predict_proba([texte]).max()), 4)}
