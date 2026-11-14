# Qualité : résultats mesurés le 14 novembre 2026

## Départ
Les premiers essais Windows ont échoué à charger une extension scikit-learn, bloquée par Smart App Control.
Une réinstallation depuis PyPI des mêmes versions a résolu le problème sans changer les protections.
Aucune couverture initiale exploitable du modèle n'est revendiquée pour cet état bloqué.

## Corrections vérifiées
- Validation des textes blancs dans le schéma, test paramétré et deux propriétés Hypothesis.
- Pannes ValueError et RuntimeError : 500, sans message interne.
- Classes inattendues : refus au démarrage ; modèle absent : FileNotFoundError.
- Labels transportés par Literal et TypedDict ; correspondance explicite.
- Clés, rôles et format d’erreur /v1 vérifiés avec des clés de test seulement.
- Couverture API mesurée : 99,25 %, seuil requis 95 %. Aucune exclusion de ligne ajoutée.
- Ruff et mypy vérifiés ; hook pre-commit installé localement. CI configurée, pas encore publiée.

## Abstention
Sur 58 avis de test : seuil 0,50 = 58 réponses, 7 erreurs, exactitude 0,879.
Seuil 0,60 = 42 réponses, 2 erreurs, exactitude 0,952 ; 16 avis à revoir par un humain.
Seuil 0,70 = 37 réponses sans erreur sur ces seuls exemples, mais 21 abstentions.
Nous conservons le seuil pédagogique 0,60. Ces résultats analysent le jeu de test ; une vraie
optimisation nécessiterait une validation séparée puis un nouveau test indépendant.

## Jeu d’or
20 avis proposés avec Codex : 11 prédictions correctes, 8 abstentions, 1 erreur franche déclarée.
L’avis négatif sur l’autonomie de la batterie est prédit POSITIVE (environ 0,68).
Il reste dans le CSV avec sa raison ; le test xfail strict signale sa correction future.
Ces avis doivent encore être validés par les membres (voir jeu-or-provenance.md).
Les abstentions ne sont pas présentées comme des classifications correctes.
