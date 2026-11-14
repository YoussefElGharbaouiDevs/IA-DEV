"""Commande installée avec le paquet : sentiment [--json] TEXTE."""
import argparse
import json
import sys

from . import __version__, predict


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in {"serve", "ui"}:
        from .launch import serve, ui
        return (serve if sys.argv[1] == "serve" else ui)(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == "predict":
        sys.argv.pop(1)
    parser = argparse.ArgumentParser(description="Sentiment d'un avis français (modèle inclus)")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--json", action="store_true", help="réponse JSON")
    parser.add_argument("texte", nargs="*", help="avis à analyser")
    args = parser.parse_args()
    if not args.texte:
        parser.print_help()
        return 0
    try:
        result = predict(" ".join(args.texte))
    except ValueError as exc:
        print(f"erreur : {exc}", file=sys.stderr)
        return 2
    except (FileNotFoundError, OSError):
        print("erreur : modèle introuvable ou illisible", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False) if args.json
          else f"{result['label']} (confiance {result['score']:.0%})")
    return 0
