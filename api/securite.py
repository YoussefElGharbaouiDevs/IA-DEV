"""Authentification par clé et rôles pour les routes protégées."""

import os
from collections.abc import Callable
from secrets import compare_digest
from typing import Annotated, Literal

from fastapi import Depends, HTTPException, Request, Security
from fastapi.security import APIKeyHeader

Role = Literal["client", "admin"]
EN_TETE = APIKeyHeader(name="X-API-Key", auto_error=False)


def charger_cles(brut: str | None = None) -> dict[str, Role]:
    if brut is None:
        brut = os.getenv("API_KEYS", "")
    cles: dict[str, Role] = {}
    for entree in filter(None, (morceau.strip() for morceau in brut.split(","))):
        cle, _, role = entree.rpartition(":")
        if role != "client" and role != "admin":
            raise ValueError("API_KEYS attend les rôles client ou admin")
        if len(cle) < 16:
            raise ValueError("Une clé API_KEYS doit avoir au moins 16 caractères")
        if cle in cles:
            raise ValueError("Une clé API_KEYS est déclarée plusieurs fois")
        cles[cle] = "client" if role == "client" else "admin"
    return cles


def identifier(request: Request, cle: Annotated[str | None, Security(EN_TETE)]) -> Role:
    cles: dict[str, Role] = request.app.state.cles
    if cle:
        for connue, role in cles.items():
            if compare_digest(cle.encode(), connue.encode()):
                return role
    message = "Clé d'API invalide" if cle else "Clé d'API manquante : en-tête X-API-Key"
    raise HTTPException(401, message, headers={"WWW-Authenticate": "APIKey"})


def exiger(*autorises: Role) -> Callable[[Role], Role]:
    def verifier(role: Annotated[Role, Depends(identifier)]) -> Role:
        if role not in autorises:
            raise HTTPException(403, f"Accès refusé au rôle « {role} »")
        return role

    return verifier
