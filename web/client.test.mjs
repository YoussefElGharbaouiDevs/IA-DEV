import assert from "node:assert/strict";
import test from "node:test";

import {analyser} from "./client.mjs";

const url = "http://127.0.0.1:8000";
const cle = "une-cle-fictive-test";
const texte = "Très bien";

test("le client envoie le texte et la clé au bon endpoint", async () => {
  const verdict = {label: "POSITIVE", score: 0.77, text: texte};
  const resultat = await analyser(url, cle, texte, async (route, options) => {
    assert.equal(route.href, url + "/v1/predict");
    assert.equal(options.method, "POST");
    assert.equal(options.headers["X-API-Key"], cle);
    assert.deepEqual(JSON.parse(options.body), {text: texte});
    return {ok: true, json: async () => verdict};
  });
  assert.deepEqual(resultat, verdict);
});

for (const [status, message] of [[401, "Clé refusée"], [422, "Avis invalide"], [503, "Modèle absent"]]) {
  test("affiche le message de l’API pour HTTP " + status, async () => {
    await assert.rejects(analyser(url, cle, texte, async () => ({
      ok: false,
      status,
      json: async () => ({erreur: {message}}),
    })), {message});
  });
}

test("une erreur réseau remonte comme telle", async () => {
  await assert.rejects(analyser(url, cle, texte, async () => {
    throw new TypeError("network");
  }), TypeError);
});
