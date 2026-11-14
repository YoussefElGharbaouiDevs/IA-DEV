import {analyser} from "./client.mjs";

const formulaire = document.querySelector("form");
const resultat = formulaire.querySelector("output");
const bouton = formulaire.querySelector("button");
const verdicts = {
  POSITIVE: "Avis positif",
  NEGATIVE: "Avis négatif",
  INDETERMINE: "À faire vérifier par un humain",
};

formulaire.addEventListener("submit", async (event) => {
  event.preventDefault();
  const donnees = new FormData(formulaire);
  bouton.disabled = true;
  resultat.textContent = "Analyse en cours…";
  try {
    const {label, score} = await analyser(donnees.get("url"), donnees.get("cle"), donnees.get("texte"));
    resultat.textContent = `${verdicts[label]} · ${Math.round(score * 100)} %`;
  } catch (erreur) {
    resultat.textContent = erreur instanceof TypeError ? "API injoignable" : erreur.message;
  } finally {
    bouton.disabled = false;
  }
});
