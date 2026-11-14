"""Contrats d'entrée et de sortie partagés par les deux versions de l'API."""
from pydantic import BaseModel, Field, field_validator

from api.model import Label


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000,
                      examples=["Livraison rapide, produit conforme, très satisfait"])

    @field_validator("text")
    @classmethod
    def texte_non_vide(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("texte vide")
        return value


class PredictResponse(BaseModel):
    label: Label
    score: float = Field(..., ge=0, le=1)
    text: str


class HealthResponse(BaseModel):
    status: str
    model: str
