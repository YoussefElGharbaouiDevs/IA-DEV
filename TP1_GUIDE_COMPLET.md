# TP1: Cadrer l'Application et Préparer l'Environnement
## Guide Complet pour Démarrer

**Durée estimée:** 2 heures (binôme)

---

## 📋 Objectifs de TP1

Après ce TP, vous aurez:
1. ✅ Un environnement Python 3.11 isolé et fonctionnel
2. ✅ Un dépôt Git partagé entre 2 membres
3. ✅ 3 fiches de cadrage justifiées pour 3 cas d'usage
4. ✅ Tous les tests verts: **38 passed**

---

## 🏗️ Architecture du Projet Global

Voici ce que vous allez construire en 5 semaines:

```
SEMAINE 1 (TP1): Cadrage + Environnement
    ↓
SEMAINE 2 (TP2): Entraîner le modèle ML
    ↓
SEMAINE 3 (TP3): Créer l'API FastAPI
    ↓
SEMAINE 4 (TP4): Tests approfondis + Qualité
    ↓
SEMAINE 5 (TP5): Interface Streamlit
    ↓
RÉSULTAT: Système complet de classification d'avis clients
```

**TP1 pose les fondations solides pour tout le reste.**

---

## 📖 ÉTAPE 1: Récupérer et Extraire le Kit

### Qu'est-ce que c'est?
Le kit est une archive ZIP contenant la **structure complète** du projet: dossiers, fichiers, tests, et données.

### Commandes PowerShell

```powershell
# Crée le dossier racine
New-Item -ItemType Directory -Force C:\IA-DEV

# Extrait l'archive ZIP
Expand-Archive "$HOME\Downloads\sentiment-app-main.zip" `
  -DestinationPath C:\IA-DEV -Force

# Renomme pour simplifier
Rename-Item C:\IA-DEV\sentiment-app-main sentiment-app

# Rentre dedans
cd C:\IA-DEV\sentiment-app

# Vérifie la structure
Get-ChildItem -Force
```

### Résultat attendu (T0)

```
Mode  Name
----  ----
d---  app              # Sera utilisé à partir de TP3
d---  data             # Données de démonstration
d---  docs             # Documentation (vos fiches vont ici)
d---  models           # Où le modèle sera sauvegardé
d---  scripts          # Utilitaires (check_setup.py, etc.)
d---  tests            # Tests automatisés
d---  ui               # Interface Streamlit (TP5)
d---  .github          # Configuration CI/CD GitHub
-a--  .gitignore       # Fichiers à ignorer par Git
```

**✅ Si tu vois ces 7 dossiers + 2 fichiers cachés, tu es bon!**

---

## 🐍 ÉTAPE 2: Préparer l'Environnement Python

### Pourquoi un environnement virtuel?

Imagine que tu as 10 projets différents sur ton ordinateur, et chacun a besoin d'une version différente de Python ou de librairies. **Sans environnement isolé, c'est le chaos.**

Avec un **environnement virtuel** (.venv):
- Chaque projet a ses propres dépendances
- Versions peuvent différer sans conflit
- Se supprime facilement: `rm -r .venv`

### Commandes

```powershell
# Étape 2a: Vérifier Python et Git
py -0                    # Liste les Python installés
py -3.11 --version       # Doit afficher Python 3.11.x
git --version            # Doit afficher git version 2.x

# Étape 2b: Créer l'environnement virtuel
py -3.11 -m venv .venv

# Étape 2c: L'activer
.venv\Scripts\Activate.ps1
# L'invite doit commencer par (.venv)

# Étape 2d: Installer les dépendances
python -m pip install --upgrade pip
pip install -r requirements.txt      # Ça prend 5-10 min!

# Geler les versions pour reproductibilité
python -m pip freeze | Out-File -Encoding utf8 requirements.lock
```

### Vérifications

```powershell
# Vérifie que tout est installé
python scripts/check_setup.py

# Résultat attendu:
# ✅ Python 3.11
# ✅ pip installé
# ✅ Git installé
# ✅ 45+ paquets présents
# 0 erreur(s), 0 avertissement(s)

