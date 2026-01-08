#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py - Point d'entree de l'application Amsterdam Trip Planner.

Ce module cree la fenetre principale de l'application et gere
la navigation entre les differents onglets (frames).

Usage:
    python main.py

Auteur: Voyage Amsterdam 2025
Date: Decembre 2024
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Import des configurations
from config import (
    APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    MIN_WIDTH, MIN_HEIGHT, COLORS, FONTS
)

# Import du gestionnaire de donnees (module avec fonctions)
import data_manager

# Import des frames (onglets)
from frames import (
    HomeFrame,
    ActivitiesFrame,
    BudgetFrame,
    HotelFrame,
    TransportFrame,
    ParticipantsFrame,
    ChecklistFrame
)

# ============================================
# VARIABLES GLOBALES
# ============================================

# Fenetre principale
root = None

# Notebook (onglets)
notebook = None

# Dictionnaire des frames
frames = {}


# ============================================
# FONCTIONS DE CONFIGURATION
# ============================================

def configure_window():
    """
    Configure les proprietes de la fenetre principale.
    """
    global root

    # Titre de la fenetre
    root.title(APP_TITLE)

    # Dimensions de la fenetre
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # Dimensions minimales
    root.minsize(MIN_WIDTH, MIN_HEIGHT)

    # Couleur de fond
    root.configure(bg=COLORS["background"])

    # Permettre le redimensionnement
    root.resizable(False, False)


def configure_styles():
    """
    Configure les styles ttk pour une apparence moderne.
    """
    style = ttk.Style()

    # Utiliser le theme par defaut du systeme
    available_themes = style.theme_names()
    if 'clam' in available_themes:
        style.theme_use('clam')

    # Style pour le Notebook (onglets)
    style.configure(
        "TNotebook",
        background=COLORS["background"],
        borderwidth=0
    )

    style.configure(
        "TNotebook.Tab",
        font=FONTS["button"],
        padding=[15, 8],
        background=COLORS["background"]
    )

    style.map(
        "TNotebook.Tab",
        background=[("selected", COLORS["primary"])],
        foreground=[("selected", COLORS["text_light"])]
    )

    # Style pour les boutons
    style.configure(
        "TButton",
        font=FONTS["button"],
        padding=[10, 5]
    )

    style.configure(
        "Primary.TButton",
        font=FONTS["button"],
        background=COLORS["primary"]
    )

    # Style pour les labels
    style.configure(
        "TLabel",
        font=FONTS["body"],
        background=COLORS["background"]
    )

    style.configure(
        "Title.TLabel",
        font=FONTS["title"],
        background=COLORS["background"]
    )

    style.configure(
        "Subtitle.TLabel",
        font=FONTS["subtitle"],
        background=COLORS["background"]
    )

    # Style pour les frames
    style.configure(
        "TFrame",
        background=COLORS["background"]
    )

    style.configure(
        "Card.TFrame",
        background="white",
        relief="solid",
        borderwidth=1
    )

    # Style pour les entrees
    style.configure(
        "TEntry",
        font=FONTS["body"],
        padding=[5, 5]
    )

    # Style pour le Treeview
    style.configure(
        "Treeview",
        font=FONTS["body"],
        rowheight=30
    )

    style.configure(
        "Treeview.Heading",
        font=FONTS["body_bold"]
    )


def center_window():
    """
    Centre la fenetre sur l'ecran.
    """
    global root

    # Mettre a jour la fenetre pour obtenir ses dimensions reelles
    root.update_idletasks()

    # Obtenir les dimensions de l'ecran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculer la position
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2

    # Appliquer la position
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


# ============================================
# FONCTIONS DE CREATION DE L'INTERFACE
# ============================================

def create_header(parent):
    """
    Cree l'en-tete de l'application avec le titre.

    Args:
        parent: Le widget parent
    """
    header_frame = ttk.Frame(parent)
    header_frame.pack(fill=tk.X, pady=(0, 10))

    # Titre principal
    title_label = ttk.Label(
        header_frame,
        text="Amsterdam Trip Planner 2025",
        style="Title.TLabel"
    )
    title_label.pack(side=tk.LEFT)

    # Bouton de sauvegarde manuelle
    save_btn = ttk.Button(
        header_frame,
        text="Sauvegarder",
        command=save_all_data
    )
    save_btn.pack(side=tk.RIGHT, padx=5)

    # Bouton de reinitialisation
    reset_btn = ttk.Button(
        header_frame,
        text="Reinitialiser",
        command=reset_data
    )
    reset_btn.pack(side=tk.RIGHT, padx=5)


