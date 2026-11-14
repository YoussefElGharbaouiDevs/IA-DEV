"""Vérifications effectuées depuis un environnement où la roue est installée."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

if os.getenv("VERIFICATION_LIVRABLE") != "1":
    pytest.skip("Roue à vérifier avec scripts/verifier_livrable.py", allow_module_level=True)

from sentiment_app import __version__, predict

CLI = Path(sys.executable).with_name("sentiment.exe" if os.name == "nt" else "sentiment")


def test_version():
    assert __version__ == "1.0.0"


@pytest.mark.parametrize(("texte", "label"), [
    ("Livraison rapide, produit conforme, très satisfait", "positive"),
    ("Produit cassé et service injoignable, à fuir", "negative"),
])
def test_prediction(texte, label):
    resultat = predict(texte)
    assert resultat["label"] == label
    assert 0.5 <= resultat["score"] <= 1


def test_texte_vide():
    with pytest.raises(ValueError, match="texte vide"):
        predict("  ")


def test_cli_json():
    texte = "Produit cassé et service injoignable, à fuir"
    sortie = subprocess.check_output([str(CLI), texte, "--json"], text=True)
    assert json.loads(sortie) == predict(texte)


def test_cli_version():
    assert subprocess.check_output([str(CLI), "--version"], text=True).strip() == "sentiment 1.0.0"
