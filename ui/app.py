"""Interface Streamlit pour l'analyse d'un avis ou d'un CSV."""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ui import client  # noqa: E402

st.set_page_config(page_title="Analyse de sentiment")
st.title("Analyse de sentiment des avis")

with client.creer_session() as session:
    etat = client.sante(session)
    if etat.ok:
        st.caption(f"API prête : {etat.message}")
    else:
        st.error(etat.message)

    onglet_avis, onglet_lot = st.tabs(["Un avis", "Un fichier d'avis"])

    with onglet_avis:
        texte = st.text_area("Avis client")
        if st.button("Analyser"):
            reponse = client.predire(session, texte)
            if reponse.ok and reponse.label is not None and reponse.score is not None:
                st.metric(client.VERDICTS[reponse.label], f"{reponse.score:.0%}")
                if reponse.label == "INDETERMINE":
                    st.info("La confiance est sous le seuil d'abstention : un humain doit trancher.")
            elif reponse.message == client.REFUS:
                st.warning(reponse.message)
            else:
                st.error(reponse.message)

    with onglet_lot:
        fichier = st.file_uploader("Fichier CSV avec une colonne text", type="csv")
        if fichier is not None:
            try:
                avis = pd.read_csv(fichier, dtype={"text": str}, keep_default_na=False)
            except (ValueError, UnicodeError):
                st.error("Le fichier ne peut pas être lu comme un CSV UTF-8.")
                st.stop()
            if "text" not in avis.columns:
                st.error("Colonne text absente du fichier.")
                st.stop()

            reponses = client.predire_lot(session, avis["text"].tolist())
            avis["verdict"] = [
                client.VERDICTS[r.label] if r.ok and r.label else r.message for r in reponses
            ]
            avis["confiance"] = [r.score for r in reponses]
            st.dataframe(avis, use_container_width=True)
            st.write(client.resumer(reponses))
            classes = avis.loc[avis["confiance"].notna()]
            if not classes.empty:
                st.subheader("Répartition des verdicts")
                st.bar_chart(classes["verdict"].value_counts())
                st.subheader("Distribution de la confiance")
                tranches = pd.cut(
                    classes["confiance"], bins=[0.5, 0.6, 0.7, 0.8, 0.9, float("inf")],
                    right=False, labels=["50 à 59 %", "60 à 69 %", "70 à 79 %",
                                         "80 à 89 %", "90 à 100 %"],
                )
                st.bar_chart(tranches.value_counts(sort=False))
                st.caption("Sous 60 %, un humain doit vérifier l’avis.")
            st.download_button("Télécharger les résultats", avis.to_csv(index=False),
                               file_name="resultats.csv", mime="text/csv")