def create_notebook(parent):
    """
    Cree le Notebook avec tous les onglets de l'application.

    Chaque onglet correspond a une fonctionnalite:
    - Accueil: Vue d'ensemble du voyage
    - Activites: Planification des activites
    - Budget: Gestion des finances
    - Hotel: Informations d'hebergement
    - Transport: Planning des transports
    - Participants: Liste des voyageurs
    - Checklist: Liste des affaires a emporter

    Args:
        parent: Le widget parent
    """
    global notebook, frames

    # Creation du Notebook
    notebook = ttk.Notebook(parent)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Liste des onglets avec leurs icones et classes
    tabs_config = [
        ("Accueil", HomeFrame, "home"),
        ("Activites", ActivitiesFrame, "activities"),
        ("Budget", BudgetFrame, "budget"),
        ("Hotel", HotelFrame, "hotel"),
        ("Transport", TransportFrame, "transport"),
        ("Participants", ParticipantsFrame, "participants"),
        ("Checklist", ChecklistFrame, "checklist")
    ]

    # Creation de chaque onglet
    for tab_name, frame_class, frame_key in tabs_config:
        # Creer le frame (passer le module data_manager comme gestionnaire)
        frame = frame_class(notebook, data_manager)

        # Ajouter au notebook
        notebook.add(frame, text=tab_name)

        # Stocker la reference
        frames[frame_key] = frame

    # Evenement lors du changement d'onglet
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)


def create_widgets():
    """
    Cree tous les widgets de l'interface principale.
    """
    global root

    # Container principal
    main_container = ttk.Frame(root)
    main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # En-tete avec le titre
    create_header(main_container)

    # Notebook (systeme d'onglets)
    create_notebook(main_container)


# ============================================
# CALLBACKS ET GESTIONNAIRES D'EVENEMENTS
# ============================================

def on_tab_changed(event):
    """
    Callback appele lors du changement d'onglet.

    Permet de rafraichir les donnees de l'onglet actif.

    Args:
        event: L'evenement Tkinter
    """
    global notebook, frames

    # Obtenir l'index de l'onglet actif
    selected_index = notebook.index(notebook.select())

    # Liste des cles dans l'ordre
    frame_keys = ["home", "activities", "budget", "hotel",
                  "transport", "participants", "checklist"]

    # Rafraichir le frame actif s'il a une methode refresh
    if selected_index < len(frame_keys):
        frame_key = frame_keys[selected_index]
        frame = frames.get(frame_key)

        if frame and hasattr(frame, 'refresh'):
            frame.refresh()


def save_all_data():
    """
    Sauvegarde manuelle de toutes les donnees.
    """
    if data_manager.save_data():
        messagebox.showinfo(
            "Sauvegarde",
            "Les donnees ont ete sauvegardees avec succes !"
        )
    else:
        messagebox.showerror(
            "Erreur",
            "Une erreur est survenue lors de la sauvegarde."
        )


def reset_data():
    """
    Reinitialise toutes les donnees aux valeurs par defaut.
    """
    global frames

    confirm = messagebox.askyesno(
        "Confirmation",
        "Etes-vous sur de vouloir reinitialiser toutes les donnees ?\n\n"
        "Cette action est irreversible !"
    )

    if confirm:
        data_manager.reset_to_defaults()

        # Rafraichir tous les frames
        for frame in frames.values():
            if hasattr(frame, 'refresh'):
                frame.refresh()

        messagebox.showinfo(
            "Reinitialisation",
            "Les donnees ont ete reinitialisees avec succes !"
        )


def on_closing():
    """
    Callback appele lors de la fermeture de l'application.

    Sauvegarde automatiquement les donnees avant de quitter.
    """
    global root

    # Sauvegarder automatiquement
    data_manager.save_data()

    # Fermer l'application
    root.destroy()


# ============================================
# FONCTION PRINCIPALE
# ============================================

def main():
    """
    Point d'entree principal de l'application.

    Cree et lance l'application Amsterdam Trip Planner.
    """
    global root

    print("=" * 50)
    print("Amsterdam Trip Planner 2025")
    print("=" * 50)
    print("Demarrage de l'application...")

    try:
        # Creer la fenetre principale
        root = tk.Tk()

        # Configuration de la fenetre
        configure_window()

        # Configuration des styles
        configure_styles()

        # Creation de l'interface
        create_widgets()

        # Centrer la fenetre
        center_window()

        # Gestion de la fermeture
        root.protocol("WM_DELETE_WINDOW", on_closing)

        print("Application prete !")
        print("=" * 50)

        # Lancer la boucle principale
        root.mainloop()

    except Exception as e:
        print(f"Erreur fatale: {e}")
        messagebox.showerror(
            "Erreur",
            f"Une erreur fatale est survenue:\n{e}"
        )
        sys.exit(1)

    print("Application fermee.")


if __name__ == "__main__":
    main()
