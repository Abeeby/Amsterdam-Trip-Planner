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

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, TRANSPORT_TYPES, format_date


# ============================================
# FONCTIONS DE GESTION DES TRANSPORTS
# ============================================

def add_local_transport(frame):
    """
    Ajoute un transport local.

    Args:
        frame: Le frame contenant les variables
    """
    transport_type = frame.local_type.get()
    description = frame.local_desc.get()

    if not transport_type or not description:
        messagebox.showwarning("Attention", "Veuillez remplir le type et la description.")
        return

    try:
        prix = float(frame.local_prix.get() or 0)
    except ValueError:
        messagebox.showerror("Erreur", "Le prix doit etre un nombre.")
        return

    # Ajouter au transport
    transport = frame.data_manager.get_transport()
    sur_place = transport.get('sur_place', [])

    sur_place.append({
        "type": transport_type,
        "description": description,
        "prix": prix
    })

    transport['sur_place'] = sur_place
    frame.data_manager.update_transport(transport)

    # Rafraichir
    refresh_local_tree(frame)

    # Vider les champs
    frame.local_type.set("")
    frame.local_desc.delete(0, "end")
    frame.local_prix.delete(0, "end")


def delete_local_transport(frame):
    """
    Supprime le transport local selectionne.

    Args:
        frame: Le frame contenant le treeview
    """
    selection = frame.local_tree.selection()
    if not selection:
        messagebox.showwarning("Attention", "Veuillez selectionner un transport.")
        return

    # Obtenir l'index
    item = selection[0]
    index = frame.local_tree.index(item)

    # Supprimer
    transport = frame.data_manager.get_transport()
    sur_place = transport.get('sur_place', [])

    if 0 <= index < len(sur_place):
        del sur_place[index]
        transport['sur_place'] = sur_place
        frame.data_manager.update_transport(transport)
        refresh_local_tree(frame)


def refresh_local_tree(frame):
    """
    Rafraichit la liste des transports locaux.

    Args:
        frame: Le frame contenant le treeview
    """
    # Vider
    for item in frame.local_tree.get_children():
        frame.local_tree.delete(item)

    # Remplir
    transport = frame.data_manager.get_transport()
    sur_place = transport.get('sur_place', [])

    for t in sur_place:
        frame.local_tree.insert(
            "",
            "end",
            values=(
                t.get('type', ''),
                t.get('description', ''),
                "{:.2f} EUR".format(t.get('prix', 0))
            )
        )


def save_all(frame):
    """
    Sauvegarde toutes les informations de transport.

    Args:
        frame: Le frame contenant les variables
    """
    transport = frame.data_manager.get_transport()

    # Aller
    transport['aller'] = {
        "type": frame.aller_type.get(),
        "compagnie": frame.aller_compagnie.get(),
        "numero": frame.aller_numero.get(),
        "depart_lieu": frame.aller_depart_lieu.get(),
        "depart_date": frame.aller_depart_date.get(),
        "depart_heure": frame.aller_depart_heure.get(),
        "arrivee_lieu": frame.aller_arrivee_lieu.get(),
        "arrivee_heure": frame.aller_arrivee_heure.get(),
        "place": frame.aller_place.get(),
        "notes": frame.aller_notes.get()
    }

    # Retour
    transport['retour'] = {
        "type": frame.retour_type.get(),
        "compagnie": frame.retour_compagnie.get(),
        "numero": frame.retour_numero.get(),
        "depart_lieu": frame.retour_depart_lieu.get(),
        "depart_date": frame.retour_depart_date.get(),
        "depart_heure": frame.retour_depart_heure.get(),
        "arrivee_lieu": frame.retour_arrivee_lieu.get(),
        "arrivee_heure": frame.retour_arrivee_heure.get(),
        "place": frame.retour_place.get(),
        "notes": frame.retour_notes.get()
    }

    frame.data_manager.update_transport(transport)

    messagebox.showinfo("Succes", "Informations de transport sauvegardees !")


def refresh_transport(frame):
    """
    Rafraichit toutes les donnees.

    Args:
        frame: Le frame contenant les variables
    """
    transport = frame.data_manager.get_transport()

    # Aller
    aller = transport.get('aller', {})
    frame.aller_type.set(aller.get('type', ''))
    frame.aller_compagnie.set(aller.get('compagnie', ''))
    frame.aller_numero.set(aller.get('numero', ''))
    frame.aller_depart_lieu.set(aller.get('depart_lieu', ''))
    frame.aller_depart_date.set(aller.get('depart_date', ''))
    frame.aller_depart_heure.set(aller.get('depart_heure', ''))
    frame.aller_arrivee_lieu.set(aller.get('arrivee_lieu', ''))
    frame.aller_arrivee_heure.set(aller.get('arrivee_heure', ''))
    frame.aller_place.set(aller.get('place', ''))
    frame.aller_notes.set(aller.get('notes', ''))

    # Retour
    retour = transport.get('retour', {})
    frame.retour_type.set(retour.get('type', ''))
    frame.retour_compagnie.set(retour.get('compagnie', ''))
    frame.retour_numero.set(retour.get('numero', ''))
    frame.retour_depart_lieu.set(retour.get('depart_lieu', ''))
    frame.retour_depart_date.set(retour.get('depart_date', ''))
    frame.retour_depart_heure.set(retour.get('depart_heure', ''))
    frame.retour_arrivee_lieu.set(retour.get('arrivee_lieu', ''))
    frame.retour_arrivee_heure.set(retour.get('arrivee_heure', ''))
    frame.retour_place.set(retour.get('place', ''))
    frame.retour_notes.set(retour.get('notes', ''))

    # Transports locaux
    refresh_local_tree(frame)


