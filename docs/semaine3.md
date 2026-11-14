# API : vérification du 14 novembre 2026

FastAPI charge le modèle au démarrage ; aucune phase d’apprentissage pendant une requête.
GET /health et /v1/health : 200 ; prédictions positives et négatives : 200.
Champ absent, numérique, vide ou blanc : 422. Le validateur utilise str.strip(), y compris les blancs Unicode.
Modèle absent : démarrage refusé ; modèle retiré : 503 ; panne interne : 500 sans détail privé.
Le modèle est chargé depuis le paquet installé, sans modification de sys.path dans api/.
Les routes /v1 requièrent une clé client/admin, sauf la route de santé publique.
Les essais sont automatisés dans tests/test_api.py et tests/test_integration.py.
