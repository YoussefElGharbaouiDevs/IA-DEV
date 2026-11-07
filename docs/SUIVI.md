# Suivi du travail — TP1 puis TP2

**Dossier actif** : `C:\Users\ziade\Desktop\5IADO-tp2\sentiment-app`

## En cours

- Installation complète des dépendances terminée dans `.venv` (Python 3.11.15). Contrôle effectué : `All installed packages are compatible`. `requirements.lock` a été actualisé.
- Préparation du nouveau dépôt GitHub sous `elwafiZiad`. La connexion au compte dans le navigateur intégré est encore attendue.

## Contrôles terminés

| Étape | Résultat réellement observé |
| --- | --- |
| Extraction du kit | Double dossier corrigé ; kit vierge conservé avant reprise |
| TP1 — avant cadrage et avant Git | 3 failed, 31 passed, 4 skipped |
| TP1 — fiches de cadrage | 12 passed |
| TP1 — cadrage terminé, avant Git | 34 passed, 4 skipped |
| TP1 — premier commit du nouveau dépôt | 37 passed, 1 failed : second auteur absent |
| TP2 — installation du kit | 3 failed, 37 passed, 2 skipped : modèle absent et second auteur absent |
| TP2 — jeu de démonstration | 290 avis, 145 par classe |
| TP2 — entraînement de démonstration | F1 macro 0,8790 ; rappel négatif 0,9310 |
| TP2 — évaluation de démonstration | Matrice : 27 / 2 ; 5 / 24. Sept erreurs sur 58 avis |
| TP2 — entraînement Allociné | 16 000 avis d’entraînement, 4 000 de test ; F1 macro 0,9205 |
| TP2 — tests après Allociné | 41 passed, 1 failed : seul le contrôle du second auteur échoue |

## Fichiers préparés

- [Journal du professeur rempli pour les contrôles observés](journal-tp1-tp6.md).
- [Compte rendu et analyse des erreurs du TP2](semaine2.md).
- `preuves/` : commandes et sorties réellement enregistrées, en texte et JSON.
- `captures/` : onze captures de pages de lecture de ces sorties ; le journal précise leur nature.
- `models/metrics.json` : mesures Allociné à versionner.
- `models/sentiment.joblib` et `data/demo_reviews.csv` : produits localement, ignorés par Git.

## À terminer

1. Installation complète, compatibilité des dépendances et verrouillage des versions : terminés.
2. Créer et publier le nouveau dépôt après connexion GitHub.
3. Faire contribuer réellement un coéquipier avec son propre compte : les tests du cours exigent au moins deux auteurs. Aucun auteur fictif n’a été ajouté.
4. Vérifier la CI et le clone frais, puis compléter les preuves des postes A et B.

Les sections TP3 à TP6 du journal restent à réaliser.
