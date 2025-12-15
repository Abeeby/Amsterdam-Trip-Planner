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
from datetime import datetime
from typing import Any, Dict

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, get_days_until_departure, format_date, format_currency


class HomeFrame(ttk.Frame):
    """
    Frame d'accueil affichant un resume du voyage.
    
    Ce frame utilise le gestionnaire PLACE pour positionner
    les widgets de maniere absolue, permettant un design
    plus creatif et visuellement attrayant.
    
    Attributes:
        data_manager: Reference au gestionnaire de donnees
        canvas: Canvas pour le fond et les elements graphiques
    """
    
    def __init__(self, parent: tk.Widget, data_manager: Any) -> None:
        """
        Initialise le frame d'accueil.
        
        Args:
            parent: Le widget parent (Notebook)
            data_manager: Reference au gestionnaire de donnees
        """
        super().__init__(parent)
        
        self.data_manager = data_manager
        
        # Variables pour le compte a rebours
        self.countdown_var = tk.StringVar(value="Calcul...")
        self.countdown_job = None
        
        # Creer l'interface
        self._create_widgets()
        
        # Lancer le compte a rebours
        self._update_countdown()
    
    def _create_widgets(self) -> None:
        """
        Cree tous les widgets de la page d'accueil.
        
        Utilise le gestionnaire PLACE pour positionner les elements.
        """
        # ============================================
        # CANVAS DE FOND (pour le design)
        # ============================================
        
        # Canvas qui occupe tout l'espace
        self.canvas = tk.Canvas(
            self,
            bg=COLORS["background"],
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Dessiner des elements decoratifs
        self._draw_decorations()
        
        # ============================================
        # TITRE PRINCIPAL (utilise PLACE)
        # ============================================
        
        # Frame pour le titre avec fond colore
        title_frame = tk.Frame(
            self,
            bg=COLORS["primary"],
            padx=30,
            pady=20
        )
        # Positionne avec PLACE - centre en haut
        title_frame.place(relx=0.5, y=30, anchor="n")
        
        # Emoji drapeau neerlandais
        flag_label = tk.Label(
            title_frame,
            text="🇳🇱",
            font=("Segoe UI Emoji", 48),
            bg=COLORS["primary"]
        )
        flag_label.pack()
        
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
            text="Voyage d'étude 2025",
            font=FONTS["subtitle"],
            fg=COLORS["text_light"],
            bg=COLORS["primary"]
        )
        subtitle_label.pack()
        
        # ============================================
        # COMPTE A REBOURS (utilise PLACE)
        # ============================================
        
        countdown_frame = tk.Frame(
            self,
            bg="white",
            padx=25,
            pady=15,
            relief="solid",
            bd=1
        )
        # Positionne sous le titre, centre
        countdown_frame.place(relx=0.5, y=220, anchor="n")
        
        countdown_title = tk.Label(
            countdown_frame,
            text="⏰ Compte à rebours",
            font=FONTS["heading"],
            bg="white",
            fg=COLORS["text"]
        )
        countdown_title.pack()
        
        countdown_value = tk.Label(
            countdown_frame,
            textvariable=self.countdown_var,
            font=("Segoe UI", 28, "bold"),
            bg="white",
            fg=COLORS["primary"]
        )
        countdown_value.pack(pady=5)
        
        countdown_subtitle = tk.Label(
            countdown_frame,
            text="avant le départ !",
            font=FONTS["body"],
            bg="white",
            fg=COLORS["text"]
        )
        countdown_subtitle.pack()
        
        # ============================================
        # CARTES DE STATISTIQUES (utilise PLACE)
        # ============================================
        
        # Carte 1: Activites (positionnee a gauche)
        self.activities_card = self._create_stat_card(
            icon="📅",
            title="Activités",
            value_var=tk.StringVar(value="0"),
            subtitle="prévues"
        )
        self.activities_card.place(relx=0.2, y=350, anchor="n")
        
        # Carte 2: Budget (positionnee au centre)
        self.budget_card = self._create_stat_card(
            icon="💰",
            title="Budget",
            value_var=tk.StringVar(value="0 €"),
            subtitle="disponible"
        )
        self.budget_card.place(relx=0.5, y=350, anchor="n")
        
        # Carte 3: Participants (positionnee a droite)
        self.participants_card = self._create_stat_card(
            icon="👥",
            title="Participants",
            value_var=tk.StringVar(value="0"),
            subtitle="inscrits"
        )
        self.participants_card.place(relx=0.8, y=350, anchor="n")
        
        # ============================================
        # INFORMATIONS DU VOYAGE (utilise PLACE)
        # ============================================
        
        info_frame = tk.Frame(
            self,
            bg="white",
            padx=30,
            pady=20,
            relief="solid",
            bd=1
        )
        info_frame.place(relx=0.5, y=480, anchor="n")
        
        # Titre de la section
        info_title = tk.Label(
            info_frame,
            text="📍 Informations du voyage",
            font=FONTS["heading"],
            bg="white",
            fg=COLORS["text"]
        )
        info_title.pack(pady=(0, 10))
        
        # Container pour les infos (utilise grid a l'interieur)
        info_container = tk.Frame(info_frame, bg="white")
        info_container.pack()
        
        # Variables pour les infos
        self.info_destination = tk.StringVar(value="Amsterdam")
        self.info_dates = tk.StringVar(value="15/09/2025 - 20/09/2025")
        self.info_checklist = tk.StringVar(value="0%")
        
        # Destination
        tk.Label(
            info_container,
            text="Destination:",
            font=FONTS["body_bold"],
            bg="white"
        ).grid(row=0, column=0, sticky="e", padx=5, pady=2)
        
        tk.Label(
            info_container,
            textvariable=self.info_destination,
            font=FONTS["body"],
            bg="white",
            fg=COLORS["primary"]
        ).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        # Dates
        tk.Label(
            info_container,
            text="Dates:",
            font=FONTS["body_bold"],
            bg="white"
        ).grid(row=1, column=0, sticky="e", padx=5, pady=2)
        
        tk.Label(
            info_container,
            textvariable=self.info_dates,
            font=FONTS["body"],
            bg="white"
        ).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Checklist
        tk.Label(
            info_container,
            text="Checklist:",
            font=FONTS["body_bold"],
            bg="white"
        ).grid(row=2, column=0, sticky="e", padx=5, pady=2)
        
        tk.Label(
            info_container,
            textvariable=self.info_checklist,
            font=FONTS["body"],
            bg="white",
            fg=COLORS["success"]
        ).grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        # Stocker les references des variables
        self.stats_vars = {
            "activities": self.activities_card.value_var,
            "budget": self.budget_card.value_var,
            "participants": self.participants_card.value_var
        }
        
        # Charger les donnees
        self.refresh()
    
    def _create_stat_card(self, icon: str, title: str, 
                          value_var: tk.StringVar, subtitle: str) -> tk.Frame:
        """
        Cree une carte de statistique.
        
        Args:
            icon: L'emoji a afficher
            title: Le titre de la carte
            value_var: Variable pour la valeur
            subtitle: Le sous-titre
            
        Returns:
            tk.Frame: La carte creee
        """
        card = tk.Frame(
            self,
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
    
    def _draw_decorations(self) -> None:
        """
        Dessine des elements decoratifs sur le canvas.
        """
        # Cette methode sera appelee apres que le canvas ait ses dimensions
        self.after(100, self._draw_decorations_delayed)
    
    def _draw_decorations_delayed(self) -> None:
        """
        Dessine les decorations apres que le canvas soit dimensionne.
        """
        # Obtenir les dimensions
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            # Le widget n'est pas encore affiche, reessayer
            self.after(100, self._draw_decorations_delayed)
            return
        
        # Dessiner des cercles decoratifs
        # Cercle orange en haut a gauche
        self.canvas.create_oval(
            -50, -50, 100, 100,
            fill=COLORS["primary"],
            outline=""
        )
        
        # Cercle bleu en bas a droite
        self.canvas.create_oval(
            width - 100, height - 100,
            width + 50, height + 50,
            fill=COLORS["secondary"],
            outline=""
        )
    
    def _update_countdown(self) -> None:
        """
        Met a jour le compte a rebours.
        
        Cette methode est appelee toutes les secondes pour
        mettre a jour l'affichage du temps restant.
        """
        days = get_days_until_departure()
        
        if days > 0:
            self.countdown_var.set(f"{days} jours")
        elif days == 0:
            self.countdown_var.set("C'est aujourd'hui !")
        else:
            self.countdown_var.set(f"Passé ({-days} jours)")
        
        # Planifier la prochaine mise a jour (toutes les heures)
        self.countdown_job = self.after(3600000, self._update_countdown)
    
    def refresh(self) -> None:
        """
        Rafraichit toutes les donnees affichees.
        
        Cette methode est appelee lors du changement d'onglet
        pour s'assurer que les donnees sont a jour.
        """
        # Actualiser les statistiques
        
        # Nombre d'activites
        activites = self.data_manager.get_activites()
        self.stats_vars["activities"].set(str(len(activites)))
        
        # Budget restant
        budget = self.data_manager.get_budget()
        budget_prevu = budget.get('budget_prevu', 0)
        total_depenses = self.data_manager.get_total_depenses()
        reste = budget_prevu - total_depenses
        self.stats_vars["budget"].set(format_currency(reste))
        
        # Nombre de participants
        participants = self.data_manager.get_participants()
        self.stats_vars["participants"].set(str(len(participants)))
        
        # Informations du voyage
        voyage_info = self.data_manager.get_voyage_info()
        self.info_destination.set(voyage_info.get('destination', 'Amsterdam'))
        
        date_depart = format_date(voyage_info.get('date_depart', '2025-09-15'))
        date_retour = format_date(voyage_info.get('date_retour', '2025-09-20'))
        self.info_dates.set(f"{date_depart} - {date_retour}")
        
        # Progression checklist
        checked, total, percentage = self.data_manager.get_checklist_progress()
        self.info_checklist.set(f"{percentage}% ({checked}/{total})")
    
    def destroy(self) -> None:
        """
        Nettoie les ressources avant la destruction du widget.
        """
        # Annuler le job du compte a rebours
        if self.countdown_job:
            self.after_cancel(self.countdown_job)
        
        super().destroy()

