# Amsterdam Trip Planner

Application de planification de voyage a Amsterdam developpee en Python avec Tkinter.

## Description

Cette application permet de planifier et organiser un voyage a Amsterdam. Elle offre plusieurs fonctionnalites pour gerer tous les aspects du voyage.

## Fonctionnalites

- **Accueil** : Vue d'ensemble du voyage avec compte a rebours
- **Activites** : Planification des activites et visites
- **Budget** : Suivi des depenses par categorie
- **Hotel** : Informations sur l'hebergement
- **Transport** : Gestion des trajets aller/retour et transports locaux
- **Participants** : Liste des voyageurs avec leurs informations
- **Checklist** : Liste des affaires a emporter

## Pre-requis

- Python 3.x
- Tkinter (inclus avec Python)

## Installation

1. Cloner le repository :
```bash
git clone <url-du-repository>
```

2. Naviguer dans le dossier du projet :
```bash
cd Amsterdam_new
```

3. Lancer l'application :
```bash
python Amsterdam/main.py
```

## Structure du projet

```
Amsterdam_new/
├── Amsterdam/
│   ├── main.py              # Point d'entree de l'application
│   ├── config.py            # Configuration et constantes
│   ├── data_manager.py      # Gestion des donnees (JSON)
│   ├── data/
│   │   └── voyage_data.json # Fichier de sauvegarde des donnees
│   └── frames/
│       ├── home_frame.py        # Page d'accueil (PLACE)
│       ├── activities_frame.py  # Gestion des activites (GRID)
│       ├── budget_frame.py      # Gestion du budget (GRID)
│       ├── hotel_frame.py       # Informations hotel (PACK)
│       ├── transport_frame.py   # Gestion des transports (GRID)
│       ├── participants_frame.py # Gestion des participants (PACK)
│       └── checklist_frame.py   # Checklist des affaires (PACK + GRID)
└── README.md
```

## Gestionnaires de Layout Tkinter

Ce projet utilise les trois gestionnaires de layout de Tkinter :

### PLACE
Utilise dans `home_frame.py` pour un positionnement absolu et relatif des widgets.
```python
widget.place(relx=0.5, rely=0.3, anchor="center")
```

### GRID
Utilise dans `activities_frame.py`, `budget_frame.py` et `transport_frame.py` pour organiser les widgets en lignes et colonnes.
```python
widget.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
```

### PACK
Utilise dans `hotel_frame.py` et `participants_frame.py` pour empiler les widgets verticalement ou horizontalement.
```python
widget.pack(fill="x", padx=10, pady=5)
```

### PACK + GRID (mixte)
Utilise dans `checklist_frame.py` pour combiner les deux approches :
- PACK pour la structure generale
- GRID pour les formulaires internes

## Architecture

L'application utilise une architecture fonctionnelle (sans classes) avec :

- **data_manager.py** : Module de gestion des donnees avec variable globale `_data`
- **Frames** : Fonctions qui creent et retournent des frames tkinter configures
- **Callbacks** : Fonctions modulaires pour gerer les evenements utilisateur

## Sauvegarde des donnees

Les donnees sont sauvegardees automatiquement dans le fichier `data/voyage_data.json` au format JSON.

## Module I319

Projet realise dans le cadre du module I319.

### Conventions respectees
- Utilisation des trois gestionnaires de layout (pack, grid, place)
- Code Python sans POO (programmation orientee objet)
- Gestion avec Git
- Documentation README

## Auteur

Projet etudiant - Module I319
