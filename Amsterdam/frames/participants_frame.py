"""
participants_frame.py - Gestion des participants au voyage a Amsterdam.

Ce module permet de gerer la liste des voyageurs:
- Ajouter, modifier, supprimer des participants
- Stocker leurs informations de contact
- Noter les allergies et informations medicales

IMPORTANT: Ce frame utilise le gestionnaire de layout PACK
pour organiser les widgets verticalement.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, PARTICIPANT_ROLES


class ParticipantsFrame(ttk.Frame):
    """
    Frame de gestion des participants du voyage.
    
    Ce frame utilise le gestionnaire PACK pour organiser
    les elements verticalement.
    
    Attributes:
        data_manager: Reference au gestionnaire de donnees
        selected_id: ID du participant selectionne
    """
    
    def __init__(self, parent: tk.Widget, data_manager: Any) -> None:
        """
        Initialise le frame des participants.
        
        Args:
            parent: Le widget parent (Notebook)
            data_manager: Reference au gestionnaire de donnees
        """
        super().__init__(parent)
        
        self.data_manager = data_manager
        self.selected_id: Optional[int] = None
        
        # Variables
        self._init_variables()
        
        # Creer l'interface avec PACK
        self._create_widgets()
        
        # Charger les donnees
        self.refresh()
    
    def _init_variables(self) -> None:
        """
        Initialise les variables du formulaire.
        """
        self.var_nom = tk.StringVar()
        self.var_prenom = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telephone = tk.StringVar()
        self.var_role = tk.StringVar()
        self.var_date_naissance = tk.StringVar()
        self.var_allergies = tk.StringVar()
        self.var_notes = tk.StringVar()
    
    def _create_widgets(self) -> None:
        """
        Cree tous les widgets du frame.
        
        Utilise PACK pour organiser les elements.
        """
        # ============================================
        # EN-TETE (utilise PACK)
        # ============================================
        
        header = tk.Frame(self, bg=COLORS["primary"], pady=15)
        header.pack(fill="x", padx=10, pady=(10, 0))
        
        tk.Label(
            header,
            text="👥 Liste des Participants",
            font=FONTS["title"],
            fg=COLORS["text_light"],
            bg=COLORS["primary"]
        ).pack()
        
        # ============================================
        # CONTENEUR PRINCIPAL (utilise PACK)
        # ============================================
        
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ============================================
        # FORMULAIRE (utilise PACK)
        # ============================================
        
        form_frame = ttk.LabelFrame(main_container, text="📝 Informations du participant", padding=15)
        form_frame.pack(fill="x", pady=(0, 10))
        
        # Ligne 1: Nom et Prenom
        row1 = ttk.Frame(form_frame)
        row1.pack(fill="x", pady=5)
        
        ttk.Label(row1, text="Nom:", width=12).pack(side="left")
        ttk.Entry(row1, textvariable=self.var_nom, width=20).pack(side="left", padx=5)
        
        ttk.Label(row1, text="Prénom:", width=10).pack(side="left", padx=(20, 0))
        ttk.Entry(row1, textvariable=self.var_prenom, width=20).pack(side="left", padx=5)
        
        ttk.Label(row1, text="Rôle:", width=8).pack(side="left", padx=(20, 0))
        ttk.Combobox(
            row1,
            textvariable=self.var_role,
            values=PARTICIPANT_ROLES,
            width=18
        ).pack(side="left", padx=5)
        
        # Ligne 2: Contact
        row2 = ttk.Frame(form_frame)
        row2.pack(fill="x", pady=5)
        
        ttk.Label(row2, text="Email:", width=12).pack(side="left")
        ttk.Entry(row2, textvariable=self.var_email, width=30).pack(side="left", padx=5)
        
        ttk.Label(row2, text="Téléphone:", width=12).pack(side="left", padx=(20, 0))
        ttk.Entry(row2, textvariable=self.var_telephone, width=20).pack(side="left", padx=5)
        
        # Ligne 3: Date de naissance et allergies
        row3 = ttk.Frame(form_frame)
        row3.pack(fill="x", pady=5)
        
        ttk.Label(row3, text="Naissance:", width=12).pack(side="left")
        ttk.Entry(row3, textvariable=self.var_date_naissance, width=15).pack(side="left", padx=5)
        ttk.Label(row3, text="(AAAA-MM-JJ)", font=FONTS["small"]).pack(side="left")
        
        ttk.Label(row3, text="Allergies:", width=12).pack(side="left", padx=(20, 0))
        ttk.Entry(row3, textvariable=self.var_allergies, width=30).pack(side="left", padx=5)
        
        # Ligne 4: Notes
        row4 = ttk.Frame(form_frame)
        row4.pack(fill="x", pady=5)
        
        ttk.Label(row4, text="Notes:", width=12).pack(side="left")
        ttk.Entry(row4, textvariable=self.var_notes, width=60).pack(side="left", padx=5, fill="x", expand=True)
        
        # Boutons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(
            btn_frame,
            text="➕ Ajouter",
            command=self._add_participant
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="✏️ Modifier",
            command=self._update_participant
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="🗑️ Supprimer",
            command=self._delete_participant
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔄 Effacer",
            command=self._clear_form
        ).pack(side="left", padx=5)
        
        # ============================================
        # LISTE DES PARTICIPANTS (utilise PACK)
        # ============================================
        
        list_frame = ttk.LabelFrame(main_container, text="📋 Participants inscrits", padding=10)
        list_frame.pack(fill="both", expand=True)
        
        # Container pour le Treeview et scrollbar
        tree_container = ttk.Frame(list_frame)
        tree_container.pack(fill="both", expand=True)
        
        # Colonnes
        columns = ("nom", "prenom", "role", "email", "telephone")
        
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # En-tetes
        self.tree.heading("nom", text="Nom")
        self.tree.heading("prenom", text="Prénom")
        self.tree.heading("role", text="Rôle")
        self.tree.heading("email", text="Email")
        self.tree.heading("telephone", text="Téléphone")
        
        # Largeurs
        self.tree.column("nom", width=120)
        self.tree.column("prenom", width=120)
        self.tree.column("role", width=150)
        self.tree.column("email", width=200)
        self.tree.column("telephone", width=120)
        
        # PACK le treeview
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_container,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Evenements
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)
        
        # ============================================
        # RESUME (utilise PACK)
        # ============================================
        
        summary_frame = ttk.Frame(main_container)
        summary_frame.pack(fill="x", pady=10)
        
        self.var_total = tk.StringVar(value="0 participant(s)")
        
        ttk.Label(
            summary_frame,
            textvariable=self.var_total,
            font=FONTS["body_bold"]
        ).pack(side="left")
        
        # Compteurs par role
        self.role_counts = tk.StringVar(value="")
        ttk.Label(
            summary_frame,
            textvariable=self.role_counts,
            font=FONTS["small"]
        ).pack(side="right")
    
    def _add_participant(self) -> None:
        """
        Ajoute un nouveau participant.
        """
        if not self.var_nom.get().strip() or not self.var_prenom.get().strip():
            messagebox.showwarning("Attention", "Le nom et le prénom sont obligatoires.")
            return
        
        participant = {
            "nom": self.var_nom.get().strip(),
            "prenom": self.var_prenom.get().strip(),
            "email": self.var_email.get().strip(),
            "telephone": self.var_telephone.get().strip(),
            "role": self.var_role.get() or "Participant",
            "date_naissance": self.var_date_naissance.get().strip(),
            "allergies": self.var_allergies.get().strip(),
            "notes": self.var_notes.get().strip()
        }
        
        self.data_manager.add_participant(participant)
        self.refresh()
        self._clear_form()
        
        messagebox.showinfo("Succès", "Participant ajouté !")
    
    def _update_participant(self) -> None:
        """
        Met a jour le participant selectionne.
        """
        if not self.selected_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner un participant.")
            return
        
        if not self.var_nom.get().strip() or not self.var_prenom.get().strip():
            messagebox.showwarning("Attention", "Le nom et le prénom sont obligatoires.")
            return
        
        participant = {
            "nom": self.var_nom.get().strip(),
            "prenom": self.var_prenom.get().strip(),
            "email": self.var_email.get().strip(),
            "telephone": self.var_telephone.get().strip(),
            "role": self.var_role.get() or "Participant",
            "date_naissance": self.var_date_naissance.get().strip(),
            "allergies": self.var_allergies.get().strip(),
            "notes": self.var_notes.get().strip()
        }
        
        self.data_manager.update_participant(self.selected_id, participant)
        self.refresh()
        self._clear_form()
        
        messagebox.showinfo("Succès", "Participant modifié !")
    
    def _delete_participant(self) -> None:
        """
        Supprime le participant selectionne.
        """
        if not self.selected_id:
            messagebox.showwarning("Attention", "Veuillez sélectionner un participant.")
            return
        
        confirm = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir supprimer ce participant ?"
        )
        
        if confirm:
            self.data_manager.delete_participant(self.selected_id)
            self.refresh()
            self._clear_form()
    
    def _clear_form(self) -> None:
        """
        Efface le formulaire.
        """
        self.var_nom.set("")
        self.var_prenom.set("")
        self.var_email.set("")
        self.var_telephone.set("")
        self.var_role.set("")
        self.var_date_naissance.set("")
        self.var_allergies.set("")
        self.var_notes.set("")
        self.selected_id = None
        
        # Deselectionner
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def _on_select(self, event: tk.Event) -> None:
        """
        Callback de selection.
        """
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            tags = self.tree.item(item)["tags"]
            self.selected_id = int(tags[0]) if tags else None
    
    def _on_double_click(self, event: tk.Event) -> None:
        """
        Callback de double-clic - remplit le formulaire.
        """
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        tags = self.tree.item(item)["tags"]
        
        if not tags:
            return
        
        self.selected_id = int(tags[0])
        
        # Trouver le participant
        participants = self.data_manager.get_participants()
        for p in participants:
            if p.get('id') == self.selected_id:
                self.var_nom.set(p.get('nom', ''))
                self.var_prenom.set(p.get('prenom', ''))
                self.var_email.set(p.get('email', ''))
                self.var_telephone.set(p.get('telephone', ''))
                self.var_role.set(p.get('role', ''))
                self.var_date_naissance.set(p.get('date_naissance', ''))
                self.var_allergies.set(p.get('allergies', ''))
                self.var_notes.set(p.get('notes', ''))
                break
    
    def refresh(self) -> None:
        """
        Rafraichit la liste des participants.
        """
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Recuperer les participants
        participants = self.data_manager.get_participants()
        
        # Compteurs par role
        role_count = {}
        
        # Remplir le tableau
        for p in sorted(participants, key=lambda x: x.get('nom', '')):
            # Compter les roles
            role = p.get('role', 'Participant')
            role_count[role] = role_count.get(role, 0) + 1
            
            self.tree.insert(
                "",
                "end",
                values=(
                    p.get('nom', ''),
                    p.get('prenom', ''),
                    role,
                    p.get('email', ''),
                    p.get('telephone', '')
                ),
                tags=(p.get('id'),)
            )
        
        # Mettre a jour le total
        total = len(participants)
        self.var_total.set(f"{total} participant(s)")
        
        # Afficher le compte par role
        role_text = " | ".join([f"{role}: {count}" for role, count in role_count.items()])
        self.role_counts.set(role_text)

