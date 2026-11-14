"""Compatibilité TP2 : python src/predict.py TEXTE, paquet installé requis."""
from sentiment_app.cli import main
from sentiment_app.predict import charger_modele, predict

__all__ = ["charger_modele", "predict"]

if __name__ == "__main__":
    raise SystemExit(main())
