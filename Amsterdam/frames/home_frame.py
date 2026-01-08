"""
home_frame.py - Page d'accueil de l'application Amsterdam Trip Planner.

Ce module affiche un resume du voyage avec:
- Un compte a rebours jusqu'au depart
- Des statistiques rapides (activites, budget, participants)
- Des informations cles du voyage

IMPORTANT: Ce frame utilise le gestionnaire de layout PLACE
pour positionner les elements de maniere absolue.
"""

import tkinter as tk
from tkinter import ttk

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, get_days_until_departure, format_date, format_currency


# ============================================
# FONCTION POUR CREER UNE CARTE DE STATISTIQUE
# ============================================

def create_stat_card(parent, icon, title, value_var, subtitle):
    """
    Cree une carte de statistique.

    Args:
        parent: Le widget parent
        icon: L'emoji a afficher
        title: Le titre de la carte
        value_var: Variable pour la valeur
        subtitle: Le sous-titre

    Returns:
        Le frame de la carte creee
    """
    card = tk.Frame(
        parent,
        bg="white",
        padx=20,
        pady=15,
        relief="solid",
        bd=1
    )

    # Stocker la variable de valeur dans le frame
    card.value_var = value_var

    # Icon
    tk.Label(
        card,
        text=icon,
        font=("Segoe UI Emoji", 32),
        bg="white"
    ).pack()

    # Titre
    tk.Label(
        card,
        text=title,
        font=FONTS["body_bold"],
        bg="white",
        fg=COLORS["text"]
    ).pack()

    # Valeur
    tk.Label(
        card,
        textvariable=value_var,
        font=("Segoe UI", 24, "bold"),
        bg="white",
        fg=COLORS["primary"]
    ).pack()

    # Sous-titre
    tk.Label(
        card,
        text=subtitle,
        font=FONTS["small"],
        bg="white",
        fg="#666666"
    ).pack()

    return card


# ============================================
# FONCTIONS POUR LE CANVAS ET DECORATIONS
# ============================================

def draw_decorations_delayed(frame, canvas):
    """
    Dessine les decorations apres que le canvas soit dimensionne.

    Args:
        frame: Le frame parent
        canvas: Le canvas sur lequel dessiner
    """
    # Obtenir les dimensions
    width = frame.winfo_width()
    height = frame.winfo_height()

    if width <= 1 or height <= 1:
        # Le widget n'est pas encore affiche, reessayer
        frame.after(100, lambda: draw_decorations_delayed(frame, canvas))
        return

    # Dessiner des cercles decoratifs
    # Cercle en haut a gauche
    canvas.create_oval(
        -50, -50, 100, 100,
        fill=COLORS["primary"],
        outline=""
    )

    # Cercle en bas a droite
    canvas.create_oval(
        width - 100, height - 100,
        width + 50, height + 50,
        fill=COLORS["secondary"],
        outline=""
    )


# ============================================
# FONCTION POUR LE COMPTE A REBOURS
# ============================================

def update_countdown(frame, countdown_var):
    """
    Met a jour le compte a rebours.

    Args:
        frame: Le frame parent (pour planifier la prochaine mise a jour)
        countdown_var: La variable StringVar pour afficher le resultat
    """
    days = get_days_until_departure()

    if days > 0:
        countdown_var.set(f"{days} jours")
    elif days == 0:
        countdown_var.set("C'est aujourd'hui !")
    else:
        countdown_var.set(f"Passe ({-days} jours)")

    # Planifier la prochaine mise a jour (toutes les heures)
    frame.countdown_job = frame.after(3600000, lambda: update_countdown(frame, countdown_var))


# ============================================
# FONCTION POUR RAFRAICHIR LES DONNEES
# ============================================

