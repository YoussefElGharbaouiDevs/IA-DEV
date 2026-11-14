"""Démarrage, pannes, clés et contrats de l'API."""
import pytest
from fastapi.testclient import TestClient

from api import model
from api.main import app
from api.securite import lire_cles
from sentiment_app.predict import charger_modele


def test_demarrage():
    with TestClient(app) as c:
        assert c.get("/health").json()["status"]=="OK"
        assert c.get("/web").status_code==200


def test_modele_absent(monkeypatch):
    charger_modele.cache_clear()
    monkeypatch.setenv("SENTIMENT_MODELE", "fichier-absent.joblib")
    try:
        with pytest.raises(FileNotFoundError), TestClient(app):
            pass
    finally:
        charger_modele.cache_clear()


def test_classes_inattendues(monkeypatch):
    class Faux:
        classes_=["inconnue"]
    monkeypatch.setattr(model,"charger_modele",lambda:Faux())
    with pytest.raises(ValueError,match="Classes inattendues"), TestClient(app):
        pass


@pytest.mark.parametrize("exception",[RuntimeError,ValueError])
def test_panne(monkeypatch,exception):
    class Panne:
        def predict(self,text):
            raise exception("message prive")
    with TestClient(app) as c:
        monkeypatch.setattr(app.state,"classifier",Panne())
        for path in ["/predict","/v1/predict"]:
            r=c.post(path,json={"text":"Bonjour"},headers={"X-API-Key":"test-client-key-123456"})
            assert r.status_code==500 and "message prive" not in r.text


def test_non_charge(monkeypatch):
    with TestClient(app) as c:
        monkeypatch.setattr(app.state,"classifier",None)
        assert c.get("/health").status_code==503
        assert c.post("/predict",json={"text":"Bonjour"}).status_code==503


def test_v1_contrat_roles():
    with TestClient(app) as c:
        assert c.get("/v1/health").status_code==200
        assert c.post("/v1/predict",json={"text":"Bonjour"}).json()["erreur"]["code"]=="NON_AUTHENTIFIE"
        c.headers["X-API-Key"]="test-client-key-123456"
        assert c.post("/v1/predict",json={"text":"Livraison rapide, très satisfait"}).status_code==200
        assert c.post("/v1/predict",json={"text":" "}).json()["erreur"]["code"]=="ENTREE_INVALIDE"
        assert c.get("/v1/admin/info").status_code==403
        c.headers["X-API-Key"]="test-admin-key-123456"
        assert c.get("/v1/admin/info").status_code==200
        assert c.get("/v1/absent").status_code==404


@pytest.mark.parametrize("value",["court:client","long-enough-key-123:superuser","cle-sans-role", "long-enough-key-123:client,long-enough-key-123:admin"])
def test_mauvaise_config(value):
    with pytest.raises(ValueError):
        lire_cles(value)
