# Détection de Communautés avec Datalog & Clingo

Ce projet implémente un système de détection de communautés dans les réseaux sociaux utilisant **Datalog** (via le moteur **Clingo**) pour la logique et une interface Web moderne (**React** + **Flask**) pour la visualisation.

##  Structure du Projet

- `backend/` : API Flask et logique Datalog.
  - `logic/rules/` : Règles ASP/Datalog (`label_propagation.lp`).
  - `engines/` : Moteur d'exécution Clingo.
  - `data/` : Datasets (Karate Club, etc.).
- `frontend/` : Interface Utilisateur React.
- `docs/` : Rapport et documentation technique.

##  Installation et Lancement

### Pré-requis
- Python 3.8+
- Node.js 16+
- Clingo (`pip install clingo`)

### 1. Démarrer le Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Le serveur Backend sera accessible sur `http://localhost:5000`.

### 2. Démarrer le Frontend
```bash
cd frontend
npm install
npm run dev
```
Ouvrez votre navigateur sur `http://localhost:5173`.

##  Fonctionnalités
1.  **Liste des Datasets** : Le graphe "Karate Club" est disponible par défaut.
2.  **Analyse** : Lancer l'algorithme "Label Propagation" implémenté en ASP.
3.  **Visualisation** : Voir les communautés détectées avec des couleurs distinctes.

