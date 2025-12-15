"""
budget_frame.py - Gestion du budget pour le voyage a Amsterdam.

Ce module permet de gerer les depenses du voyage:
- Definir le budget prevu
- Ajouter des depenses par categorie
- Visualiser le budget restant
- Voir la repartition par categorie

IMPORTANT: Ce frame utilise le gestionnaire de layout GRID
pour organiser les widgets en lignes et colonnes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, BUDGET_CATEGORIES, format_currency, format_date


class BudgetFrame(ttk.Frame):
    """
    Frame de gestion du budget du voyage.
    
    Ce frame utilise le gestionnaire GRID pour organiser
    le formulaire de depenses et l'affichage du budget.
    
    Attributes:
        data_manager: Reference au gestionnaire de donnees
        tree: Widget Treeview pour afficher les depenses
        selected_id: ID de la depense selectionnee
    """
    
    def __init__(self, parent: tk.Widget, data_manager: Any) -> None:
        """
        Initialise le frame du budget.
        
        Args:
            parent: Le widget parent (Notebook)
            data_manager: Reference au gestionnaire de donnees
        """
        super().__init__(parent)
        
        self.data_manager = data_manager
        self.selected_id: Optional[int] = None
        
        # Variables
        self._init_variables()
        
        # Creer l'interface
        self._create_widgets()
        
        # Charger les donnees
        self.refresh()
    
    def _init_variables(self) -> None:
        """
        Initialise les variables du formulaire.
        """
        # Variables du formulaire
        self.var_date = tk.StringVar()
        self.var_categorie = tk.StringVar()
        self.var_montant = tk.StringVar()
        self.var_description = tk.StringVar()
        self.var_participant = tk.StringVar()
        
        # Variables du budget
        self.var_budget_prevu = tk.StringVar()
        self.var_total_depenses = tk.StringVar(value="0,00 €")
        self.var_budget_restant = tk.StringVar(value="0,00 €")
    
    def _create_widgets(self) -> None:
        """
        Cree tous les widgets du frame.
        
        Utilise GRID pour organiser les elements.
        """
        # Configuration du grid principal
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        
        # ============================================
        # RESUME DU BUDGET (utilise GRID)
        # ============================================
        
        summary_frame = ttk.LabelFrame(self, text="💰 Résumé du budget", padding=15)
        summary_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Configuration du grid du resume
        summary_frame.columnconfigure(1, weight=1)
        summary_frame.columnconfigure(3, weight=1)
        summary_frame.columnconfigure(5, weight=1)
        
        # Budget prevu
        ttk.Label(
            summary_frame,
            text="Budget prévu:",
            font=FONTS["body_bold"]
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        budget_entry = ttk.Entry(
            summary_frame,
            textvariable=self.var_budget_prevu,
            width=15,
            font=FONTS["body"]
        )
        budget_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Button(
            summary_frame,
            text="💾",
            width=3,
            command=self._save_budget_prevu
        ).grid(row=0, column=2, padx=2)
        
        # Total depenses
        ttk.Label(
            summary_frame,
            text="Total dépensé:",
            font=FONTS["body_bold"]
        ).grid(row=0, column=3, sticky="e", padx=5, pady=5)
        
        ttk.Label(
            summary_frame,
            textvariable=self.var_total_depenses,
            font=("Segoe UI", 14, "bold"),
            foreground=COLORS["danger"]
        ).grid(row=0, column=4, sticky="w", padx=5, pady=5)
        
        # Budget restant
        ttk.Label(
            summary_frame,
            text="Reste:",
            font=FONTS["body_bold"]
        ).grid(row=0, column=5, sticky="e", padx=5, pady=5)
        
        self.label_restant = ttk.Label(
            summary_frame,
            textvariable=self.var_budget_restant,
            font=("Segoe UI", 14, "bold"),
            foreground=COLORS["success"]
        )
        self.label_restant.grid(row=0, column=6, sticky="w", padx=5, pady=5)
        
        # ============================================
        # FORMULAIRE D'AJOUT DE DEPENSE (utilise GRID)
        # ============================================
        
        form_frame = ttk.LabelFrame(self, text="➕ Ajouter une dépense", padding=15)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Configuration du grid du formulaire
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        form_frame.columnconfigure(5, weight=1)
        
        # Ligne 1: Date, Categorie
        ttk.Label(form_frame, text="Date:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_date, width=15).grid(
            row=0, column=1, sticky="w", padx=5, pady=5
        )
        
        ttk.Label(form_frame, text="Catégorie:").grid(
            row=0, column=2, sticky="e", padx=5, pady=5
        )
        categorie_combo = ttk.Combobox(
            form_frame,
            textvariable=self.var_categorie,
            values=BUDGET_CATEGORIES,
            state="readonly",
            width=15
        )
        categorie_combo.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        ttk.Label(form_frame, text="Montant (€):").grid(
            row=0, column=4, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_montant, width=12).grid(
            row=0, column=5, sticky="w", padx=5, pady=5
        )
        
        # Ligne 2: Description, Participant
        ttk.Label(form_frame, text="Description:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_description, width=40).grid(
            row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5
        )
        
        ttk.Label(form_frame, text="Payé par:").grid(
            row=1, column=4, sticky="e", padx=5, pady=5
        )
        self.participant_combo = ttk.Combobox(
            form_frame,
            textvariable=self.var_participant,
            values=["Groupe"],
            width=15
        )
        self.participant_combo.grid(row=1, column=5, sticky="w", padx=5, pady=5)
        
        # Ligne 3: Boutons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=10)
        
        ttk.Button(
            btn_frame,
            text="➕ Ajouter",
            command=self._add_expense
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Supprimer",
            command=self._delete_expense
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔄 Effacer",
            command=self._clear_form
        ).grid(row=0, column=2, padx=5)
        
        # ============================================
        # TABLEAU DES DEPENSES (utilise GRID)
        # ============================================
        
        table_frame = ttk.LabelFrame(self, text="📋 Liste des dépenses", padding=10)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Colonnes du Treeview
        columns = ("date", "categorie", "montant", "description", "participant")
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # En-tetes
        self.tree.heading("date", text="Date")
        self.tree.heading("categorie", text="Catégorie")
        self.tree.heading("montant", text="Montant")
        self.tree.heading("description", text="Description")
        self.tree.heading("participant", text="Payé par")
        
        # Largeurs
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("categorie", width=100)
        self.tree.column("montant", width=100, anchor="e")
        self.tree.column("description", width=200)
        self.tree.column("participant", width=100)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Selection
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        
        # ============================================
        # REPARTITION PAR CATEGORIE (utilise GRID)
        # ============================================
        
        cat_frame = ttk.LabelFrame(self, text="📊 Répartition par catégorie", padding=10)
        cat_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        
        cat_frame.columnconfigure(0, weight=1)
        cat_frame.rowconfigure(0, weight=1)
        
        # Frame pour les barres de progression
        self.categories_container = ttk.Frame(cat_frame)
        self.categories_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.categories_container.columnconfigure(1, weight=1)
    
    def _save_budget_prevu(self) -> None:
        """
        Sauvegarde le budget prevu.
        """
        try:
            montant = float(self.var_budget_prevu.get().replace(",", ".").replace(" ", "").replace("€", ""))
            self.data_manager.update_budget_prevu(montant)
            self.refresh()
            messagebox.showinfo("Succès", "Budget prévu mis à jour !")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")
    
    def _add_expense(self) -> None:
        """
        Ajoute une nouvelle depense.
        """
        # Validations
        if not self.var_categorie.get():
            messagebox.showwarning("Attention", "Veuillez sélectionner une catégorie.")
            return
        
        try:
            montant = float(self.var_montant.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre.")
            return
        
        if montant <= 0:
            messagebox.showwarning("Attention", "Le montant doit être positif.")
            return
        
        # Creer la depense
        depense = {
            "date": self.var_date.get() or "Non spécifié",
            "categorie": self.var_categorie.get(),
            "montant": montant,
            "description": self.var_description.get().strip(),
            "participant": self.var_participant.get() or "Groupe"
        }
        
        self.data_manager.add_depense(depense)
        self.refresh()
        self._clear_form()
        
        messagebox.showinfo("Succès", "Dépense ajoutée !")
    
    def _delete_expense(self) -> None:
        """
        Supprime la depense selectionnee.
        """
        if not self.selected_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner une dépense.")
            return
        
        confirm = messagebox.askyesno(
            "Confirmation",
            "Supprimer cette dépense ?"
        )
        
        if confirm:
            self.data_manager.delete_depense(self.selected_id)
            self.refresh()
            self._clear_form()
    
    def _clear_form(self) -> None:
        """
        Efface le formulaire.
        """
        self.var_date.set("")
        self.var_categorie.set("")
        self.var_montant.set("")
        self.var_description.set("")
        self.var_participant.set("")
        self.selected_id = None
    
    def _on_select(self, event: tk.Event) -> None:
        """
        Callback de selection.
        """
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            tags = self.tree.item(item)["tags"]
            self.selected_id = int(tags[0]) if tags else None
    
    def _update_categories_display(self) -> None:
        """
        Met a jour l'affichage des categories.
        """
        # Nettoyer
        for widget in self.categories_container.winfo_children():
            widget.destroy()
        
        # Obtenir les totaux par categorie
        totaux = self.data_manager.get_depenses_by_category()
        total = sum(totaux.values())
        
        if total == 0:
            ttk.Label(
                self.categories_container,
                text="Aucune dépense enregistrée",
                font=FONTS["body"]
            ).grid(row=0, column=0, pady=20)
            return
        
        # Creer une barre pour chaque categorie
        row = 0
        colors = ["#FF6B35", "#1E3A5F", "#F7C948", "#28A745", "#DC3545", "#6C757D"]
        
        for i, cat in enumerate(BUDGET_CATEGORIES):
            montant = totaux.get(cat, 0)
            if montant > 0:
                pourcentage = (montant / total) * 100
                
                # Label categorie
                ttk.Label(
                    self.categories_container,
                    text=f"{cat}:",
                    font=FONTS["body"]
                ).grid(row=row, column=0, sticky="w", padx=5, pady=2)
                
                # Barre de progression
                progress = ttk.Progressbar(
                    self.categories_container,
                    length=150,
                    maximum=100,
                    value=pourcentage
                )
                progress.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                
                # Montant et pourcentage
                ttk.Label(
                    self.categories_container,
                    text=f"{format_currency(montant)} ({pourcentage:.1f}%)",
                    font=FONTS["small"]
                ).grid(row=row, column=2, sticky="w", padx=5, pady=2)
                
                row += 1
    
    def _update_participants_list(self) -> None:
        """
        Met a jour la liste des participants dans le combobox.
        """
        participants = self.data_manager.get_participants()
        noms = ["Groupe"] + [f"{p.get('prenom', '')} {p.get('nom', '')}" for p in participants]
        self.participant_combo["values"] = noms
    
    def refresh(self) -> None:
        """
        Rafraichit toutes les donnees.
        """
        # Budget
        budget = self.data_manager.get_budget()
        budget_prevu = budget.get('budget_prevu', 0)
        self.var_budget_prevu.set(str(budget_prevu))
        
        # Total depenses
        total = self.data_manager.get_total_depenses()
        self.var_total_depenses.set(format_currency(total))
        
        # Restant
        restant = budget_prevu - total
        self.var_budget_restant.set(format_currency(restant))
        
        # Couleur selon le restant
        if restant < 0:
            self.label_restant.configure(foreground=COLORS["danger"])
        elif restant < budget_prevu * 0.2:
            self.label_restant.configure(foreground=COLORS["warning"])
        else:
            self.label_restant.configure(foreground=COLORS["success"])
        
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Remplir le tableau
        depenses = self.data_manager.get_depenses()
        for dep in sorted(depenses, key=lambda x: x.get('date', ''), reverse=True):
            self.tree.insert(
                "",
                "end",
                values=(
                    dep.get('date', ''),
                    dep.get('categorie', ''),
                    format_currency(dep.get('montant', 0)),
                    dep.get('description', ''),
                    dep.get('participant', '')
                ),
                tags=(dep.get('id'),)
            )
        
        # Mettre a jour les categories
        self._update_categories_display()
        
        # Mettre a jour les participants
        self._update_participants_list()

