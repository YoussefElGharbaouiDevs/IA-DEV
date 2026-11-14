"""Routes de la version 1 et opérations communes avec l'API historique."""

import json
import logging
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request

from api.model import SEUIL_ABSTENTION, Prediction, SentimentClassifier
from api.schemas import ErreurV1, HealthResponse, PredictRequest, PredictResponse
from api.securite import exiger

logger = logging.getLogger(__name__)
METRIQUES = Path(__file__).resolve().parents[1] / "models" / "metrics.json"
ERREURS: dict[int | str, dict[str, Any]] = {code: {"model": ErreurV1} for code in (401, 403, 422, 500, 503)}
router = APIRouter(prefix="/v1", tags=["v1"], responses=ERREURS)


def classifier(request: Request) -> SentimentClassifier:
    modele: SentimentClassifier | None = getattr(request.app.state, "classifier", None)
    if modele is None:
        raise HTTPException(503, "Modèle non chargé")
    return modele


Classifier = Annotated[SentimentClassifier, Depends(classifier)]


@router.get("/health", response_model=HealthResponse, summary="Santé (public)")
def sante(clf: Classifier) -> HealthResponse:
    return HealthResponse(status="OK", model=clf.model_name)


@router.post("/predict", response_model=PredictResponse,
             dependencies=[Depends(exiger("client", "admin"))])
def predire(corps: PredictRequest, clf: Classifier) -> Prediction:
    try:
        resultat = clf.predict(corps.text)
    except Exception:
        logger.exception("Échec de la prédiction")
        raise HTTPException(500, "Erreur interne du serveur") from None
    logger.info("Prédiction %s (%.2f)", resultat["label"], resultat["score"])
    return resultat


@router.get("/modele", dependencies=[Depends(exiger("admin"))])
def modele(clf: Classifier) -> dict[str, object]:
    try:
        metriques = json.loads(METRIQUES.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise HTTPException(503, "Métriques indisponibles") from None
    return {"model": clf.model_name, "seuil_abstention": SEUIL_ABSTENTION, "metriques": metriques}
