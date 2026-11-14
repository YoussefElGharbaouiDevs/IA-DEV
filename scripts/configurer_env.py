"""Crée les clés de démonstration dans le fichier .env local."""

from pathlib import Path
from secrets import token_urlsafe

racine = Path(__file__).resolve().parents[1]
client, admin = token_urlsafe(24), token_urlsafe(24)
modele = (racine / ".env.example").read_text(encoding="utf-8")

try:
    with (racine / ".env").open("x", encoding="utf-8") as f:
        f.write(modele.replace("remplacer-cle-client", client).replace("remplacer-cle-admin", admin))
except FileExistsError:
    print(".env existe déjà.")
else:
    print("Clés locales créées dans .env.")
