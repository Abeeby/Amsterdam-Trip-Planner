"""
activities_frame.py - Planificateur d'activites pour le voyage a Amsterdam.

Ce module permet de gerer les activites prevues pendant le voyage:
- Ajouter, modifier, supprimer des activites
- Afficher la liste des activites dans un tableau
- Trier par date

IMPORTANT: Ce frame utilise le gestionnaire de layout GRID
pour organiser les widgets en lignes et colonnes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict, Optional
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, format_date, format_currency


class ActivitiesFrame(ttk.Frame):
    """
    Frame de gestion des activites du voyage.
    
    Ce frame utilise le gestionnaire GRID pour organiser
    le formulaire et le tableau des activites.
    
    Attributes:
        data_manager: Reference au gestionnaire de donnees
        tree: Widget Treeview pour afficher les activites
        selected_id: ID de l'activite selectionnee
    """
    
    def __init__(self, parent: tk.Widget, data_manager: Any) -> None:
        """
        Initialise le frame des activites.
        
        Args:
            parent: Le widget parent (Notebook)
            data_manager: Reference au gestionnaire de donnees
        """
        super().__init__(parent)
        
        self.data_manager = data_manager
        self.selected_id: Optional[int] = None
        
        # Variables pour le formulaire
        self._init_form_variables()
        
        # Creer l'interface
        self._create_widgets()
        
        # Charger les donnees
        self.refresh()
    
    def _init_form_variables(self) -> None:
        """
        Initialise les variables du formulaire.
        """
        self.var_date = tk.StringVar()
        self.var_nom = tk.StringVar()
        self.var_lieu = tk.StringVar()
        self.var_horaire = tk.StringVar()
        self.var_duree = tk.StringVar()
        self.var_prix = tk.StringVar()
        self.var_description = tk.StringVar()
    
    def _create_widgets(self) -> None:
        """
        Cree tous les widgets du frame.
        
        Utilise GRID pour organiser les elements.
        """
        # Configuration du grid principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # ============================================
        # FORMULAIRE D'AJOUT/MODIFICATION (utilise GRID)
        # ============================================
        
        form_frame = ttk.LabelFrame(self, text="📝 Nouvelle activité", padding=15)
        form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Configuration des colonnes du formulaire
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        form_frame.columnconfigure(5, weight=1)
        
        # Ligne 1: Date, Nom, Lieu
        ttk.Label(form_frame, text="Date:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_date, width=15).grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )
        ttk.Label(form_frame, text="(AAAA-MM-JJ)", font=FONTS["small"]).grid(
            row=0, column=2, sticky="w"
        )
        
        ttk.Label(form_frame, text="Nom:").grid(
            row=0, column=3, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_nom, width=30).grid(
            row=0, column=4, columnspan=2, sticky="ew", padx=5, pady=5
        )
        
        # Ligne 2: Lieu, Horaire, Duree
        ttk.Label(form_frame, text="Lieu:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_lieu, width=30).grid(
            row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5
        )
        
        ttk.Label(form_frame, text="Horaire:").grid(
            row=1, column=3, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_horaire, width=10).grid(
            row=1, column=4, sticky="w", padx=5, pady=5
        )
        
        ttk.Label(form_frame, text="Durée:").grid(
            row=1, column=5, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_duree, width=10).grid(
            row=1, column=6, sticky="w", padx=5, pady=5
        )
        
        # Ligne 3: Prix, Description
        ttk.Label(form_frame, text="Prix (€):").grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_prix, width=10).grid(
            row=2, column=1, sticky="w", padx=5, pady=5
        )
        
        ttk.Label(form_frame, text="Description:").grid(
            row=2, column=3, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_description, width=40).grid(
            row=2, column=4, columnspan=3, sticky="ew", padx=5, pady=5
        )
        
        # Ligne 4: Boutons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=7, pady=10)
        
        ttk.Button(
            btn_frame,
            text="➕ Ajouter",
            command=self._add_activity
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            btn_frame,
            text="✏️ Modifier",
            command=self._update_activity
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Supprimer",
            command=self._delete_activity
        ).grid(row=0, column=2, padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔄 Effacer",
            command=self._clear_form
        ).grid(row=0, column=3, padx=5)
        
        # ============================================
        # TABLEAU DES ACTIVITES (utilise GRID)
        # ============================================
        
        table_frame = ttk.LabelFrame(self, text="📅 Liste des activités", padding=10)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configuration du grid pour le tableau
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Colonnes du Treeview
        columns = ("date", "nom", "lieu", "horaire", "duree", "prix")
        
        # Creer le Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Configurer les en-tetes
        self.tree.heading("date", text="Date", command=lambda: self._sort_by("date"))
        self.tree.heading("nom", text="Activité")
        self.tree.heading("lieu", text="Lieu")
        self.tree.heading("horaire", text="Horaire")
        self.tree.heading("duree", text="Durée")
        self.tree.heading("prix", text="Prix")
        
        # Configurer les largeurs des colonnes
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("nom", width=200)
        self.tree.column("lieu", width=200)
        self.tree.column("horaire", width=80, anchor="center")
        self.tree.column("duree", width=80, anchor="center")
        self.tree.column("prix", width=80, anchor="e")
        
        # Placer avec GRID
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar verticale
        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        # Scrollbar horizontale
        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        # Evenement de selection
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)
        
        # ============================================
        # RESUME (utilise GRID)
        # ============================================
        
        summary_frame = ttk.Frame(self)
        summary_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        # Configuration du grid pour le resume
        summary_frame.columnconfigure(1, weight=1)
        
        self.var_total_activities = tk.StringVar(value="0")
        self.var_total_prix = tk.StringVar(value="0,00 €")
        
        ttk.Label(
            summary_frame,
            text="Total activités:",
            font=FONTS["body_bold"]
        ).grid(row=0, column=0, padx=5)
        
        ttk.Label(
            summary_frame,
            textvariable=self.var_total_activities,
            font=FONTS["body"]
        ).grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(
            summary_frame,
            text="Coût total:",
            font=FONTS["body_bold"]
        ).grid(row=0, column=2, padx=5)
        
        ttk.Label(
            summary_frame,
            textvariable=self.var_total_prix,
            font=FONTS["body"],
            foreground=COLORS["primary"]
        ).grid(row=0, column=3, sticky="w", padx=5)
    
    def _add_activity(self) -> None:
        """
        Ajoute une nouvelle activite.
        """
        # Valider les champs obligatoires
        if not self.var_nom.get().strip():
            messagebox.showwarning("Attention", "Le nom de l'activité est obligatoire.")
            return
        
        if not self.var_date.get().strip():
            messagebox.showwarning("Attention", "La date est obligatoire.")
            return
        
        # Valider le format de la date
        try:
            datetime.strptime(self.var_date.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez AAAA-MM-JJ")
            return
        
        # Valider le prix
        try:
            prix = float(self.var_prix.get() or 0)
        except ValueError:
            messagebox.showerror("Erreur", "Le prix doit être un nombre.")
            return
        
        # Creer l'activite
        activite = {
            "date": self.var_date.get(),
            "nom": self.var_nom.get().strip(),
            "lieu": self.var_lieu.get().strip(),
            "horaire": self.var_horaire.get().strip(),
            "duree": self.var_duree.get().strip(),
            "prix": prix,
            "description": self.var_description.get().strip()
        }
        
        # Ajouter via le data manager
        self.data_manager.add_activite(activite)
        
        # Rafraichir et vider le formulaire
        self.refresh()
        self._clear_form()
        
        messagebox.showinfo("Succès", "Activité ajoutée avec succès !")
    
    def _update_activity(self) -> None:
        """
        Met a jour l'activite selectionnee.
        """
        if not self.selected_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner une activité.")
            return
        
        # Valider les champs
        if not self.var_nom.get().strip():
            messagebox.showwarning("Attention", "Le nom de l'activité est obligatoire.")
            return
        
        try:
            prix = float(self.var_prix.get() or 0)
        except ValueError:
            messagebox.showerror("Erreur", "Le prix doit être un nombre.")
            return
        
        # Creer l'activite mise a jour
        activite = {
            "date": self.var_date.get(),
            "nom": self.var_nom.get().strip(),
            "lieu": self.var_lieu.get().strip(),
            "horaire": self.var_horaire.get().strip(),
            "duree": self.var_duree.get().strip(),
            "prix": prix,
            "description": self.var_description.get().strip()
        }
        
        # Mettre a jour via le data manager
        self.data_manager.update_activite(self.selected_id, activite)
        
        # Rafraichir et vider
        self.refresh()
        self._clear_form()
        
        messagebox.showinfo("Succès", "Activité modifiée avec succès !")
    
    def _delete_activity(self) -> None:
        """
        Supprime l'activite selectionnee.
        """
        if not self.selected_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner une activité.")
            return
        
        # Confirmation
        confirm = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir supprimer cette activité ?"
        )
        
        if confirm:
            self.data_manager.delete_activite(self.selected_id)
            self.refresh()
            self._clear_form()
            messagebox.showinfo("Succès", "Activité supprimée.")
    
    def _clear_form(self) -> None:
        """
        Efface tous les champs du formulaire.
        """
        self.var_date.set("")
        self.var_nom.set("")
        self.var_lieu.set("")
        self.var_horaire.set("")
        self.var_duree.set("")
        self.var_prix.set("")
        self.var_description.set("")
        self.selected_id = None
        
        # Deselectionner dans le treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def _on_select(self, event: tk.Event) -> None:
        """
        Callback lors de la selection d'une ligne.
        """
        selection = self.tree.selection()
        if not selection:
            return
        
        # Recuperer l'ID stocke dans le tag
        item = selection[0]
        self.selected_id = self.tree.item(item)["tags"][0] if self.tree.item(item)["tags"] else None
    
    def _on_double_click(self, event: tk.Event) -> None:
        """
        Callback lors du double-clic sur une ligne.
        
        Remplit le formulaire avec les donnees de l'activite.
        """
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        tags = self.tree.item(item)["tags"]
        
        if not tags:
            return
        
        self.selected_id = int(tags[0])
        
        # Trouver l'activite correspondante
        activites = self.data_manager.get_activites()
        for activite in activites:
            if activite.get('id') == self.selected_id:
                # Remplir le formulaire
                self.var_date.set(activite.get('date', ''))
                self.var_nom.set(activite.get('nom', ''))
                self.var_lieu.set(activite.get('lieu', ''))
                self.var_horaire.set(activite.get('horaire', ''))
                self.var_duree.set(activite.get('duree', ''))
                self.var_prix.set(str(activite.get('prix', '')))
                self.var_description.set(activite.get('description', ''))
                break
    
    def _sort_by(self, column: str) -> None:
        """
        Trie le tableau par la colonne specifiee.
        """
        # Pour l'instant, on rafraichit simplement
        # (le tri par date est fait dans refresh)
        self.refresh()
    
    def refresh(self) -> None:
        """
        Rafraichit le tableau des activites.
        """
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Recuperer les activites
        activites = self.data_manager.get_activites()
        
        # Trier par date
        activites_triees = sorted(
            activites,
            key=lambda x: x.get('date', '9999-12-31')
        )
        
        # Calculer les totaux
        total_prix = 0
        
        # Remplir le tableau
        for activite in activites_triees:
            prix = activite.get('prix', 0)
            total_prix += prix
            
            self.tree.insert(
                "",
                "end",
                values=(
                    format_date(activite.get('date', '')),
                    activite.get('nom', ''),
                    activite.get('lieu', ''),
                    activite.get('horaire', ''),
                    activite.get('duree', ''),
                    format_currency(prix)
                ),
                tags=(activite.get('id'),)
            )
        
        # Mettre a jour les totaux
        self.var_total_activities.set(str(len(activites)))
        self.var_total_prix.set(format_currency(total_prix))

