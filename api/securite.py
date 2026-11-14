"""Clés et rôles : configuration validée, comparaison en temps constant."""
import secrets
from typing import Annotated

from fastapi import Header, HTTPException, Request


def lire_cles(value: str) -> dict[str, str]:
    keys: dict[str, str] = {}
    if not value.strip():
        return keys
    for entry in value.split(","):
        key, separator, role = entry.strip().partition(":")
        if not separator or len(key) < 16 or role not in {"client", "admin"} or key in keys:
            raise ValueError("Configuration API_KEYS invalide : clé unique >=16 caractères et rôle client/admin")
        keys[key] = role
    return keys


def exiger(*roles: str):
    def verifier(request: Request, x_api_key: Annotated[str | None, Header()] = None) -> str:
        role = next((role for key, role in request.app.state.api_keys.items()
                     if secrets.compare_digest(key.encode(), (x_api_key or "").encode())), None)
        if role is None:
            raise HTTPException(401, "Clé absente ou inconnue")
        if role not in roles:
            raise HTTPException(403, "Rôle insuffisant")
        return role
    return verifier
