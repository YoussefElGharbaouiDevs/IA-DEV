"""Lanceurs utilisables sans dépôt ni modification du PATH Python."""
import argparse
import subprocess
import sys
from importlib.resources import files


def serve(args=None):
    import uvicorn
    parser = argparse.ArgumentParser(description="API et client web local")
    parser.add_argument("--port", type=int, default=8000)
    opts = parser.parse_args(args)
    uvicorn.run("api.main:app", host="127.0.0.1", port=opts.port)
    return 0


def ui(args=None):
    parser = argparse.ArgumentParser(description="Interface Streamlit (API déjà lancée)")
    parser.add_argument("--port", type=int, default=8501)
    opts = parser.parse_args(args)
    path = str(files("ui").joinpath("app.py"))
    return subprocess.call([sys.executable, "-m", "streamlit", "run", path,
                            "--server.address=127.0.0.1", f"--server.port={opts.port}",
                            "--browser.gatherUsageStats=false", "--server.headless=true"])
