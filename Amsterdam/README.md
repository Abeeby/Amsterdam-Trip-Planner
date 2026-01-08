# 🇳🇱 Amsterdam Trip Planner 2025

Application de planification de voyage d'étude à Amsterdam, développée en Python avec Tkinter.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Description

Cette application permet d'organiser un voyage d'étude à Amsterdam en gérant :
- **📅 Activités** : Planification des visites et sorties
- **💰 Budget** : Suivi des dépenses par catégorie
- **🏨 Hôtel** : Informations sur l'hébergement
- **🚂 Transport** : Planning des trajets aller/retour
- **👥 Participants** : Liste des voyageurs
- **✅ Checklist** : Liste des affaires à emporter

## 🎯 Objectifs pédagogiques

Ce projet démontre l'utilisation des **trois gestionnaires de layout** de Tkinter :

| Gestionnaire | Fichier | Utilisation |
|--------------|---------|-------------|
| **PLACE** | `home_frame.py` | Positionnement absolu pour le design créatif |
| **GRID** | `activities_frame.py`, `budget_frame.py`, `transport_frame.py` | Organisation en tableau |
| **PACK** | `hotel_frame.py`, `participants_frame.py` | Empilement vertical |
| **PACK + GRID** | `checklist_frame.py` | Combinaison des deux méthodes |

## 📁 Structure du projet

```
Amsterdam/
├── main.py                 # Point d'entrée de l'application
├── config.py               # Configuration et constantes
├── data_manager.py         # Gestion sauvegarde/chargement JSON
├── frames/
│   ├── __init__.py         # Package des frames
│   ├── home_frame.py       # Page d'accueil (PLACE)
│   ├── activities_frame.py # Planificateur activités (GRID)
│   ├── budget_frame.py     # Gestion budget (GRID)
│   ├── hotel_frame.py      # Infos hébergement (PACK)
│   ├── transport_frame.py  # Planning transport (GRID)
│   ├── participants_frame.py # Liste participants (PACK)
│   └── checklist_frame.py  # Checklist bagages (PACK + GRID)
├── data/
│   └── voyage_data.json    # Données sauvegardées (auto-généré)
├── README.md               # Ce fichier
├── requirements.txt        # Dépendances
└── .gitignore              # Fichiers ignorés par Git
```

## 🔧 Prérequis

- **Python 3.8+** (testé avec Python 3.10)
- **Tkinter** (inclus avec Python sur Windows/Mac)

### Vérifier votre version de Python

```bash
python --version
```

### Vérifier que Tkinter est installé

```bash
python -c "import tkinter; print('Tkinter OK')"
```

Sur **Ubuntu/Debian**, si Tkinter n'est pas installé :
```bash
sudo apt-get install python3-tk
```

## 🚀 Installation

1. **Cloner le dépôt**
```bash
git clone <url-du-repo>
cd Amsterdam
```

2. **Aucune dépendance externe requise !**  
   L'application utilise uniquement la bibliothèque standard Python.

## ▶️ Exécution

```bash
python main.py
```

Ou sur certains systèmes :
```bash
python3 main.py
```

## 📱 Fonctionnalités

### 🏠 Page d'accueil
- Compte à rebours jusqu'au départ
- Statistiques rapides (activités, budget, participants)
- Résumé du voyage

### 📅 Planificateur d'activités
- Ajouter/modifier/supprimer des activités
- Informations : date, lieu, horaire, prix
- Tri automatique par date

### 💰 Gestion du budget
- Définir le budget prévu
- Ajouter des dépenses par catégorie
- Visualiser la répartition
- Alerte si budget dépassé

### 🏨 Informations hôtel
- Coordonnées complètes
- Dates de check-in/check-out
- Numéro de réservation
- Services inclus

### 🚂 Planning transport
- Détails du trajet aller
- Détails du trajet retour
- Transports sur place

### 👥 Liste des participants
- Informations de contact
- Rôle dans le groupe
- Allergies/informations médicales

### ✅ Checklist
- Liste des affaires à emporter
- Catégories (Documents, Vêtements, etc.)
- Progression visuelle

## 💾 Sauvegarde des données

Les données sont automatiquement sauvegardées dans `data/voyage_data.json` :
- À chaque modification
- À la fermeture de l'application

## 🎨 Conventions de code

Ce projet respecte les conventions Python :
- **PEP 8** : Style de code
- **Docstrings** : Documentation des classes/fonctions
- **Type hints** : Annotations de types
- **Snake_case** : Nommage des variables et fonctions
- **PascalCase** : Nommage des classes

## 📚 Structure des données JSON

```json
{
  "voyage_info": {
    "destination": "Amsterdam",
    "date_depart": "2025-09-15",
    "date_retour": "2025-09-20"
  },
  "activites": [...],
  "budget": {
    "budget_prevu": 500,
    "depenses": [...]
  },
  "hotel": {...},
  "transport": {...},
  "participants": [...],
  "checklist": [...]
}
```

## 🔄 Workflow Git

```bash
# Initialisation (déjà fait)
git init

# Ajouter les fichiers
git add .

# Commit initial
git commit -m "Initial commit - Amsterdam Trip Planner"

# Commits suivants
git add .
git commit -m "Description des modifications"
```

## 🛠️ Personnalisation

### Modifier les dates du voyage
Éditez `config.py` :
```python
DATE_DEPART = "2025-09-15"
DATE_RETOUR = "2025-09-20"
```

### Modifier les catégories de budget
Éditez `config.py` :
```python
BUDGET_CATEGORIES = [
    "Transport",
    "Hébergement",
    "Nourriture",
    # Ajoutez vos catégories...
]
```

## 📝 Licence

Ce projet est développé dans le cadre d'un exercice pédagogique.

## 👥 Auteurs

Projet réalisé pour le voyage d'étude à Amsterdam 2025.

AMIN TORRISI ET KODJO ATTIVON

---