# ============================================
# FONCTION POUR CREER UN FORMULAIRE DE TRANSPORT
# ============================================

def create_transport_form(parent, frame, prefix):
    """
    Cree un formulaire de transport (aller ou retour).

    Args:
        parent: Le frame parent
        frame: Le frame principal contenant les variables
        prefix: 'aller' ou 'retour' pour identifier les variables
    """
    # Configuration du grid
    parent.columnconfigure(1, weight=1)

    # Recuperer les variables
    vars_dict = {
        "type": getattr(frame, prefix + "_type"),
        "compagnie": getattr(frame, prefix + "_compagnie"),
        "numero": getattr(frame, prefix + "_numero"),
        "depart_lieu": getattr(frame, prefix + "_depart_lieu"),
        "depart_date": getattr(frame, prefix + "_depart_date"),
        "depart_heure": getattr(frame, prefix + "_depart_heure"),
        "arrivee_lieu": getattr(frame, prefix + "_arrivee_lieu"),
        "arrivee_heure": getattr(frame, prefix + "_arrivee_heure"),
        "place": getattr(frame, prefix + "_place"),
        "notes": getattr(frame, prefix + "_notes"),
    }

    row = 0

    # Type de transport
    ttk.Label(parent, text="Type:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Combobox(
        parent,
        textvariable=vars_dict["type"],
        values=TRANSPORT_TYPES,
        width=15
    ).grid(row=row, column=1, sticky="w", padx=5, pady=3)
    row += 1

    # Compagnie
    ttk.Label(parent, text="Compagnie:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["compagnie"], width=20).grid(
        row=row, column=1, sticky="w", padx=5, pady=3
    )
    row += 1

    # Numero
    ttk.Label(parent, text="N Vol/Train:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["numero"], width=15).grid(
        row=row, column=1, sticky="w", padx=5, pady=3
    )
    row += 1

    # Separateur
    ttk.Separator(parent, orient="horizontal").grid(
        row=row, column=0, columnspan=2, sticky="ew", pady=10
    )
    row += 1

    # Depart
    ttk.Label(parent, text="DEPART", font=FONTS["body_bold"]).grid(
        row=row, column=0, columnspan=2, sticky="w", padx=5, pady=5
    )
    row += 1

    ttk.Label(parent, text="Lieu:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["depart_lieu"], width=25).grid(
        row=row, column=1, sticky="w", padx=5, pady=3
    )
    row += 1

    ttk.Label(parent, text="Date:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["depart_date"], width=12).grid(
        row=row, column=1, sticky="w", padx=5, pady=3
    )
    row += 1

    ttk.Label(parent, text="Heure:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["depart_heure"], width=8).grid(
        row=row, column=1, sticky="w", padx=5, pady=3
    )
    row += 1

    # Separateur
    ttk.Separator(parent, orient="horizontal").grid(
        row=row, column=0, columnspan=2, sticky="ew", pady=10
    )
    row += 1

    # Arrivee
    ttk.Label(parent, text="ARRIVEE", font=FONTS["body_bold"]).grid(
        row=row, column=0, columnspan=2, sticky="w", padx=5, pady=5
    )
    row += 1

    ttk.Label(parent, text="Lieu:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["arrivee_lieu"], width=25).grid(
        row=row, column=1, sticky="w", padx=5, pady=3
    )
    row += 1

    ttk.Label(parent, text="Heure:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["arrivee_heure"], width=8).grid(
        row=row, column=1, sticky="w", padx=5, pady=3
    )
    row += 1

    # Separateur
    ttk.Separator(parent, orient="horizontal").grid(
        row=row, column=0, columnspan=2, sticky="ew", pady=10
    )
    row += 1

    # Place/Siege
    ttk.Label(parent, text="Place/Siege:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["place"], width=15).grid(
        row=row, column=1, sticky="w", padx=5, pady=3
    )
    row += 1

    # Notes
    ttk.Label(parent, text="Notes:").grid(row=row, column=0, sticky="e", padx=5, pady=3)
    ttk.Entry(parent, textvariable=vars_dict["notes"], width=30).grid(
        row=row, column=1, sticky="ew", padx=5, pady=3
    )


# ============================================
# FONCTION PRINCIPALE DE CREATION DU FRAME
# ============================================

