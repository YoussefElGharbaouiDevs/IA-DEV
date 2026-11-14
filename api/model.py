"""Adaptation du prédicteur local au contrat HTTP."""

from typing import TypedDict, cast

from api.schemas import Label
from src.predict import charger_modele
from src.predict import predict as predire

SEUIL_ABSTENTION = 0.6


class Prediction(TypedDict):
    label: Label
    score: float
    text: str


class SentimentClassifier:
    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        charger_modele()

    def predict(self, text: str) -> Prediction:
        resultat = predire(text)
        score = resultat["score"]
        label = cast(Label, str(resultat["label"]).upper())
        if score < SEUIL_ABSTENTION:
            label = "INDETERMINE"
        return {"label": label, "score": score, "text": text[:100]}


def load_model() -> SentimentClassifier:
    return SentimentClassifier()
