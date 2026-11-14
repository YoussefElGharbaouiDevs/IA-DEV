"""Vérifie les artefacts du TP4 et installe la roue dans un environnement neuf."""

import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import venv
from pathlib import Path
from zipfile import ZipFile

RACINE = Path(__file__).resolve().parents[1]
DIST = RACINE / "dist"
VERSION = "1.0.0"
ROUE = DIST / f"sentiment_app-{VERSION}-py3-none-any.whl"
SOURCE = DIST / f"sentiment_app-{VERSION}.tar.gz"
MODELE = "sentiment_app/modele/sentiment.joblib"


def verifier() -> int:
    lignes: list[str] = []

    def controle(ok: bool, message: str) -> None:
        lignes.append(f"[{'OK' if ok else 'ÉCHEC'}] {message}")

    def lancer(args, dossier=RACINE, env=None):
        return subprocess.run(args, cwd=dossier, env=env, text=True,
                              encoding="utf-8", stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, check=True).stdout.strip()

    controle(ROUE.is_file(), f"roue présente : {ROUE.name}")
    controle(SOURCE.is_file(), f"distribution source présente : {SOURCE.name}")
    controle(DIST.is_dir() and set(DIST.iterdir()) == {ROUE, SOURCE}, "deux archives dans dist/")
    try:
        if ROUE.is_file():
            with ZipFile(ROUE) as archive:
                fichiers = archive.namelist()
                controle(MODELE in fichiers, "modèle embarqué dans la roue")
                entree = f"sentiment_app-{VERSION}.dist-info/entry_points.txt"
                controle(entree in fichiers and b"sentiment = sentiment_app.cli:main" in
                         archive.read(entree), "commande sentiment déclarée")
                controle(not any(n.startswith("tests/") for n in fichiers), "pas de tests dans la roue")
        if SOURCE.is_file():
            with tarfile.open(SOURCE) as archive_source:
                controle(any(n.endswith("/src/" + MODELE) for n in archive_source.getnames()),
                         "modèle présent dans la distribution source")
        controle(f"## [{VERSION}]" in (RACINE / "CHANGELOG.md").read_text(encoding="utf-8"),
                 "version décrite dans CHANGELOG.md")
        controle(f"v{VERSION}" in lancer(["git", "tag", "--points-at", "HEAD"]).splitlines(),
                 f"étiquette v{VERSION} sur HEAD")
        if ROUE.is_file():
            with tempfile.TemporaryDirectory(prefix="sentiment-verification-") as temporaire:
                dossier = Path(temporaire)
                environnement = dossier / "venv"
                venv.EnvBuilder(with_pip=True).create(environnement)
                scripts = environnement / ("Scripts" if os.name == "nt" else "bin")
                suffixe = ".exe" if os.name == "nt" else ""
                python = str(scripts / f"python{suffixe}")
                cli = str(scripts / f"sentiment{suffixe}")
                env = {**os.environ, "VERIFICATION_LIVRABLE": "1", "PYTHONUTF8": "1"}
                env.pop("PYTHONPATH", None)
                lancer([python, "-m", "pip", "install", str(ROUE), "pytest>=8"], dossier, env)
                controle(True, "installation de la roue dans un environnement neuf")
                shutil.copy2(RACINE / "tests/test_paquet.py", dossier)
                bilan = lancer([python, "-m", "pytest", "-q", "test_paquet.py"], dossier, env)
                controle("6 passed" in bilan, f"tests du paquet installé : {bilan.splitlines()[-1]}")
                sortie = lancer([cli, "Produit cassé et service injoignable", "--json"], dossier, env)
                controle(json.loads(sortie)["label"] == "negative", f"commande installée : {sortie}")
    except subprocess.CalledProcessError as erreur:
        controle(False, f"commande échouée : {erreur.cmd}\n{erreur.stdout}")
    except (OSError, ValueError) as erreur:
        controle(False, str(erreur))

    conforme = all(ligne.startswith("[OK]") for ligne in lignes)
    lignes.append(f"Bilan : {'CONFORME' if conforme else 'NON CONFORME'}")
    rapport = "\n".join(lignes) + "\n"
    (RACINE / "docs/livrable-tp4.txt").write_text(rapport, encoding="utf-8")
    print(rapport, end="")
    return 0 if conforme else 1


if __name__ == "__main__":
    raise SystemExit(verifier())