def refresh_home(frame):
    """
    Rafraichit toutes les donnees affichees.

    Args:
        frame: Le frame contenant les references aux variables et au data_manager
    """
    data_manager = frame.data_manager

    # Nombre d'activites
    activites = data_manager.get_activites()
    frame.stats_vars["activities"].set(str(len(activites)))

    # Budget restant
    budget = data_manager.get_budget()
    budget_prevu = budget.get('budget_prevu', 0)
    total_depenses = data_manager.get_total_depenses()
    reste = budget_prevu - total_depenses
    frame.stats_vars["budget"].set(format_currency(reste))

    # Nombre de participants
    participants = data_manager.get_participants()
    frame.stats_vars["participants"].set(str(len(participants)))

    # Informations du voyage
    voyage_info = data_manager.get_voyage_info()
    frame.info_destination.set(voyage_info.get('destination', 'Amsterdam'))

    date_depart = format_date(voyage_info.get('date_depart', '2025-09-15'))
    date_retour = format_date(voyage_info.get('date_retour', '2025-09-20'))
    frame.info_dates.set(f"{date_depart} - {date_retour}")

    # Progression checklist
    checked, total, percentage = data_manager.get_checklist_progress()
    frame.info_checklist.set(f"{percentage}% ({checked}/{total})")


# ============================================
# FONCTION PRINCIPALE DE CREATION DU FRAME
# ============================================

