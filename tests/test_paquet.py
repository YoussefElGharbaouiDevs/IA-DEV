"""Ces tests doivent passer sur la roue installée, hors du dépôt."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

import sentiment_app

if "site-packages" not in sentiment_app.__file__:
    pytest.skip("Tests réservés à la roue installée hors du dépôt : scripts/verifier_livrable.py",
                allow_module_level=True)


def commande(*args):
    exe = Path(sys.executable).parent / ("sentiment.exe" if sys.platform == "win32" else "sentiment")
    return subprocess.run([str(exe), *args], capture_output=True, text=True, encoding="utf-8")


def test_importe_depuis_le_paquet_installe():
    assert "site-packages" in sentiment_app.__file__


def test_version():
    assert sentiment_app.__version__ == "1.0.0"
    assert commande("--version").stdout.strip() == "1.0.0"


def test_prediction():
    result = sentiment_app.predict("Livraison rapide, très satisfait")
    assert result["label"] == "positive" and 0 <= result["score"] <= 1


def test_cli_json():
    result = commande("--json", "Produit cassé, à fuir")
    assert result.returncode == 0
    assert json.loads(result.stdout)["label"] == "negative"


def test_vide():
    result = commande(" ")
    assert result.returncode == 2 and "texte vide" in result.stderr
    assert "Traceback" not in result.stderr


def test_aide():
    assert commande().returncode == 0
    assert "usage:" in commande().stdout