# Lance les tests (beaucoup vont échouer, c'est normal)
python -m pytest -q
# Résultat attendu (T1): 3 failed, 31 passed, 4 skipped
```

**Important:** Les 3 tests échouent parce que les **fiches de cadrage sont vides**. C'est normal à ce stade.

---

## 📝 ÉTAPE 3: Remplir les Fiches de Cadrage

### Pourquoi des fiches?

Avant de coder, tu dois répondre à des questions critiques:
- Quel problème résolvez-vous?
- Quelles données avez-vous?
- Quelle approche choisissez-vous et **pourquoi**?

**Les fiches forcent cette réflexion.**

### Structure d'une Fiche

**Fichiers à remplir:**
- `docs/cadrage/cas1-pharmacie.md`
- `docs/cadrage/cas2-reglement.md`
- `docs/cadrage/cas3-avisnegatifs.md`

**Contenu minimum de chaque fiche:**

```markdown
## Contexte
[Décrivez le cas d'usage en 3-4 phrases]
Exemple: Les pharmaciens reçoivent des avis clients...

## Les données
[Décrivez: où, combien, comment étiquetées?]
Exemple: 500 avis de clients, étiquetés positif/négatif...

## Approche retenue
Cochez UNE SEULE case:
- [ ] Apprentissage supervisé
- [ ] Apprentissage non-supervisé
- [ ] Heuristique simple

## Justification
[Expliquez votre choix en citant AU MOINS 2 critères]

Les 4 critères disponibles:
(a) Données étiquetées, modèle ML supervisé possible
(b) Vérifiabilité de chaque prédiction par humain
(c) Coût par requête faible (important à l'échelle)
(d) Conséquence d'une erreur grave (sécurité, confiance)

Exemple de bonne justification:
"J'ai choisi apprentissage supervisé (✓) car:
 - (a) Nous avons 500 avis étiquetés par les propriétaires
 - (d) Une mauvaise classification nuirait à la réputation"
```

### Commandes

```powershell
# Ouvre l'éditeur pour chaque fiche
notepad docs\cadrage\cas1-pharmacie.md
notepad docs\cadrage\cas2-reglement.md
notepad docs\cadrage\cas3-avisnegatifs.md
```

### Tests

```powershell
# Après avoir rempli les 3 fiches
python -m pytest tests/test_cadrage.py -q

# Résultat attendu (T2): 34 passed, 4 skipped
# Les 3 tests des fiches doivent maintenant passer!
```

---

## 🔗 ÉTAPE 4: Créer le Dépôt GitHub

### Sur GitHub (Navigateur)

1. Va à https://github.com/new
2. **Repository name:** `sentiment-app`
3. **Private:** ✅ Cocher (projet étudiant privé)
4. **Initialize this repository with:** Ne cocher RIEN
5. Click "Create repository"

### Local: Initialiser Git

```powershell
# Initialise Git
git init

# Ajoute tous les fichiers
git add -A

# Vérifie avant de commiter
git status
# Tu dois voir: "On branch master" ou "On branch main"

# Premier commit
git commit -m "TP1 : environnement, structure et cadrage"

# Renomme en "main" si besoin
git branch -M main

# Ajoute le dépôt distant (remplace TONCOMPTE)
git remote add origin https://github.com/TONCOMPTE/sentiment-app.git

# Envoie les fichiers
git push -u origin main
```

### Invite les Collaborateurs sur GitHub

1. Va sur ton dépôt
2. Settings → Collaborators → Add people
3. Invite le membre B
4. Invite l'enseignant: `Larhlimiabd-ai`

---

## 👥 ÉTAPE 5-6: Collaboration Binôme

### Membre B: Clone et Contribue

```powershell
# Clone le dépôt
cd C:\IA-DEV
git clone https://github.com/TONCOMPTE/sentiment-app.git sentiment-app
cd sentiment-app

# Prépare l'environnement
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# IMPORTANT: Configure GIT LOCALEMENT (pas --global!)
git config user.name "Prénom Nom B"
git config user.email "prenom.nom.b@ecole.ma"

# Fait une modification
notepad README.md                    # Ajoute une ligne avec son nom
git add README.md
git commit -m "README: ajout de [Nom B]"
git push
```

### Membre A: Valide et Confirme

```powershell
# Récupère le changement de B
cd C:\IA-DEV\sentiment-app
git pull

# Ajoute aussi sa ligne
notepad README.md

# Configure GIT LOCALEMENT
git config user.name "Aya Larhlimi"
git config user.email "aya.larhlimi@ecole.ma"

# Commit avec son identité
git add README.md
git commit -m "README: ajout de Aya Larhlimi"
git push

# Vérifie les 2 auteurs
git shortlog -sn --all         # Doit afficher 2 noms distincts
```

### Tests de Collaboration

```powershell
python -m pytest tests/test_git_history.py -q
# Résultat attendu (T5-T6): 3 passed
# Prouve qu'il y a 2 auteurs distincts
```

---

## ✅ ÉTAPE 7: Vérification Finale

```powershell
# Mise à jour
git pull

# Vérification
python scripts/check_setup.py
python -m pytest -q

# Résultat attendu (T6):
# ✅ 0 erreur(s), 0 avertissement(s)
# ✅ 38 passed
# ✅ GitHub Actions: VERT
```

---

## 🔄 ÉTAPE 8: Clone Frais (Test Final)

Simule un nouvel étudiant qui clone le dépôt pour la première fois:

```powershell
cd $env:TEMP
git clone https://github.com/TONCOMPTE/sentiment-app.git verif
cd verif
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/check_setup.py
python -m pytest -q

# Résultat attendu (T7):
# ✅ 38 passed
# Prouve que le dépôt est complet et prêt à être partagé
```

---

## 📚 Résumé Récapitulatif

| Étape | Qu'est-ce? | Durée | Résultat |
|-------|-----------|-------|----------|
| 1 | Extraire le kit | 2 min | 7 dossiers + 2 fichiers |
| 2 | Environnement Python | 15 min | .venv fonctionnel, 45+ paquets |
| 3 | Fiches cadrage | 30 min | 3 cas d'usage documentés |
| 4 | Dépôt GitHub | 5 min | Dépôt créé et versionné |
| 5-6 | Collaboration | 20 min | 2 auteurs distincts |
| 7-8 | Vérification | 10 min | 38 tests passants |
| **Total** | | **82 min** | **TP1 COMPLET** |

---

## 🔧 Troubleshooting Courant

### Problème: Python 3.11 non trouvé

```powershell
# Vérifier les versions installées
py -0

# Si absent, installer avec winget
winget install Python.Python.3.11
```

### Problème: `.venv\Scripts\Activate.ps1` refuse de s'exécuter

```powershell
# Autoriser temporairement les scripts PowerShell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# Essayer à nouveau
.venv\Scripts\Activate.ps1
```

### Problème: Git push échoue avec "remote not found"

```powershell
# Supprimer les credentials en cache
cmdkey /delete:git:https://github.com

# Essayer git push à nouveau
git push
```

### Problème: Encodage CSV incorrect (accents cassés)

```powershell
# Utiliser Python pour créer les fichiers (garantit UTF-8)
python -c "
import csv
with open('docs/cadrage/cas1-pharmacie.md', 'w', encoding='utf-8') as f:
    f.write('contenu...')
"
```

---

## 💡 Conseils Importants

1. **Ne renommez pas les dossiers** - la structure est critique pour les tests
2. **Activez le .venv à chaque session** - `.venv\Scripts\Activate.ps1`
3. **Configurez Git LOCALEMENT** - sans `--global` pour le binôme
4. **Sauvegardez requirements.lock** - montre exactement quelles versions vous aviez
5. **Committez souvent** - Git permet de revenir en arrière
6. **Lisez les erreurs de test** - elles vous disent exactement quoi corriger

---

## 📖 Références

- **Python 3.11**: https://www.python.org/downloads/
- **Git**: https://git-scm.com/
- **GitHub**: https://github.com/
- **PowerShell Guide**: https://docs.microsoft.com/en-us/powershell/

---

## ✨ Prochaines Étapes

Une fois TP1 complété, passez à **TP2**:
- Générer des données de démonstration
- Entraîner un modèle TF-IDF + Régression logistique
- Évaluer sur un ensemble de test
- Sauvegarder métriques et modèle

**Bonne chance!** 🚀