def HomeFrame(parent, data_manager):
    """
    Cree et retourne le frame d'accueil.

    Ce frame utilise le gestionnaire PLACE pour positionner
    les widgets de maniere absolue.

    Args:
        parent: Le widget parent (Notebook)
        data_manager: Reference au gestionnaire de donnees

    Returns:
        Le frame configure avec tous ses widgets
    """
    # Creer le frame principal
    frame = ttk.Frame(parent)

    # Stocker la reference au data_manager
    frame.data_manager = data_manager

    # Variable pour le compte a rebours
    countdown_var = tk.StringVar(value="Calcul...")
    frame.countdown_job = None

    # ============================================
    # CANVAS DE FOND (pour le design)
    # ============================================

    canvas = tk.Canvas(
        frame,
        bg=COLORS["background"],
        highlightthickness=0
    )
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # Dessiner les decorations apres un delai
    frame.after(100, lambda: draw_decorations_delayed(frame, canvas))

    # ============================================
    # TITRE PRINCIPAL (utilise PLACE)
    # ============================================

    title_frame = tk.Frame(
        frame,
        bg=COLORS["primary"],
        padx=30,
        pady=20
    )
    # Positionne avec PLACE - centre en haut
    title_frame.place(relx=0.5, y=30, anchor="n")

    # Titre "Amsterdam"
    title_label = tk.Label(
        title_frame,
        text="AMSTERDAM",
        font=("Segoe UI", 36, "bold"),
        fg=COLORS["text_light"],
        bg=COLORS["primary"]
    )
    title_label.pack()

    # Sous-titre
    subtitle_label = tk.Label(
        title_frame,
        text="Voyage d'etude 2025",
        font=FONTS["subtitle"],
        fg=COLORS["text_light"],
        bg=COLORS["primary"]
    )
    subtitle_label.pack()

    # ============================================
    # COMPTE A REBOURS (utilise PLACE)
    # ============================================

    countdown_frame = tk.Frame(
        frame,
        bg="white",
        padx=20,
        pady=10,
        relief="solid",
        bd=1
    )
    # Positionne sous le titre, centre
    countdown_frame.place(relx=0.5, y=200, anchor="n")

    countdown_title = tk.Label(
        countdown_frame,
        text="Compte a rebours",
        font=FONTS["heading"],
        bg="white",
        fg=COLORS["text"]
    )
    countdown_title.pack()

    countdown_value = tk.Label(
        countdown_frame,
        textvariable=countdown_var,
        font=("Segoe UI", 25, "bold"),
        bg="white",
        fg=COLORS["primary"]
    )
    countdown_value.pack(pady=3)

    countdown_subtitle = tk.Label(
        countdown_frame,
        text="avant le depart !",
        font=FONTS["body"],
        bg="white",
        fg=COLORS["text"]
    )
    countdown_subtitle.pack()

    # ============================================
    # CARTES DE STATISTIQUES (utilise PLACE)
    # ============================================

    # Variables pour les stats
    activities_var = tk.StringVar(value="0")
    budget_var = tk.StringVar(value="0 EUR")
    participants_var = tk.StringVar(value="0")

    # Carte 1: Activites (positionnee a gauche)
    activities_card = create_stat_card(
        frame,
        icon="Activites",
        title="Activites",
        value_var=activities_var,
        subtitle="prevues"
    )
    activities_card.place(relx=0.3, y=350, anchor="n")

    # Carte 2: Budget (positionnee au centre)
    budget_card = create_stat_card(
        frame,
        icon="Budget",
        title="Budget",
        value_var=budget_var,
        subtitle="disponible"
    )
    budget_card.place(relx=0.5, y=350, anchor="n")

    # Carte 3: Participants (positionnee a droite)
    participants_card = create_stat_card(
        frame,
        icon="Participants",
        title="Participants",
        value_var=participants_var,
        subtitle="inscrits"
    )
    participants_card.place(relx=0.7, y=350, anchor="n")

    # Stocker les variables dans le frame
    frame.stats_vars = {
        "activities": activities_var,
        "budget": budget_var,
        "participants": participants_var
    }

    # ============================================
    # INFORMATIONS DU VOYAGE (utilise PLACE)
    # ============================================

    info_frame = tk.Frame(
        frame,
        bg="white",
        padx=30,
        pady=20,
        relief="solid",
        bd=1
    )
    info_frame.place(relx=0.5, y=550, anchor="n")

    # Titre de la section
    info_title = tk.Label(
        info_frame,
        text="Informations du voyage",
        font=FONTS["heading"],
        bg="white",
        fg=COLORS["text"]
    )
    info_title.pack(pady=(0, 10))

    # Container pour les infos
    info_container = tk.Frame(info_frame, bg="white")
    info_container.pack()

    # Seconde box pour les informations
    info_container2 = tk.Frame(info_frame, bg="white")
    info_container2.pack(side="left", padx=5)

    # Troisieme box pour les informations
    info_container3 = tk.Frame(info_frame, bg="white")
    info_container3.pack(side="right", padx=5)

    # Variables pour les infos
    frame.info_destination = tk.StringVar(value="Amsterdam")
    frame.info_dates = tk.StringVar(value="15/09/2025 - 20/09/2025")
    frame.info_checklist = tk.StringVar(value="0%")

    # Destination
    tk.Label(
        info_container2,
        text="Destination:",
        font=FONTS["body_bold"],
        bg="white"
    ).grid(row=0, column=0, sticky="e", padx=5, pady=2)

    tk.Label(
        info_container2,
        textvariable=frame.info_destination,
        font=FONTS["body"],
        bg="white",
        fg=COLORS["primary"]
    ).grid(row=0, column=1, sticky="w", padx=5, pady=2)

    # Dates
    tk.Label(
        info_container3,
        text="Dates:",
        font=FONTS["body_bold"],
        bg="white"
    ).grid(row=1, column=0, sticky="e", padx=5, pady=2)

    tk.Label(
        info_container3,
        textvariable=frame.info_dates,
        font=FONTS["body"],
        bg="white"
    ).grid(row=1, column=1, sticky="w", padx=5, pady=2)

    # Checklist
    tk.Label(
        info_container2,
        text="Checklist:",
        font=FONTS["body_bold"],
        bg="white"
    ).grid(row=2, column=0, sticky="e", padx=5, pady=2)

    tk.Label(
        info_container2,
        textvariable=frame.info_checklist,
        font=FONTS["body"],
        bg="white",
        fg=COLORS["success"]
    ).grid(row=2, column=1, sticky="w", padx=5, pady=2)

    # ============================================
    # ATTACHER LA METHODE REFRESH AU FRAME
    # ============================================

    frame.refresh = lambda: refresh_home(frame)

    # Lancer le compte a rebours
    update_countdown(frame, countdown_var)

    # Charger les donnees initiales
    frame.refresh()

    return frame