def TransportFrame(parent, data_manager):
    """
    Cree et retourne le frame des transports.

    Ce frame utilise le gestionnaire GRID pour organiser
    les informations de transport en sections.

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

    # Variables pour le trajet aller
    frame.aller_type = tk.StringVar()
    frame.aller_compagnie = tk.StringVar()
    frame.aller_numero = tk.StringVar()
    frame.aller_depart_lieu = tk.StringVar()
    frame.aller_depart_date = tk.StringVar()
    frame.aller_depart_heure = tk.StringVar()
    frame.aller_arrivee_lieu = tk.StringVar()
    frame.aller_arrivee_heure = tk.StringVar()
    frame.aller_place = tk.StringVar()
    frame.aller_notes = tk.StringVar()

    # Variables pour le trajet retour
    frame.retour_type = tk.StringVar()
    frame.retour_compagnie = tk.StringVar()
    frame.retour_numero = tk.StringVar()
    frame.retour_depart_lieu = tk.StringVar()
    frame.retour_depart_date = tk.StringVar()
    frame.retour_depart_heure = tk.StringVar()
    frame.retour_arrivee_lieu = tk.StringVar()
    frame.retour_arrivee_heure = tk.StringVar()
    frame.retour_place = tk.StringVar()
    frame.retour_notes = tk.StringVar()

    # Configuration du grid principal
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)

    # ============================================
    # EN-TETE (utilise GRID)
    # ============================================

    header = tk.Frame(frame, bg=COLORS["secondary"], pady=15)
    header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))

    tk.Label(
        header,
        text="Planning des Transports",
        font=FONTS["title"],
        fg=COLORS["text_light"],
        bg=COLORS["secondary"]
    ).pack()

    # ============================================
    # TRAJET ALLER (utilise GRID)
    # ============================================

    aller_frame = ttk.LabelFrame(frame, text="Trajet Aller", padding=15)
    aller_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    create_transport_form(aller_frame, frame, "aller")

    # ============================================
    # TRAJET RETOUR (utilise GRID)
    # ============================================

    retour_frame = ttk.LabelFrame(frame, text="Trajet Retour", padding=15)
    retour_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    create_transport_form(retour_frame, frame, "retour")

    # ============================================
    # TRANSPORTS SUR PLACE (utilise GRID)
    # ============================================

    local_frame = ttk.LabelFrame(frame, text="Transports sur place", padding=15)
    local_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    local_frame.columnconfigure(0, weight=1)
    local_frame.rowconfigure(1, weight=1)

    # Formulaire d'ajout
    add_frame = ttk.Frame(local_frame)
    add_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    ttk.Label(add_frame, text="Type:").grid(row=0, column=0, padx=5)
    frame.local_type = ttk.Combobox(
        add_frame,
        values=["Metro", "Tramway", "Bus", "Velo", "A pied"],
        width=12
    )
    frame.local_type.grid(row=0, column=1, padx=5)

    ttk.Label(add_frame, text="Description:").grid(row=0, column=2, padx=5)
    frame.local_desc = ttk.Entry(add_frame, width=40)
    frame.local_desc.grid(row=0, column=3, padx=5)

    ttk.Label(add_frame, text="Prix:").grid(row=0, column=4, padx=5)
    frame.local_prix = ttk.Entry(add_frame, width=10)
    frame.local_prix.grid(row=0, column=5, padx=5)

    ttk.Button(
        add_frame,
        text="Ajouter",
        command=lambda: add_local_transport(frame)
    ).grid(row=0, column=6, padx=10)

    # Liste des transports locaux
    columns = ("type", "description", "prix")
    frame.local_tree = ttk.Treeview(
        local_frame,
        columns=columns,
        show="headings",
        height=5
    )

    frame.local_tree.heading("type", text="Type")
    frame.local_tree.heading("description", text="Description")
    frame.local_tree.heading("prix", text="Prix")

    frame.local_tree.column("type", width=100)
    frame.local_tree.column("description", width=300)
    frame.local_tree.column("prix", width=100, anchor="e")

    frame.local_tree.grid(row=1, column=0, sticky="nsew")

    # Scrollbar
    scrollbar = ttk.Scrollbar(
        local_frame,
        orient="vertical",
        command=frame.local_tree.yview
    )
    scrollbar.grid(row=1, column=1, sticky="ns")
    frame.local_tree.configure(yscrollcommand=scrollbar.set)

    # Bouton supprimer
    ttk.Button(
        local_frame,
        text="Supprimer selection",
        command=lambda: delete_local_transport(frame)
    ).grid(row=2, column=0, pady=10)

    # ============================================
    # BOUTONS DE SAUVEGARDE (utilise GRID)
    # ============================================

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

    ttk.Button(
        btn_frame,
        text="Sauvegarder tout",
        command=lambda: save_all(frame)
    ).grid(row=0, column=0, padx=10)

    ttk.Button(
        btn_frame,
        text="Reinitialiser",
        command=lambda: refresh_transport(frame)
    ).grid(row=0, column=1, padx=10)

    # ============================================
    # ATTACHER LA METHODE REFRESH AU FRAME
    # ============================================

    frame.refresh = lambda: refresh_transport(frame)

    # Charger les donnees initiales
    frame.refresh()

    return frame
