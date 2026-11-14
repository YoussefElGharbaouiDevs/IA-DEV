"""API locale historique et API /v1 protégée, sans entraînement au démarrage."""
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.model import Prediction, SentimentClassifier, load_model
from api.schemas import HealthResponse, PredictRequest, PredictResponse
from api.securite import exiger, lire_cles

load_dotenv(Path.cwd() / ".env")
logger = logging.getLogger("sentiment_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.api_keys = lire_cles(os.getenv("API_KEYS", ""))
    app.state.classifier = load_model()
    yield
    app.state.classifier = None


app = FastAPI(title="Sentiment Analysis API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware,
                  allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500,http://localhost:15500,http://127.0.0.1:15500").split(","),
                  allow_methods=["GET", "POST"], allow_headers=["Content-Type", "X-API-Key"])

CODES = {400: "REQUETE_INVALIDE", 401: "NON_AUTHENTIFIE", 403: "ACCES_REFUSE",
         404: "INTROUVABLE", 405: "METHODE_NON_AUTORISEE", 422: "ENTREE_INVALIDE",
         500: "ERREUR_INTERNE", 503: "MODELE_INDISPONIBLE"}


def erreur_v1(status: int, message: str, champs: list | None = None) -> JSONResponse:
    return JSONResponse(status_code=status, content={"erreur": {
        "code": CODES.get(status, f"HTTP_{status}"), "message": message, "champs": champs or []}})


@app.exception_handler(StarletteHTTPException)
async def erreur_http(request: Request, exc: StarletteHTTPException) -> Response:
    if request.url.path == "/v1" or request.url.path.startswith("/v1/"):
        return erreur_v1(exc.status_code, str(exc.detail))
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def erreur_validation(request: Request, exc: RequestValidationError) -> Response:
    if request.url.path.startswith("/v1/"):
        champs = [{"champ": ".".join(map(str, error["loc"])), "message": error["msg"]}
                  for error in exc.errors()]
        return erreur_v1(422, "Entrée refusée par le contrat de l'API", champs)
    return await request_validation_exception_handler(request, exc)


def classifier() -> SentimentClassifier:
    model = getattr(app.state, "classifier", None)
    if model is None:
        raise HTTPException(503, "Modèle non chargé")
    return model


@app.get("/")
def root():
    return {"message": "Sentiment Analysis API", "docs": "/docs", "health": "/v1/health"}


@app.get("/health", response_model=HealthResponse, deprecated=True)
@app.get("/v1/health", response_model=HealthResponse)
def health_check():
    return {"status": "OK", "model": classifier().model_name}


def analyser(body: PredictRequest) -> Prediction:
    model = classifier()
    try:
        result = model.predict(body.text)
    except Exception:
        logger.exception("Erreur lors de la prédiction")
        raise HTTPException(500, "Erreur interne du serveur") from None
    logger.info("predict -> %s (%.2f)", result["label"], result["score"])
    return result


@app.post("/predict", response_model=PredictResponse, deprecated=True)
def predict(body: PredictRequest, response: Response):
    response.headers["Deprecation"] = "true"
    return analyser(body)


@app.post("/v1/predict", response_model=PredictResponse,
          dependencies=[Depends(exiger("client", "admin"))])
def predict_v1(body: PredictRequest):
    return analyser(body)


@app.get("/v1/admin/info", dependencies=[Depends(exiger("admin"))])
def admin_info():
    return {"version": "1.0.0", "model": classifier().model_name}


@app.get("/web", include_in_schema=False)
def web_client():
    from importlib.resources import files

    from fastapi.responses import HTMLResponse
    return HTMLResponse(files("sentiment_app").joinpath("web/index.html").read_text(encoding="utf-8"))
