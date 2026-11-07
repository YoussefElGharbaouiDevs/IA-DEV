# Semaine 2 : modèle de sentiment

## Mesures réellement obtenues

Le pipeline du kit utilise TF-IDF sur les unigrammes et bigrammes, puis une régression logistique. Les données sont séparées avant l’ajustement du vectoriseur, avec une graine de 42 et une séparation stratifiée de 80 % / 20 %.

| Jeu | Entraînement | Test | F1 macro | Rappel négatif |
| --- | ---: | ---: | ---: | ---: |
| Démonstration | 232 | 58 | 0,8790 | 0,9310 |
| Allociné | 16 000 | 4 000 | 0,9205 | 0,9113 |

La matrice de confusion du jeu de démonstration est la suivante, avec les classes réelles en lignes et les prédictions en colonnes :

| Réel / prédit | Négatif | Positif |
| --- | ---: | ---: |
| Négatif | 27 | 2 |
| Positif | 5 | 24 |

Les sorties sources sont conservées dans `preuves/tp2-c3.txt`, `preuves/tp2-c4.txt`, `preuves/tp2-demo-metrics.json` et `preuves/tp2-c5-allocine.txt`. Le contrôle C5 a chargé 20 000 avis Allociné et appris un vocabulaire de 149 529 termes. Le F1 est meilleur sur ce jeu, mais les deux valeurs ne se comparent pas comme un progrès sur un même test : les données et le domaine sont différents.

## Analyse des erreurs

Les erreurs affichées portent sur des avis qui changent de sentiment en cours de phrase : par exemple, une plainte sur la taille et le retour est suivie de « sauf que ensuite produit conforme à la description, très satisfait », mais le modèle prédit négatif. Le pipeline reconnaît des mots et des groupes de deux mots ; il ne représente pas suffisamment la relation entre une première impression et la conclusion qui la renverse, et ne doit donc pas être interprété comme une compréhension de la phrase. Pour réduire ces erreurs, il faudrait évaluer davantage d’avis contrastés et comparer une représentation contextuelle, en conservant un jeu de test distinct pour mesurer le gain plutôt que de régler le modèle sur ces sept erreurs.

## Cadrage et limites

Le F1 macro de démonstration dépasse le seuil de 0,85, et le rappel des avis négatifs de 0,931 dépasse l’objectif de 0,90 fixé dans la fiche de cadrage. Ce petit jeu synthétique ne suffit pas à valider un usage réel en e-commerce ; Allociné contient des critiques de films et constitue aussi un domaine différent des avis marchands. Il faut donc distinguer la réussite du TP d’une validation métier sur les données du site.

## Reproductibilité et versionnage

Le pipeline complet est sauvegardé dans `models/sentiment.joblib`, afin de garder le vectoriseur et le classifieur ensemble. Ce fichier et `data/demo_reviews.csv` sont ignorés par Git ; `models/metrics.json` est versionné pour permettre la lecture des mesures et les tests de métriques en CI. Après l’entraînement Allociné, les commandes de démonstration sans `--allocine` permettront de retrouver le modèle attendu par les essais du TP3.

## État des tests et collaboration

Après entraînement sur le jeu de démonstration puis sur Allociné : **41 passed, 1 failed** dans les deux cas. Les quatre tests du modèle passent ; l’échec est `test_each_member_has_committed`, car ce nouveau dépôt n’a pour l’instant qu’un auteur, `elwafiZiad`. Un coéquipier doit y faire une contribution réelle sous sa propre identité avant de valider le contrôle de collaboration et obtenir les 42 tests verts.
