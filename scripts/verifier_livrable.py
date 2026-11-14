"""Installe la roue dans un venv neuf hors du dépôt et vérifie l'application entière."""
import os
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.request
import venv
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def port_libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    wheel = ROOT / "dist/sentiment_app-1.0.0-py3-none-any.whl"
    checks = []
    with zipfile.ZipFile(wheel) as z:
        names = z.namelist()
        assert "sentiment_app/modele/sentiment.joblib" in names
        assert "sentiment_app/web/index.html" in names
        assert not any(n.startswith("tests/") or ".env" in n for n in names)
    checks.append("Roue : modèle, client web et métadonnées présents ; aucun test/secret")
    with tempfile.TemporaryDirectory(prefix="recette-sentiment-") as tmp:
        folder = Path(tmp)
        venv.create(folder / "env", with_pip=True)
        bins = folder / "env" / ("Scripts" if os.name == "nt" else "bin")
        python = str(bins / ("python.exe" if os.name == "nt" else "python"))
        cli = str(bins / ("sentiment.exe" if os.name == "nt" else "sentiment"))
        env = {k: v for k, v in os.environ.items() if k not in {
            "PYTHONPATH", "SENTIMENT_MODELE", "API_KEYS", "API_KEY", "API_URL"}}
        env["PYTHONUTF8"] = "1"

        def run(*args):
            r = subprocess.run(args, cwd=folder, env=env, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=600)
            if r.returncode:
                raise RuntimeError(r.stdout + r.stderr)
            return r.stdout.strip()

        print("Installation de la roue dans un environnement neuf...", flush=True)
        run(python, "-m", "pip", "install", "--disable-pip-version-check", str(wheel), "pytest==8.3.5")
        run(python, "-m", "pip", "check")
        checks.append("Installation isolée et pip check : OK")
        shutil.copy2(ROOT / "tests/test_paquet.py", folder / "test_paquet.py")
        checks.append(run(python, "-m", "pytest", "-q", "test_paquet.py"))
        api_port, ui_port = port_libre(), port_libre()
        env.update(API_KEYS="recette-client-key-123:client,recette-admin-key-123:admin",
                   API_KEY="recette-client-key-123", API_URL=f"http://127.0.0.1:{api_port}")
        (folder / ".env").write_text("\n".join(f"{k}={env[k]}" for k in
                                     ["API_KEYS", "API_KEY", "API_URL"]) + "\n", encoding="utf-8")
        service_env = {k: v for k, v in env.items() if k not in {"API_KEYS", "API_KEY", "API_URL"}}
        processes = []
        try:
            for mode, port, path in [("serve", api_port, "/v1/health"), ("ui", ui_port, "/_stcore/health")]:
                log = (folder / f"{mode}.log").open("w", encoding="utf-8")
                process = subprocess.Popen([cli, mode, "--port", str(port)], cwd=folder,
                                           env=service_env, stdout=log, stderr=log)
                processes.append((process, log))
                url = f"http://127.0.0.1:{port}{path}"
                for _ in range(100):
                    try:
                        with urllib.request.urlopen(url, timeout=2) as response:
                            assert response.status == 200
                        break
                    except OSError:
                        if process.poll() is not None:
                            raise RuntimeError((folder / f"{mode}.log").read_text()) from None
                        time.sleep(.3)
                else:
                    raise RuntimeError(f"Démarrage {mode} trop long")
                checks.append(f"Commande sentiment {mode} et serveur HTTP : OK")
            smoke = r'''
import io, os
from importlib.resources import files
import httpx
import streamlit as st
from streamlit.testing.v1 import AppTest
base=os.environ["API_URL"]
with httpx.Client(base_url=base) as c:
    assert c.get('/web').status_code == 200
    assert c.post('/v1/predict',json={'text':'Bonjour'}).status_code == 401
    c.headers['X-API-Key']=os.environ['API_KEY']
    assert c.post('/v1/predict',json={'text':'   '}).status_code == 422
    assert c.post('/v1/predict',json={'text':'Livraison rapide, très satisfait'}).json()['label']=='POSITIVE'
    assert c.post('/v1/predict',json={'text':'xqzvb wlkptr grombu'}).json()['label']=='INDETERMINE'
    assert c.get('/v1/admin/info').status_code==403
    c.headers['X-API-Key']='recette-admin-key-123'
    assert c.get('/v1/admin/info').status_code==200
page=AppTest.from_file(str(files('ui').joinpath('app.py')),default_timeout=30).run()
assert not page.exception
assert 'API prête' in page.caption[0].value
page.text_area[0].input('Livraison rapide, produit conforme, très satisfait').run()
page.button[0].click().run()
assert page.metric[0].label=='Avis positif'
st.file_uploader=lambda *a,**kw:io.BytesIO('text\nLivraison rapide, très satisfait\nProduit cassé, à fuir\n'.encode())
page=AppTest.from_file(str(files('ui').joinpath('app.py')),default_timeout=30).run()
assert not page.exception
assert len(page.dataframe[0].value)==2
assert len(page.get('arrow_vega_lite_chart'))==2
assert len(page.get('download_button'))==1
print('API, rôles, refus, abstention, Streamlit, CSV, deux graphiques et export : OK')
'''
            (folder / "smoke.py").write_text(smoke, encoding="utf-8")
            checks.append(run(python, "smoke.py"))
        finally:
            for process, log in reversed(processes):
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)
                else:
                    process.terminate()
                process.wait(timeout=15)
                log.close()
        run(python, "-m", "pip", "uninstall", "-y", "sentiment-app")
        absent = subprocess.run([python, "-c", "import sentiment_app"], cwd=folder, env=env,
                                capture_output=True)
        assert absent.returncode != 0 and not Path(cli).exists()
        checks.append("Désinstallation : paquet et commande retirés")
    report = "\n".join(checks) + "\nBilan technique : CONFORME\n"
    report += "Publication GitHub/tag/CI distante et recette par un autre membre : non effectuées par ce contrôle local.\n"
    (ROOT / "docs/livrable-tp4.txt").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
