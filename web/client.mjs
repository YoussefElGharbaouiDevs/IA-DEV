export async function analyser(url, cle, texte, envoyer = fetch) {
  const reponse = await envoyer(new URL("/v1/predict", url), {
    method: "POST",
    headers: {"Content-Type": "application/json", "X-API-Key": cle},
    body: JSON.stringify({text: texte}),
  });
  const corps = await reponse.json();
  if (!reponse.ok) {
    throw new Error(corps.erreur?.message ?? `Erreur HTTP ${reponse.status}`);
  }
  return corps;
}
