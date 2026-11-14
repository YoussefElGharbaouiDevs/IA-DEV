"""Adaptateur typé : modèle installé, labels API et abstention."""
from typing import Literal, TypedDict

from sentiment_app.predict import charger_modele
from sentiment_app.predict import predict as _predict

Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
SEUIL_ABSTENTION = 0.60
ETIQUETTES: dict[str, Label] = {"positive": "POSITIVE", "negative": "NEGATIVE"}


class Prediction(TypedDict):
    label: Label
    score: float
    text: str


class SentimentClassifier:
    model_name = "tfidf-logreg (TP2, sentiment.joblib inclus dans sentiment-app 1.0.0)"

    def __init__(self) -> None:
        if set(charger_modele().classes_) != set(ETIQUETTES):
            raise ValueError("Classes inattendues dans le modèle")

    def predict(self, text: str) -> Prediction:
        result = _predict(text)
        label = ETIQUETTES[result["label"]] if result["score"] >= SEUIL_ABSTENTION else "INDETERMINE"
        return {"label": label, "score": result["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    return SentimentClassifier()
