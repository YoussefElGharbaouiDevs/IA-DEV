"""Vérifie réellement le parcours CSV, ses graphiques, son export et ses erreurs."""
from io import BytesIO
from pathlib import Path

import pytest
import streamlit as st
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

from api.main import app
from ui import client

PAGE = str(Path(__file__).parents[1] / "ui/app.py")


@pytest.mark.parametrize("data,message", [
    (b"", "CSV illisible"), (b"autre\nbonjour", "Colonne text absente"),
    (b"text\n" + b"bonjour\n" * 1001, "1000 avis"),
])
def test_csv_erreurs(monkeypatch, data, message):
    with TestClient(app) as api:
        monkeypatch.setattr(client, "creer_session", lambda: api)
        monkeypatch.setattr(st, "file_uploader", lambda *a, **kw: BytesIO(data))
        page = AppTest.from_file(PAGE).run()
        assert not page.exception
        assert any(message in e.value for e in page.error)


def test_csv_graphiques_export(monkeypatch):
    data = (Path(__file__).parents[1] / "data/avis_exemple.csv").read_bytes()
    with TestClient(app, headers={"X-API-Key": "test-client-key-123456"}) as api:
        monkeypatch.setattr(client, "creer_session", lambda: api)
        monkeypatch.setattr(st, "file_uploader", lambda *a, **kw: BytesIO(data))
        page = AppTest.from_file(PAGE).run()
        assert not page.exception
        assert len(page.dataframe[0].value) == 6
        assert {"verdict", "confiance"} <= set(page.dataframe[0].value.columns)
        assert len(page.get("arrow_vega_lite_chart")) == 2
        assert len(page.get("download_button")) == 1
