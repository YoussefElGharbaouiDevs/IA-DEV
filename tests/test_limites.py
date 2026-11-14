"""Frontières et propriétés Unicode du contrat historique."""
import json

import pytest
from fastapi.testclient import TestClient
from hypothesis import given, settings
from hypothesis import strategies as st

from api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.mark.parametrize("body,status", [("",422),("   ",422),("a",200),("a"*2000,200),
    ("a"*2001,422),(None,422),(42,422),("\u0085",422)])
def test_frontieres(client, body, status):
    response=client.post("/predict", json={} if body is None else {"text":body})
    assert response.status_code==status
    if status==422:
        assert all({"loc","msg","type"} <= set(e) for e in response.json()["detail"])


def test_json_invalide(client):
    assert client.post("/predict",content=b"pas du json",headers={"Content-Type":"application/json"}).status_code==422


@settings(max_examples=40,deadline=None)
@given(st.text(min_size=1,max_size=2000).filter(lambda s: bool(s.strip())))
def test_texte_valide(client, text):
    r=client.post("/predict",content=json.dumps({"text":text}).encode(),headers={"Content-Type":"application/json"})
    assert r.status_code==200
    assert r.json()["label"] in {"POSITIVE","NEGATIVE","INDETERMINE"}
    assert 0<=r.json()["score"]<=1


@settings(max_examples=30,deadline=None)
@given(st.text(alphabet=" \t\n\r\u0085\u00a0\u2003",min_size=1,max_size=2000))
def test_blancs_refuses(client,text):
    r=client.post("/predict",json={"text":text})
    assert r.status_code==422 and isinstance(r.json()["detail"],list)
