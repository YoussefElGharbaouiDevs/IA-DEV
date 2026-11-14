# Interface : vérification du 14 novembre 2026

L’interface appelle /v1 par HTTP avec API_KEY ; elle n’importe jamais le modèle.
Deux onglets : avis seul et CSV (colonne text), verdict, confiance et abstention.
Le test AppTest analyse un CSV de six avis et vérifie le tableau, deux graphiques et le bouton d’export.
CSV vide, colonne manquante, plus de 1000 lignes : erreurs lisibles ; texte blanc : refus.
API arrêtée : message de connexion ; clé invalide : message d’accès refusé.
Le graphique des classes montre la part renvoyée à un humain. La distribution de confiance
montre la dispersion des scores, mais ne mesure pas leur calibration ni leur justesse.
La roue contient aussi le client HTML disponible sur /web.
