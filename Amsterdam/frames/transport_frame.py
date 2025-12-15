"""
transport_frame.py - Planning des transports pour le voyage a Amsterdam.

Ce module gere les informations de transport:
- Trajet aller (train, avion, bus)
- Trajet retour
- Transports sur place

IMPORTANT: Ce frame utilise le gestionnaire de layout GRID
pour organiser les informations en tableau.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, TRANSPORT_TYPES, format_date


class TransportFrame(ttk.Frame):
    """
    Frame de gestion des transports du voyage.
    
    Ce frame utilise le gestionnaire GRID pour organiser
    les informations de transport en sections.
    
    Attributes:
        data_manager: Reference au gestionnaire de donnees
    """
    
    def __init__(self, parent: tk.Widget, data_manager: Any) -> None:
        """
        Initialise le frame des transports.
        
        Args:
            parent: Le widget parent (Notebook)
            data_manager: Reference au gestionnaire de donnees
        """
        super().__init__(parent)
        
        self.data_manager = data_manager
        
        # Variables
        self._init_variables()
        
        # Creer l'interface
        self._create_widgets()
        
        # Charger les donnees
        self.refresh()
    
    def _init_variables(self) -> None:
        """
        Initialise les variables des formulaires.
        """
        # Variables pour le trajet aller
        self.aller_type = tk.StringVar()
        self.aller_compagnie = tk.StringVar()
        self.aller_numero = tk.StringVar()
        self.aller_depart_lieu = tk.StringVar()
        self.aller_depart_date = tk.StringVar()
        self.aller_depart_heure = tk.StringVar()
        self.aller_arrivee_lieu = tk.StringVar()
        self.aller_arrivee_heure = tk.StringVar()
        self.aller_place = tk.StringVar()
        self.aller_notes = tk.StringVar()
        
        # Variables pour le trajet retour
        self.retour_type = tk.StringVar()
        self.retour_compagnie = tk.StringVar()
        self.retour_numero = tk.StringVar()
        self.retour_depart_lieu = tk.StringVar()
        self.retour_depart_date = tk.StringVar()
        self.retour_depart_heure = tk.StringVar()
        self.retour_arrivee_lieu = tk.StringVar()
        self.retour_arrivee_heure = tk.StringVar()
        self.retour_place = tk.StringVar()
        self.retour_notes = tk.StringVar()
    
    def _create_widgets(self) -> None:
        """
        Cree tous les widgets du frame.
        
        Utilise GRID pour organiser les elements.
        """
        # Configuration du grid principal
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        
        # ============================================
        # EN-TETE (utilise GRID)
        # ============================================
        
        header = tk.Frame(self, bg=COLORS["secondary"], pady=15)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))
        
        tk.Label(
            header,
            text="🚂 Planning des Transports",
            font=FONTS["title"],
            fg=COLORS["text_light"],
            bg=COLORS["secondary"]
        ).pack()
        
        # ============================================
        # TRAJET ALLER (utilise GRID)
        # ============================================
        
        aller_frame = ttk.LabelFrame(self, text="✈️ Trajet Aller", padding=15)
        aller_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self._create_transport_form(aller_frame, "aller")
        
        # ============================================
        # TRAJET RETOUR (utilise GRID)
        # ============================================
        
        retour_frame = ttk.LabelFrame(self, text="🏠 Trajet Retour", padding=15)
        retour_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        self._create_transport_form(retour_frame, "retour")
        
        # ============================================
        # TRANSPORTS SUR PLACE (utilise GRID)
        # ============================================
        
        local_frame = ttk.LabelFrame(self, text="🚋 Transports sur place", padding=15)
        local_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        local_frame.columnconfigure(0, weight=1)
        local_frame.rowconfigure(1, weight=1)
        
        # Formulaire d'ajout
        add_frame = ttk.Frame(local_frame)
        add_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(add_frame, text="Type:").grid(row=0, column=0, padx=5)
        self.local_type = ttk.Combobox(
            add_frame,
            values=["Métro", "Tramway", "Bus", "Vélo", "À pied"],
            width=12
        )
        self.local_type.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Description:").grid(row=0, column=2, padx=5)
        self.local_desc = ttk.Entry(add_frame, width=40)
        self.local_desc.grid(row=0, column=3, padx=5)
        
        ttk.Label(add_frame, text="Prix:").grid(row=0, column=4, padx=5)
        self.local_prix = ttk.Entry(add_frame, width=10)
        self.local_prix.grid(row=0, column=5, padx=5)
        
        ttk.Button(
            add_frame,
            text="➕ Ajouter",
            command=self._add_local_transport
        ).grid(row=0, column=6, padx=10)
        
        # Liste des transports locaux
        columns = ("type", "description", "prix")
        self.local_tree = ttk.Treeview(
            local_frame,
            columns=columns,
            show="headings",
            height=5
        )
        
        self.local_tree.heading("type", text="Type")
        self.local_tree.heading("description", text="Description")
        self.local_tree.heading("prix", text="Prix")
        
        self.local_tree.column("type", width=100)
        self.local_tree.column("description", width=300)
        self.local_tree.column("prix", width=100, anchor="e")
        
        self.local_tree.grid(row=1, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            local_frame,
            orient="vertical",
            command=self.local_tree.yview
        )
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.local_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bouton supprimer
        ttk.Button(
            local_frame,
            text="🗑️ Supprimer sélection",
            command=self._delete_local_transport
        ).grid(row=2, column=0, pady=10)
        
        # ============================================
        # BOUTONS DE SAUVEGARDE (utilise GRID)
        # ============================================
        
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame,
            text="💾 Sauvegarder tout",
            command=self._save_all
        ).grid(row=0, column=0, padx=10)
        
        ttk.Button(
            btn_frame,
            text="🔄 Réinitialiser",
            command=self.refresh
        ).grid(row=0, column=1, padx=10)
    
    def _create_transport_form(self, parent: ttk.Frame, prefix: str) -> None:
        """
        Cree un formulaire de transport (aller ou retour).
        
        Args:
            parent: Le frame parent
            prefix: 'aller' ou 'retour' pour identifier les variables
        """
        # Configuration du grid
        parent.columnconfigure(1, weight=1)
        
        # Recuperer les variables
        vars = {
            "type": getattr(self, f"{prefix}_type"),
            "compagnie": getattr(self, f"{prefix}_compagnie"),
            "numero": getattr(self, f"{prefix}_numero"),
            "depart_lieu": getattr(self, f"{prefix}_depart_lieu"),
            "depart_date": getattr(self, f"{prefix}_depart_date"),
            "depart_heure": getattr(self, f"{prefix}_depart_heure"),
            "arrivee_lieu": getattr(self, f"{prefix}_arrivee_lieu"),
            "arrivee_heure": getattr(self, f"{prefix}_arrivee_heure"),
            "place": getattr(self, f"{prefix}_place"),
            "notes": getattr(self, f"{prefix}_notes"),
        }
        
        row = 0
        
        # Type de transport
        ttk.Label(parent, text="Type:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Combobox(
            parent,
            textvariable=vars["type"],
            values=TRANSPORT_TYPES,
            width=15
        ).grid(row=row, column=1, sticky="w", padx=5, pady=3)
        row += 1
        
        # Compagnie
        ttk.Label(parent, text="Compagnie:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["compagnie"], width=20).grid(
            row=row, column=1, sticky="w", padx=5, pady=3
        )
        row += 1
        
        # Numero
        ttk.Label(parent, text="N° Vol/Train:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["numero"], width=15).grid(
            row=row, column=1, sticky="w", padx=5, pady=3
        )
        row += 1
        
        # Separateur
        ttk.Separator(parent, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10
        )
        row += 1
        
        # Depart
        ttk.Label(parent, text="📍 Départ", font=FONTS["body_bold"]).grid(
            row=row, column=0, columnspan=2, sticky="w", padx=5, pady=5
        )
        row += 1
        
        ttk.Label(parent, text="Lieu:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["depart_lieu"], width=25).grid(
            row=row, column=1, sticky="w", padx=5, pady=3
        )
        row += 1
        
        ttk.Label(parent, text="Date:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["depart_date"], width=12).grid(
            row=row, column=1, sticky="w", padx=5, pady=3
        )
        row += 1
        
        ttk.Label(parent, text="Heure:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["depart_heure"], width=8).grid(
            row=row, column=1, sticky="w", padx=5, pady=3
        )
        row += 1
        
        # Separateur
        ttk.Separator(parent, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10
        )
        row += 1
        
        # Arrivee
        ttk.Label(parent, text="🎯 Arrivée", font=FONTS["body_bold"]).grid(
            row=row, column=0, columnspan=2, sticky="w", padx=5, pady=5
        )
        row += 1
        
        ttk.Label(parent, text="Lieu:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["arrivee_lieu"], width=25).grid(
            row=row, column=1, sticky="w", padx=5, pady=3
        )
        row += 1
        
        ttk.Label(parent, text="Heure:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["arrivee_heure"], width=8).grid(
            row=row, column=1, sticky="w", padx=5, pady=3
        )
        row += 1
        
        # Separateur
        ttk.Separator(parent, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10
        )
        row += 1
        
        # Place/Siege
        ttk.Label(parent, text="Place/Siège:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["place"], width=15).grid(
            row=row, column=1, sticky="w", padx=5, pady=3
        )
        row += 1
        
        # Notes
        ttk.Label(parent, text="Notes:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
        ttk.Entry(parent, textvariable=vars["notes"], width=30).grid(
            row=row, column=1, sticky="ew", padx=5, pady=3
        )
    
    def _add_local_transport(self) -> None:
        """
        Ajoute un transport local.
        """
        transport_type = self.local_type.get()
        description = self.local_desc.get()
        
        if not transport_type or not description:
            messagebox.showwarning("Attention", "Veuillez remplir le type et la description.")
            return
        
        try:
            prix = float(self.local_prix.get() or 0)
        except ValueError:
            messagebox.showerror("Erreur", "Le prix doit être un nombre.")
            return
        
        # Ajouter au transport
        transport = self.data_manager.get_transport()
        sur_place = transport.get('sur_place', [])
        
        sur_place.append({
            "type": transport_type,
            "description": description,
            "prix": prix
        })
        
        transport['sur_place'] = sur_place
        self.data_manager.update_transport(transport)
        
        # Rafraichir
        self._refresh_local_tree()
        
        # Vider les champs
        self.local_type.set("")
        self.local_desc.delete(0, "end")
        self.local_prix.delete(0, "end")
    
    def _delete_local_transport(self) -> None:
        """
        Supprime le transport local selectionne.
        """
        selection = self.local_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un transport.")
            return
        
        # Obtenir l'index
        item = selection[0]
        index = self.local_tree.index(item)
        
        # Supprimer
        transport = self.data_manager.get_transport()
        sur_place = transport.get('sur_place', [])
        
        if 0 <= index < len(sur_place):
            del sur_place[index]
            transport['sur_place'] = sur_place
            self.data_manager.update_transport(transport)
            self._refresh_local_tree()
    
    def _refresh_local_tree(self) -> None:
        """
        Rafraichit la liste des transports locaux.
        """
        # Vider
        for item in self.local_tree.get_children():
            self.local_tree.delete(item)
        
        # Remplir
        transport = self.data_manager.get_transport()
        sur_place = transport.get('sur_place', [])
        
        for t in sur_place:
            self.local_tree.insert(
                "",
                "end",
                values=(
                    t.get('type', ''),
                    t.get('description', ''),
                    f"{t.get('prix', 0):.2f} €"
                )
            )
    
    def _save_all(self) -> None:
        """
        Sauvegarde toutes les informations de transport.
        """
        transport = self.data_manager.get_transport()
        
        # Aller
        transport['aller'] = {
            "type": self.aller_type.get(),
            "compagnie": self.aller_compagnie.get(),
            "numero": self.aller_numero.get(),
            "depart_lieu": self.aller_depart_lieu.get(),
            "depart_date": self.aller_depart_date.get(),
            "depart_heure": self.aller_depart_heure.get(),
            "arrivee_lieu": self.aller_arrivee_lieu.get(),
            "arrivee_heure": self.aller_arrivee_heure.get(),
            "place": self.aller_place.get(),
            "notes": self.aller_notes.get()
        }
        
        # Retour
        transport['retour'] = {
            "type": self.retour_type.get(),
            "compagnie": self.retour_compagnie.get(),
            "numero": self.retour_numero.get(),
            "depart_lieu": self.retour_depart_lieu.get(),
            "depart_date": self.retour_depart_date.get(),
            "depart_heure": self.retour_depart_heure.get(),
            "arrivee_lieu": self.retour_arrivee_lieu.get(),
            "arrivee_heure": self.retour_arrivee_heure.get(),
            "place": self.retour_place.get(),
            "notes": self.retour_notes.get()
        }
        
        self.data_manager.update_transport(transport)
        
        messagebox.showinfo("Succès", "Informations de transport sauvegardées !")
    
    def refresh(self) -> None:
        """
        Rafraichit toutes les donnees.
        """
        transport = self.data_manager.get_transport()
        
        # Aller
        aller = transport.get('aller', {})
        self.aller_type.set(aller.get('type', ''))
        self.aller_compagnie.set(aller.get('compagnie', ''))
        self.aller_numero.set(aller.get('numero', ''))
        self.aller_depart_lieu.set(aller.get('depart_lieu', ''))
        self.aller_depart_date.set(aller.get('depart_date', ''))
        self.aller_depart_heure.set(aller.get('depart_heure', ''))
        self.aller_arrivee_lieu.set(aller.get('arrivee_lieu', ''))
        self.aller_arrivee_heure.set(aller.get('arrivee_heure', ''))
        self.aller_place.set(aller.get('place', ''))
        self.aller_notes.set(aller.get('notes', ''))
        
        # Retour
        retour = transport.get('retour', {})
        self.retour_type.set(retour.get('type', ''))
        self.retour_compagnie.set(retour.get('compagnie', ''))
        self.retour_numero.set(retour.get('numero', ''))
        self.retour_depart_lieu.set(retour.get('depart_lieu', ''))
        self.retour_depart_date.set(retour.get('depart_date', ''))
        self.retour_depart_heure.set(retour.get('depart_heure', ''))
        self.retour_arrivee_lieu.set(retour.get('arrivee_lieu', ''))
        self.retour_arrivee_heure.set(retour.get('arrivee_heure', ''))
        self.retour_place.set(retour.get('place', ''))
        self.retour_notes.set(retour.get('notes', ''))
        
        # Transports locaux
        self._refresh_local_tree()

