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

# Import du gestionnaire de donnees
from data_manager import data_manager

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


class AmsterdamTripPlanner(tk.Tk):
    """
    Classe principale de l'application Amsterdam Trip Planner.
    
    Cette classe herite de tk.Tk et represente la fenetre principale
    de l'application. Elle gere la navigation entre les differents
    onglets via un systeme de Notebook (onglets).
    
    Attributes:
        data_manager: Instance du gestionnaire de donnees
        notebook: Widget Notebook pour la navigation par onglets
        frames: Dictionnaire des frames (onglets) de l'application
    """
    
    def __init__(self) -> None:
        """
        Initialise la fenetre principale et tous ses composants.
        """
        super().__init__()
        
        # Configuration de la fenetre principale
        self._configure_window()
        
        # Configuration du style ttk
        self._configure_styles()
        
        # Reference au gestionnaire de donnees
        self.data_manager = data_manager
        
        # Creation de l'interface
        self._create_widgets()
        
        # Centrer la fenetre sur l'ecran
        self._center_window()
        
        # Gestion de la fermeture
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _configure_window(self) -> None:
        """
        Configure les proprietes de la fenetre principale.
        """
        # Titre de la fenetre
        self.title(APP_TITLE)
        
        # Dimensions de la fenetre
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Dimensions minimales
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        
        # Couleur de fond
        self.configure(bg=COLORS["background"])
        
        # Permettre le redimensionnement
        self.resizable(True, True)
    
    def _configure_styles(self) -> None:
        """
        Configure les styles ttk pour une apparence moderne.
        """
        self.style = ttk.Style()
        
        # Utiliser le theme par defaut du systeme
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        
        # Style pour le Notebook (onglets)
        self.style.configure(
            "TNotebook",
            background=COLORS["background"],
            borderwidth=0
        )
        
        self.style.configure(
            "TNotebook.Tab",
            font=FONTS["button"],
            padding=[15, 8],
            background=COLORS["background"]
        )
        
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", COLORS["primary"])],
            foreground=[("selected", COLORS["text_light"])]
        )
        
        # Style pour les boutons
        self.style.configure(
            "TButton",
            font=FONTS["button"],
            padding=[10, 5]
        )
        
        self.style.configure(
            "Primary.TButton",
            font=FONTS["button"],
            background=COLORS["primary"]
        )
        
        # Style pour les labels
        self.style.configure(
            "TLabel",
            font=FONTS["body"],
            background=COLORS["background"]
        )
        
        self.style.configure(
            "Title.TLabel",
            font=FONTS["title"],
            background=COLORS["background"]
        )
        
        self.style.configure(
            "Subtitle.TLabel",
            font=FONTS["subtitle"],
            background=COLORS["background"]
        )
        
        # Style pour les frames
        self.style.configure(
            "TFrame",
            background=COLORS["background"]
        )
        
        self.style.configure(
            "Card.TFrame",
            background="white",
            relief="solid",
            borderwidth=1
        )
        
        # Style pour les entrees
        self.style.configure(
            "TEntry",
            font=FONTS["body"],
            padding=[5, 5]
        )
        
        # Style pour le Treeview
        self.style.configure(
            "Treeview",
            font=FONTS["body"],
            rowheight=30
        )
        
        self.style.configure(
            "Treeview.Heading",
            font=FONTS["body_bold"]
        )
    
    def _create_widgets(self) -> None:
        """
        Cree tous les widgets de l'interface principale.
        """
        # Container principal
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # En-tete avec le titre
        self._create_header()
        
        # Notebook (systeme d'onglets)
        self._create_notebook()
    
    def _create_header(self) -> None:
        """
        Cree l'en-tete de l'application avec le titre.
        """
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Titre principal
        title_label = ttk.Label(
            header_frame,
            text="🇳🇱 Amsterdam Trip Planner 2025",
            style="Title.TLabel"
        )
        title_label.pack(side=tk.LEFT)
        
        # Bouton de sauvegarde manuelle
        save_btn = ttk.Button(
            header_frame,
            text="💾 Sauvegarder",
            command=self._save_all_data
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        # Bouton de reinitialisation
        reset_btn = ttk.Button(
            header_frame,
            text="🔄 Réinitialiser",
            command=self._reset_data
        )
        reset_btn.pack(side=tk.RIGHT, padx=5)
    
    def _create_notebook(self) -> None:
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
        """
        # Creation du Notebook
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dictionnaire pour stocker les references aux frames
        self.frames = {}
        
        # Liste des onglets avec leurs icones et classes
        tabs_config = [
            ("🏠 Accueil", HomeFrame, "home"),
            ("📅 Activités", ActivitiesFrame, "activities"),
            ("💰 Budget", BudgetFrame, "budget"),
            ("🏨 Hôtel", HotelFrame, "hotel"),
            ("🚂 Transport", TransportFrame, "transport"),
            ("👥 Participants", ParticipantsFrame, "participants"),
            ("✅ Checklist", ChecklistFrame, "checklist")
        ]
        
        # Creation de chaque onglet
        for tab_name, frame_class, frame_key in tabs_config:
            # Creer le frame
            frame = frame_class(self.notebook, self.data_manager)
            
            # Ajouter au notebook
            self.notebook.add(frame, text=tab_name)
            
            # Stocker la reference
            self.frames[frame_key] = frame
        
        # Evenement lors du changement d'onglet
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
    
    def _on_tab_changed(self, event: tk.Event) -> None:
        """
        Callback appele lors du changement d'onglet.
        
        Permet de rafraichir les donnees de l'onglet actif.
        
        Args:
            event: L'evenement Tkinter
        """
        # Obtenir l'index de l'onglet actif
        selected_index = self.notebook.index(self.notebook.select())
        
        # Liste des cles dans l'ordre
        frame_keys = ["home", "activities", "budget", "hotel", 
                      "transport", "participants", "checklist"]
        
        # Rafraichir le frame actif s'il a une methode refresh
        if selected_index < len(frame_keys):
            frame_key = frame_keys[selected_index]
            frame = self.frames.get(frame_key)
            
            if frame and hasattr(frame, 'refresh'):
                frame.refresh()
    
    def _center_window(self) -> None:
        """
        Centre la fenetre sur l'ecran.
        """
        # Mettre a jour la fenetre pour obtenir ses dimensions reelles
        self.update_idletasks()
        
        # Obtenir les dimensions de l'ecran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculer la position
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        
        # Appliquer la position
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    
    def _save_all_data(self) -> None:
        """
        Sauvegarde manuelle de toutes les donnees.
        """
        if self.data_manager.save_data():
            messagebox.showinfo(
                "Sauvegarde",
                "Les données ont été sauvegardées avec succès !"
            )
        else:
            messagebox.showerror(
                "Erreur",
                "Une erreur est survenue lors de la sauvegarde."
            )
    
    def _reset_data(self) -> None:
        """
        Reinitialise toutes les donnees aux valeurs par defaut.
        """
        confirm = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir réinitialiser toutes les données ?\n\n"
            "Cette action est irréversible !"
        )
        
        if confirm:
            self.data_manager.reset_to_defaults()
            
            # Rafraichir tous les frames
            for frame in self.frames.values():
                if hasattr(frame, 'refresh'):
                    frame.refresh()
            
            messagebox.showinfo(
                "Réinitialisation",
                "Les données ont été réinitialisées avec succès !"
            )
    
    def _on_closing(self) -> None:
        """
        Callback appele lors de la fermeture de l'application.
        
        Sauvegarde automatiquement les donnees avant de quitter.
        """
        # Sauvegarder automatiquement
        self.data_manager.save_data()
        
        # Fermer l'application
        self.destroy()


def main() -> None:
    """
    Point d'entree principal de l'application.
    
    Cree et lance l'application Amsterdam Trip Planner.
    """
    print("=" * 50)
    print("🇳🇱 Amsterdam Trip Planner 2025")
    print("=" * 50)
    print("Démarrage de l'application...")
    
    try:
        # Creer l'application
        app = AmsterdamTripPlanner()
        
        print("Application prête !")
        print("=" * 50)
        
        # Lancer la boucle principale
        app.mainloop()
        
    except Exception as e:
        print(f"Erreur fatale: {e}")
        messagebox.showerror(
            "Erreur",
            f"Une erreur fatale est survenue:\n{e}"
        )
        sys.exit(1)
    
    print("Application fermée.")


if __name__ == "__main__":
    main()

