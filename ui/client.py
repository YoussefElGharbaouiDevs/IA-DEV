"""Client HTTP de l'API versionnée."""

import os
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

VERDICTS = {
    "POSITIVE": "Avis positif",
    "NEGATIVE": "Avis négatif",
    "INDETERMINE": "Je ne sais pas : à faire vérifier par un humain",
}
INJOIGNABLE = "API injoignable : lancez d'abord uvicorn api.main:app"
REFUS = "Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères."
SANS_MODELE = "Modèle non chargé : python src/train.py, puis relancer l'API."
CLE = "Clé API refusée. Vérifiez API_KEY."


@dataclass
class Reponse:
    ok: bool
    label: str | None = None
    score: float | None = None
    message: str = ""


def creer_session() -> httpx.Client:
    return httpx.Client(base_url=os.getenv("API_URL", "http://127.0.0.1:8000"),
                        timeout=10, headers={"X-API-Key": os.getenv("API_KEY", "")})


def erreur(reponse: httpx.Response) -> Reponse:
    try:
        code = reponse.json()["erreur"]["code"]
    except (ValueError, KeyError, TypeError):
        code = ""
    messages = {
        "ENTREE_INVALIDE": REFUS,
        "MODELE_INDISPONIBLE": SANS_MODELE,
        "NON_AUTHENTIFIE": CLE,
        "ACCES_REFUSE": CLE,
    }
    return Reponse(False, message=messages.get(code, f"Erreur de l'API ({reponse.status_code})."))


def sante(session: httpx.Client) -> Reponse:
    try:
        r = session.get("/v1/health")
    except httpx.TransportError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        return Reponse(True, message=r.json()["model"])
    return erreur(r)


def predire(session: httpx.Client, texte: str) -> Reponse:
    try:
        r = session.post("/v1/predict", json={"text": texte})
    except httpx.TransportError:
        return Reponse(False, message=INJOIGNABLE)
    if r.status_code == 200:
        corps = r.json()
        return Reponse(True, label=corps["label"], score=corps["score"])
    return erreur(r)


def predire_lot(session: httpx.Client, textes: list[str]) -> list[Reponse]:
    return [predire(session, texte) for texte in textes]


def resumer(reponses: list[Reponse]) -> dict[str, int]:
    compte = Counter(r.label if r.ok else "REFUS OU ERREUR" for r in reponses)
    return dict(sorted(compte.items()))
