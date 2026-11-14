"""API FastAPI. Lancer avec python -m uvicorn api.main:app."""

import logging
import os
from collections.abc import Mapping
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from api import v1
from api.model import Prediction, load_model
from api.schemas import (
    ChampInvalide,
    DetailErreur,
    ErreurV1,
    HealthResponse,
    PredictRequest,
    PredictResponse,
)
from api.securite import charger_cles

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cles = charger_cles()
    app.state.classifier = load_model()
    logger.info("Modèle chargé, %d clé(s) d'API", len(app.state.cles))
    yield
    app.state.classifier = None


app = FastAPI(title="Analyse de sentiment", version="1.0.0", lifespan=lifespan)
origines = "http://localhost:5500,http://127.0.0.1:5500"
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origine.strip() for origine in os.getenv("CORS_ORIGINS", origines).split(",")],
    allow_methods=["GET", "POST"],
    allow_headers=["X-API-Key", "Content-Type"],
)
app.include_router(v1.router)

CODES = {
    400: "REQUETE_INVALIDE",
    401: "NON_AUTHENTIFIE",
    403: "ACCES_REFUSE",
    404: "INTROUVABLE",
    405: "METHODE_NON_AUTORISEE",
    422: "ENTREE_INVALIDE",
    500: "ERREUR_INTERNE",
    503: "MODELE_INDISPONIBLE",
}


def erreur_v1(statut: int, message: str, champs: list[ChampInvalide] | None = None,
              en_tetes: Mapping[str, str] | None = None) -> JSONResponse:
    detail = DetailErreur(code=CODES.get(statut, f"HTTP_{statut}"), message=message,
                          champs=champs or [])
    return JSONResponse(ErreurV1(erreur=detail).model_dump(), statut, headers=en_tetes)


def est_v1(request: Request) -> bool:
    return request.url.path == "/v1" or request.url.path.startswith("/v1/")


@app.exception_handler(HTTPException)
async def erreur_http(request: Request, exc: HTTPException) -> Response:
    if est_v1(request):
        return erreur_v1(exc.status_code, str(exc.detail), en_tetes=exc.headers)
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def erreur_validation(request: Request, exc: RequestValidationError) -> Response:
    if est_v1(request):
        champs = [
            ChampInvalide(champ=".".join(str(x) for x in e["loc"]), message=e["msg"])
            for e in exc.errors()
        ]
        return erreur_v1(422, "Entrée refusée par le contrat de l'API", champs)
    return await request_validation_exception_handler(request, exc)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Sentiment Analysis API", "docs": "/docs", "health": "/health"}


@app.get("/health", response_model=HealthResponse, deprecated=True)
def health_check(response: Response, clf: v1.Classifier) -> HealthResponse:
    response.headers.update({"Deprecation": "true", "Link": '</v1/health>; rel="successor-version"'})
    return v1.sante(clf)


@app.post("/predict", response_model=PredictResponse, deprecated=True)
def predict(request: PredictRequest, response: Response, clf: v1.Classifier) -> Prediction:
    response.headers.update({"Deprecation": "true", "Link": '</v1/predict>; rel="successor-version"'})
    return v1.predire(request, clf)
