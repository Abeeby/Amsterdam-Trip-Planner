"""
config.py - Configuration et constantes de l'application Amsterdam Trip Planner.

Ce module contient toutes les constantes et configurations utilisees
dans l'ensemble de l'application. Centraliser ces valeurs permet de
les modifier facilement sans toucher au code des autres modules.
"""

import os
from datetime import datetime

# ============================================
# INFORMATIONS DU VOYAGE
# ============================================

# Destination du voyage
DESTINATION = "Amsterdam"

# Dates du voyage (format: AAAA-MM-JJ)
DATE_DEPART = "2025-09-15"
DATE_RETOUR = "2025-09-20"

# ============================================
# CONFIGURATION DE LA FENETRE PRINCIPALE
# ============================================

# Titre de l'application
APP_TITLE = "Voyage d'etude - Amsterdam 2025"

# Dimensions de la fenetre principale (largeur x hauteur)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 850

# Dimensions minimales de la fenetre
MIN_WIDTH = 800
MIN_HEIGHT = 600

# ============================================
# CHEMINS DES FICHIERS
# ============================================

# Repertoire de base de l'application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Repertoire des donnees
DATA_DIR = os.path.join(BASE_DIR, "data")

# Fichier de sauvegarde des donnees JSON
DATA_FILE = os.path.join(DATA_DIR, "voyage_data.json")

# ============================================
# COULEURS DE L'APPLICATION
# ============================================

# Couleurs inspirees du drapeau neerlandais et d'Amsterdam
COLORS = {
    "primary": "#023047",      # blue (couleur nationale)
    "secondary": "#1E3A5F",    # Bleu fonce
    "accent": "#F7C948",       # Jaune/Or
    "background": "#F5F5F5",   # Gris clair
    "text": "#333333",         # Texte fonce
    "text_light": "#FFFFFF",   # Texte clair
    "success": "#28A745",      # Vert pour succes
    "warning": "#FFC107",      # Jaune pour avertissement
    "danger": "#DC3545",       # Rouge pour danger/erreur
    "border": "#CCCCCC",       # Bordures
}

# ============================================
# POLICES DE CARACTERES
# ============================================

FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "subtitle": ("Segoe UI", 16, "bold"),
    "heading": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 11),
    "body_bold": ("Segoe UI", 11, "bold"),
    "small": ("Segoe UI", 9),
    "button": ("Segoe UI", 10, "bold"),
}

# ============================================
# CATEGORIES DE BUDGET
# ============================================

BUDGET_CATEGORIES = [
    "Transport",
    "Hebergement",
    "Nourriture",
    "Activites",
    "Shopping",
    "Autre"
]

# ============================================
# CATEGORIES DE CHECKLIST
# ============================================

CHECKLIST_CATEGORIES = [
    "Documents",
    "Vetements",
    "Electronique",
    "Hygiene",
    "Medicaments",
    "Autre"
]

# ============================================
# TYPES DE TRANSPORT
# ============================================

TRANSPORT_TYPES = [
    "Avion",
    "Train",
    "Bus",
    "Voiture",
    "Metro",
    "Tramway",
    "Velo",
    "A pied"
]

# ============================================
# ROLES DES PARTICIPANTS
# ============================================

PARTICIPANT_ROLES = [
    "Organisateur",
    "Accompagnateur",
    "Participant",
    "Responsable budget",
    "Responsable activites"
]

# ============================================
# DONNEES PAR DEFAUT
# ============================================

