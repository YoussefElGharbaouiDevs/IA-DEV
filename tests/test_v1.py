"""Contrat, authentification et cas d’erreur de l’API."""

import pytest
from fastapi.testclient import TestClient

from api import main, v1
from api.model import SentimentClassifier, charger_modele
from api.securite import charger_cles
from src import predict as predicteur
from tests.conftest_api import CLE_ADMIN, CLE_CLIENT

FAVORABLE = "Livraison rapide, produit conforme, très satisfait"
CLIENT = {"X-API-Key": CLE_CLIENT}
ADMIN = {"X-API-Key": CLE_ADMIN}


@pytest.fixture
def api(monkeypatch):
    monkeypatch.setenv("API_KEYS", f"{CLE_CLIENT}:client,{CLE_ADMIN}:admin")
    with TestClient(main.app) as client:
        yield client


@pytest.mark.parametrize("texte,verdict", [
    (FAVORABLE, "POSITIVE"),
    ("Produit cassé et service injoignable, à fuir", "NEGATIVE"),
    ("xqzvb wlkptr grombu", "INDETERMINE"),
])
def test_predire(api, texte, verdict):
    resultat = api.post("/v1/predict", json={"text": texte}, headers=CLIENT)
    assert resultat.status_code == 200
    assert resultat.json()["label"] == verdict
    assert 0.5 <= resultat.json()["score"] <= 1


@pytest.mark.parametrize("corps", [{}, {"text": ""}, {"text": " \t"}, {"text": "a" * 2001},
                                  {"text": 42}, {"text": None}])
def test_entree_invalide(api, corps):
    reponse = api.post("/v1/predict", json=corps, headers=CLIENT)
    assert reponse.status_code == 422
    erreur = reponse.json()["erreur"]
    assert erreur["code"] == "ENTREE_INVALIDE"
    assert erreur["champs"][0]["champ"] == "body.text"


@pytest.mark.parametrize("taille", [1, 2000])
def test_bornes_valides(api, taille):
    reponse = api.post("/v1/predict", json={"text": "a" * taille}, headers=CLIENT)
    assert reponse.status_code == 200
    assert len(reponse.json()["text"]) == min(taille, 100)


@pytest.mark.parametrize("en_tetes", [{}, {"X-API-Key": "invalide"}])
def test_authentification(api, en_tetes):
    reponse = api.post("/v1/predict", json={"text": FAVORABLE}, headers=en_tetes)
    assert reponse.status_code == 401
    assert reponse.headers["WWW-Authenticate"] == "APIKey"
    assert reponse.json()["erreur"]["code"] == "NON_AUTHENTIFIE"


def test_autorisation(api):
    interdit = api.get("/v1/modele", headers=CLIENT)
    assert interdit.status_code == 403
    assert interdit.json()["erreur"]["code"] == "ACCES_REFUSE"
    assert api.get("/v1/modele", headers=ADMIN).json()["seuil_abstention"] == 0.6
    assert api.post("/v1/predict", json={"text": FAVORABLE}, headers=ADMIN).status_code == 200


def test_cors(api):
    def prevol(origine):
        return api.options("/v1/predict", headers={
            "Origin": origine, "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-API-Key,Content-Type",
        })
    assert prevol("http://localhost:5500").headers["access-control-allow-origin"] == (
        "http://localhost:5500"
    )
    assert prevol("http://localhost:5600").status_code == 400


def test_routes_historiques(api):
    assert api.get("/").json()["docs"] == "/docs"
    assert api.get("/health").headers["deprecation"] == "true"
    assert api.get("/v1/health").json()["status"] == "OK"
    reponse = api.post("/predict", json={"text": FAVORABLE})
    assert reponse.status_code == 200
    assert reponse.headers["link"] == '</v1/predict>; rel="successor-version"'
    assert "detail" in api.post("/predict", json={"text": ""}).json()


@pytest.mark.parametrize(("methode", "route", "statut", "code"), [
    ("get", "/v1/inconnue", 404, "INTROUVABLE"),
    ("get", "/v1/predict", 405, "METHODE_NON_AUTORISEE"),
])
def test_erreur_route(api, methode, route, statut, code):
    reponse = api.request(methode, route)
    assert reponse.status_code == statut
    assert reponse.json()["erreur"]["code"] == code


def test_modele_indisponible(api, monkeypatch):
    monkeypatch.setattr(main.app.state, "classifier", None)
    assert api.get("/health").status_code == 503
    reponse = api.get("/v1/health")
    assert reponse.status_code == 503
    assert reponse.json()["erreur"]["code"] == "MODELE_INDISPONIBLE"


def test_metriques_indisponibles(api, tmp_path, monkeypatch):
    monkeypatch.setattr(v1, "METRIQUES", tmp_path / "absentes.json")
    assert api.get("/v1/modele", headers=ADMIN).status_code == 503


@pytest.mark.parametrize("exception", [RuntimeError("secret"), ValueError("interne")])
def test_panne(api, exception, monkeypatch):
    def panne(*args):
        raise exception

    monkeypatch.setattr(SentimentClassifier, "predict", panne)
    reponse = api.post("/v1/predict", json={"text": FAVORABLE}, headers=CLIENT)
    assert reponse.status_code == 500
    assert reponse.json()["erreur"]["message"] == "Erreur interne du serveur"


@pytest.mark.parametrize("valeur", [
    "cle-correcte-pour-test:autre", "petite:client", f"{CLE_CLIENT}:client,{CLE_CLIENT}:admin",
])
def test_configuration_invalide(valeur):
    with pytest.raises(ValueError):
        charger_cles(valeur)


def test_modele_absent_au_demarrage(tmp_path, monkeypatch):
    monkeypatch.setattr(predicteur, "MODELE", tmp_path / "absent.joblib")
    charger_modele.cache_clear()
    with pytest.raises(FileNotFoundError), TestClient(main.app):
        pass
