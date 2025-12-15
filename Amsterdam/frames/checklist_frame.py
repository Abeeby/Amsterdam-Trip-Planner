"""
checklist_frame.py - Checklist des affaires a emporter pour le voyage.

Ce module permet de gerer une liste d'affaires a emporter:
- Ajouter des items par categorie
- Cocher les items prepares
- Suivre la progression

IMPORTANT: Ce frame utilise les gestionnaires PACK et GRID combines
pour demontrer l'utilisation mixte des layouts.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, CHECKLIST_CATEGORIES


class ChecklistFrame(ttk.Frame):
    """
    Frame de gestion de la checklist du voyage.
    
    Ce frame utilise une combinaison de PACK et GRID:
    - PACK pour l'organisation generale verticale
    - GRID pour le formulaire et les boutons
    
    Attributes:
        data_manager: Reference au gestionnaire de donnees
        checkbuttons: Dictionnaire des checkbuttons par ID
    """
    
    def __init__(self, parent: tk.Widget, data_manager: Any) -> None:
        """
        Initialise le frame de la checklist.
        
        Args:
            parent: Le widget parent (Notebook)
            data_manager: Reference au gestionnaire de donnees
        """
        super().__init__(parent)
        
        self.data_manager = data_manager
        self.checkbuttons: Dict[int, tk.BooleanVar] = {}
        
        # Variables
        self.var_item = tk.StringVar()
        self.var_categorie = tk.StringVar()
        self.var_progress = tk.StringVar(value="0%")
        self.var_progress_text = tk.StringVar(value="0/0 items cochés")
        
        # Creer l'interface
        self._create_widgets()
        
        # Charger les donnees
        self.refresh()
    
    def _create_widgets(self) -> None:
        """
        Cree tous les widgets du frame.
        
        Utilise PACK pour la structure principale et GRID pour les details.
        """
        # ============================================
        # EN-TETE (utilise PACK)
        # ============================================
        
        header = tk.Frame(self, bg=COLORS["success"], pady=15)
        header.pack(fill="x", padx=10, pady=(10, 0))
        
        tk.Label(
            header,
            text="✅ Checklist - Affaires à emporter",
            font=FONTS["title"],
            fg=COLORS["text_light"],
            bg=COLORS["success"]
        ).pack()
        
        # ============================================
        # BARRE DE PROGRESSION (utilise PACK)
        # ============================================
        
        progress_frame = ttk.Frame(self)
        progress_frame.pack(fill="x", padx=20, pady=15)
        
        # Label de progression
        ttk.Label(
            progress_frame,
            textvariable=self.var_progress_text,
            font=FONTS["body_bold"]
        ).pack(side="left")
        
        # Pourcentage
        ttk.Label(
            progress_frame,
            textvariable=self.var_progress,
            font=("Segoe UI", 18, "bold"),
            foreground=COLORS["success"]
        ).pack(side="right")
        
        # Barre de progression
        self.progressbar = ttk.Progressbar(
            progress_frame,
            length=400,
            maximum=100,
            mode="determinate"
        )
        self.progressbar.pack(side="right", padx=20)
        
        # ============================================
        # FORMULAIRE D'AJOUT (utilise GRID dans un frame PACK)
        # ============================================
        
        form_frame = ttk.LabelFrame(self, text="➕ Ajouter un item", padding=15)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Utiliser GRID pour le formulaire
        form_frame.columnconfigure(1, weight=1)
        
        # Item
        ttk.Label(form_frame, text="Item:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Entry(form_frame, textvariable=self.var_item, width=50).grid(
            row=0, column=1, sticky="ew", padx=5, pady=5
        )
        
        # Categorie
        ttk.Label(form_frame, text="Catégorie:").grid(
            row=0, column=2, sticky="e", padx=5, pady=5
        )
        ttk.Combobox(
            form_frame,
            textvariable=self.var_categorie,
            values=CHECKLIST_CATEGORIES,
            width=15,
            state="readonly"
        ).grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Boutons (utilise GRID)
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        ttk.Button(
            btn_frame,
            text="➕ Ajouter",
            command=self._add_item
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            btn_frame,
            text="✅ Tout cocher",
            command=self._check_all
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            btn_frame,
            text="⬜ Tout décocher",
            command=self._uncheck_all
        ).grid(row=0, column=2, padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Supprimer cochés",
            command=self._delete_checked
        ).grid(row=0, column=3, padx=5)
        
        # ============================================
        # LISTE DES ITEMS (utilise PACK)
        # ============================================
        
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas pour le scroll
        canvas = tk.Canvas(list_frame, bg="white", highlightthickness=1, highlightbackground=COLORS["border"])
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        
        self.items_frame = ttk.Frame(canvas)
        
        # Configurer le scroll
        self.items_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.items_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # PACK les elements
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll avec la molette
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"
        ))
        
        # ============================================
        # LEGENDE DES CATEGORIES (utilise PACK + GRID)
        # ============================================
        
        legend_frame = ttk.LabelFrame(self, text="📁 Catégories", padding=10)
        legend_frame.pack(fill="x", padx=20, pady=10)
        
        # Utiliser GRID pour les categories
        for i, cat in enumerate(CHECKLIST_CATEGORIES):
            col = i % 3
            row = i // 3
            
            icon = self._get_category_icon(cat)
            ttk.Label(
                legend_frame,
                text=f"{icon} {cat}",
                font=FONTS["body"]
            ).grid(row=row, column=col, sticky="w", padx=15, pady=2)
    
    def _get_category_icon(self, category: str) -> str:
        """
        Retourne l'emoji correspondant a la categorie.
        """
        icons = {
            "Documents": "📄",
            "Vêtements": "👕",
            "Électronique": "📱",
            "Hygiène": "🧴",
            "Médicaments": "💊",
            "Autre": "📦"
        }
        return icons.get(category, "📦")
    
    def _add_item(self) -> None:
        """
        Ajoute un nouvel item a la checklist.
        """
        item_text = self.var_item.get().strip()
        categorie = self.var_categorie.get()
        
        if not item_text:
            messagebox.showwarning("Attention", "Veuillez entrer un item.")
            return
        
        if not categorie:
            messagebox.showwarning("Attention", "Veuillez sélectionner une catégorie.")
            return
        
        item = {
            "item": item_text,
            "categorie": categorie,
            "checked": False
        }
        
        self.data_manager.add_checklist_item(item)
        
        # Vider le champ
        self.var_item.set("")
        
        # Rafraichir
        self.refresh()
    
    def _toggle_item(self, item_id: int) -> None:
        """
        Inverse l'etat d'un item.
        """
        self.data_manager.toggle_checklist_item(item_id)
        self._update_progress()
    
    def _delete_item(self, item_id: int) -> None:
        """
        Supprime un item.
        """
        self.data_manager.delete_checklist_item(item_id)
        self.refresh()
    
    def _check_all(self) -> None:
        """
        Coche tous les items.
        """
        checklist = self.data_manager.get_checklist()
        
        for item in checklist:
            if not item.get('checked', False):
                self.data_manager.toggle_checklist_item(item['id'])
        
        self.refresh()
    
    def _uncheck_all(self) -> None:
        """
        Decoche tous les items.
        """
        checklist = self.data_manager.get_checklist()
        
        for item in checklist:
            if item.get('checked', False):
                self.data_manager.toggle_checklist_item(item['id'])
        
        self.refresh()
    
    def _delete_checked(self) -> None:
        """
        Supprime tous les items coches.
        """
        checklist = self.data_manager.get_checklist()
        checked_items = [item for item in checklist if item.get('checked', False)]
        
        if not checked_items:
            messagebox.showinfo("Info", "Aucun item coché à supprimer.")
            return
        
        confirm = messagebox.askyesno(
            "Confirmation",
            f"Supprimer {len(checked_items)} item(s) coché(s) ?"
        )
        
        if confirm:
            for item in checked_items:
                self.data_manager.delete_checklist_item(item['id'])
            
            self.refresh()
    
    def _update_progress(self) -> None:
        """
        Met a jour la barre de progression.
        """
        checked, total, percentage = self.data_manager.get_checklist_progress()
        
        self.var_progress.set(f"{percentage}%")
        self.var_progress_text.set(f"{checked}/{total} items cochés")
        self.progressbar["value"] = percentage
        
        # Mettre a jour les checkbuttons
        checklist = self.data_manager.get_checklist()
        for item in checklist:
            item_id = item.get('id')
            if item_id in self.checkbuttons:
                self.checkbuttons[item_id].set(item.get('checked', False))
    
    def refresh(self) -> None:
        """
        Rafraichit la liste complete.
        """
        # Nettoyer
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        self.checkbuttons.clear()
        
        # Recuperer les items
        checklist = self.data_manager.get_checklist()
        
        # Organiser par categorie
        by_category: Dict[str, list] = {}
        for item in checklist:
            cat = item.get('categorie', 'Autre')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)
        
        # Afficher par categorie
        row = 0
        
        for categorie in CHECKLIST_CATEGORIES:
            items = by_category.get(categorie, [])
            
            if not items:
                continue
            
            # En-tete de categorie
            icon = self._get_category_icon(categorie)
            cat_label = tk.Label(
                self.items_frame,
                text=f"{icon} {categorie}",
                font=FONTS["heading"],
                bg="white",
                fg=COLORS["secondary"]
            )
            cat_label.grid(row=row, column=0, columnspan=3, sticky="w", padx=10, pady=(15, 5))
            row += 1
            
            # Separateur
            sep = ttk.Separator(self.items_frame, orient="horizontal")
            sep.grid(row=row, column=0, columnspan=3, sticky="ew", padx=10)
            row += 1
            
            # Items de cette categorie
            for item in items:
                item_id = item.get('id')
                
                # Variable pour la checkbox
                var = tk.BooleanVar(value=item.get('checked', False))
                self.checkbuttons[item_id] = var
                
                # Checkbox avec le texte
                cb = tk.Checkbutton(
                    self.items_frame,
                    text=item.get('item', ''),
                    variable=var,
                    font=FONTS["body"],
                    bg="white",
                    activebackground="white",
                    command=lambda iid=item_id: self._toggle_item(iid)
                )
                cb.grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=2)
                
                # Bouton supprimer
                del_btn = tk.Button(
                    self.items_frame,
                    text="🗑️",
                    font=("Segoe UI", 8),
                    bg="white",
                    relief="flat",
                    cursor="hand2",
                    command=lambda iid=item_id: self._delete_item(iid)
                )
                del_btn.grid(row=row, column=2, sticky="e", padx=10)
                
                row += 1
        
        # Si aucun item
        if not checklist:
            tk.Label(
                self.items_frame,
                text="Aucun item dans la checklist.\nAjoutez des affaires à emporter !",
                font=FONTS["body"],
                bg="white",
                fg="#666666",
                justify="center"
            ).grid(row=0, column=0, pady=50, padx=50)
        
        # Mettre a jour la progression
        self._update_progress()