DEFAULT_DATA = {
    "voyage_info": {
        "destination": DESTINATION,
        "date_depart": DATE_DEPART,
        "date_retour": DATE_RETOUR,
        "description": "Voyage d'etude a Amsterdam pour decouvrir la culture neerlandaise"
    },
    "activites": [
        {
            "id": 1,
            "date": "2025-09-15",
            "nom": "Visite du Rijksmuseum",
            "lieu": "Museumstraat 1",
            "horaire": "10:00",
            "duree": "3h",
            "prix": 22.50,
            "description": "Musee national avec les oeuvres de Rembrandt et Vermeer"
        },
        {
            "id": 2,
            "date": "2025-09-16",
            "nom": "Maison d'Anne Frank",
            "lieu": "Prinsengracht 263-267",
            "horaire": "09:00",
            "duree": "2h",
            "prix": 16.00,
            "description": "Visite historique de la cachette d'Anne Frank"
        },
        {
            "id": 3,
            "date": "2025-09-17",
            "nom": "Croisiere sur les canaux",
            "lieu": "Damrak",
            "horaire": "14:00",
            "duree": "1h30",
            "prix": 18.00,
            "description": "Decouverte de la ville depuis les canaux"
        }
    ],
    "budget": {
        "budget_prevu": 500.00,
        "devise": "EUR",
        "depenses": [
            {
                "id": 1,
                "date": "2025-09-15",
                "categorie": "Transport",
                "montant": 150.00,
                "description": "Billet de train aller-retour",
                "participant": "Groupe"
            }
        ]
    },
    "hotel": {
        "nom": "Hotel Amsterdam Centre",
        "adresse": "Damrak 93-94, 1012 LP Amsterdam",
        "telephone": "+31 20 555 0000",
        "email": "info@hotelamsterdam.nl",
        "site_web": "www.hotelamsterdam.nl",
        "date_checkin": "2025-09-15",
        "heure_checkin": "15:00",
        "date_checkout": "2025-09-20",
        "heure_checkout": "11:00",
        "numero_reservation": "AMS-2025-001",
        "nombre_chambres": 5,
        "type_chambre": "Double",
        "petit_dejeuner": True,
        "wifi": True,
        "notes": "Situe au centre-ville, proche de la gare centrale"
    },
    "transport": {
        "aller": {
            "type": "Train",
            "compagnie": "Thalys",
            "numero": "THA 9321",
            "depart_lieu": "Paris Gare du Nord",
            "depart_date": "2025-09-15",
            "depart_heure": "07:25",
            "arrivee_lieu": "Amsterdam Centraal",
            "arrivee_heure": "10:44",
            "place": "Voiture 12",
            "notes": "Rendez-vous a la gare a 06:45"
        },
        "retour": {
            "type": "Train",
            "compagnie": "Thalys",
            "numero": "THA 9346",
            "depart_lieu": "Amsterdam Centraal",
            "depart_date": "2025-09-20",
            "depart_heure": "17:17",
            "arrivee_lieu": "Paris Gare du Nord",
            "arrivee_heure": "20:41",
            "place": "Voiture 8",
            "notes": "Prevoir d'etre a la gare a 16:30"
        },
        "sur_place": [
            {
                "type": "Metro",
                "description": "Abonnement GVB 5 jours",
                "prix": 40.50
            }
        ]
    },
    "participants": [
        {
            "id": 1,
            "nom": "Dupont",
            "prenom": "Marie",
            "email": "marie.dupont@email.com",
            "telephone": "06 12 34 56 78",
            "role": "Organisateur",
            "date_naissance": "2000-05-15",
            "allergies": "",
            "notes": "Responsable du groupe"
        },
        {
            "id": 2,
            "nom": "Martin",
            "prenom": "Lucas",
            "email": "lucas.martin@email.com",
            "telephone": "06 98 76 54 32",
            "role": "Responsable budget",
            "date_naissance": "2001-03-22",
            "allergies": "Arachides",
            "notes": "Gere les depenses du groupe"
        }
    ],
    "checklist": [
        {"id": 1, "item": "Passeport/Carte d'identite", "categorie": "Documents", "checked": False},
        {"id": 2, "item": "Carte europeenne d'assurance maladie", "categorie": "Documents", "checked": False},
        {"id": 3, "item": "Billets de train", "categorie": "Documents", "checked": False},
        {"id": 4, "item": "Confirmation hotel", "categorie": "Documents", "checked": False},
        {"id": 5, "item": "Vetements pour 5 jours", "categorie": "Vetements", "checked": False},
        {"id": 6, "item": "Veste impermeable", "categorie": "Vetements", "checked": False},
        {"id": 7, "item": "Chaussures confortables", "categorie": "Vetements", "checked": False},
        {"id": 8, "item": "Chargeur telephone", "categorie": "Electronique", "checked": False},
        {"id": 9, "item": "Appareil photo", "categorie": "Electronique", "checked": False},
        {"id": 10, "item": "Batterie externe", "categorie": "Electronique", "checked": False},
        {"id": 11, "item": "Brosse a dents", "categorie": "Hygiene", "checked": False},
        {"id": 12, "item": "Medicaments personnels", "categorie": "Medicaments", "checked": False}
    ]
}

# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def get_days_until_departure():
    """
    Calcule le nombre de jours restants avant le depart.

    Returns:
        Nombre de jours avant le depart (negatif si deja passe)
    """
    departure = datetime.strptime(DATE_DEPART, "%Y-%m-%d")
    today = datetime.now()
    delta = departure - today
    return delta.days


def format_date(date_str, format_input="%Y-%m-%d", format_output="%d/%m/%Y"):
    """
    Convertit une date d'un format a un autre.

    Args:
        date_str: La date en chaine de caracteres
        format_input: Le format d'entree (par defaut: AAAA-MM-JJ)
        format_output: Le format de sortie (par defaut: JJ/MM/AAAA)

    Returns:
        La date formatee
    """
    try:
        date_obj = datetime.strptime(date_str, format_input)
        return date_obj.strftime(format_output)
    except ValueError:
        return date_str


def format_currency(amount, currency="EUR"):
    """
    Formate un montant en devise.

    Args:
        amount: Le montant a formater
        currency: La devise (par defaut: EUR)

    Returns:
        Le montant formate (ex: "25,50 EUR")
    """
    if currency == "EUR":
        return f"{amount:,.2f} EUR".replace(",", " ").replace(".", ",")
    return f"{amount:,.2f} {currency}"
