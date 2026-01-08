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

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, PARTICIPANT_ROLES


# ============================================
# FONCTIONS DE GESTION DES PARTICIPANTS
# ============================================

def add_participant(frame):
    """
    Ajoute un nouveau participant.

    Args:
        frame: Le frame contenant les variables
    """
    if not frame.var_nom.get().strip() or not frame.var_prenom.get().strip():
        messagebox.showwarning("Attention", "Le nom et le prenom sont obligatoires.")
        return

    participant = {
        "nom": frame.var_nom.get().strip(),
        "prenom": frame.var_prenom.get().strip(),
        "email": frame.var_email.get().strip(),
        "telephone": frame.var_telephone.get().strip(),
        "role": frame.var_role.get() or "Participant",
        "date_naissance": frame.var_date_naissance.get().strip(),
        "allergies": frame.var_allergies.get().strip(),
        "notes": frame.var_notes.get().strip()
    }

    frame.data_manager.add_participant(participant)
    refresh_participants(frame)
    clear_form(frame)

    messagebox.showinfo("Succes", "Participant ajoute !")


def update_participant(frame):
    """
    Met a jour le participant selectionne.

    Args:
        frame: Le frame contenant les variables
    """
    if not frame.selected_id:
        messagebox.showwarning("Attention", "Veuillez selectionner un participant.")
        return

    if not frame.var_nom.get().strip() or not frame.var_prenom.get().strip():
        messagebox.showwarning("Attention", "Le nom et le prenom sont obligatoires.")
        return

    participant = {
        "nom": frame.var_nom.get().strip(),
        "prenom": frame.var_prenom.get().strip(),
        "email": frame.var_email.get().strip(),
        "telephone": frame.var_telephone.get().strip(),
        "role": frame.var_role.get() or "Participant",
        "date_naissance": frame.var_date_naissance.get().strip(),
        "allergies": frame.var_allergies.get().strip(),
        "notes": frame.var_notes.get().strip()
    }

    frame.data_manager.update_participant(frame.selected_id, participant)
    refresh_participants(frame)
    clear_form(frame)

    messagebox.showinfo("Succes", "Participant modifie !")


def delete_participant(frame):
    """
    Supprime le participant selectionne.

    Args:
        frame: Le frame contenant les variables
    """
    if not frame.selected_id:
        messagebox.showwarning("Attention", "Veuillez selectionner un participant.")
        return

    confirm = messagebox.askyesno(
        "Confirmation",
        "Etes-vous sur de vouloir supprimer ce participant ?"
    )

    if confirm:
        frame.data_manager.delete_participant(frame.selected_id)
        refresh_participants(frame)
        clear_form(frame)


def clear_form(frame):
    """
    Efface le formulaire.

    Args:
        frame: Le frame contenant les variables
    """
    frame.var_nom.set("")
    frame.var_prenom.set("")
    frame.var_email.set("")
    frame.var_telephone.set("")
    frame.var_role.set("")
    frame.var_date_naissance.set("")
    frame.var_allergies.set("")
    frame.var_notes.set("")
    frame.selected_id = None

    # Deselectionner
    for item in frame.tree.selection():
        frame.tree.selection_remove(item)


# ============================================
# FONCTIONS DE CALLBACKS
# ============================================

def on_select(frame, event):
    """
    Callback de selection.

    Args:
        frame: Le frame contenant le treeview
        event: L'evenement tkinter
    """
    selection = frame.tree.selection()
    if selection:
        item = selection[0]
        tags = frame.tree.item(item)["tags"]
        frame.selected_id = int(tags[0]) if tags else None


def on_double_click(frame, event):
    """
    Callback de double-clic - remplit le formulaire.

    Args:
        frame: Le frame contenant les variables
        event: L'evenement tkinter
    """
    selection = frame.tree.selection()
    if not selection:
        return

    item = selection[0]
    tags = frame.tree.item(item)["tags"]

    if not tags:
        return

    frame.selected_id = int(tags[0])

    # Trouver le participant
    participants = frame.data_manager.get_participants()
    for p in participants:
        if p.get('id') == frame.selected_id:
            frame.var_nom.set(p.get('nom', ''))
            frame.var_prenom.set(p.get('prenom', ''))
            frame.var_email.set(p.get('email', ''))
            frame.var_telephone.set(p.get('telephone', ''))
            frame.var_role.set(p.get('role', ''))
            frame.var_date_naissance.set(p.get('date_naissance', ''))
            frame.var_allergies.set(p.get('allergies', ''))
            frame.var_notes.set(p.get('notes', ''))
            break


# ============================================
# FONCTION DE RAFRAICHISSEMENT
# ============================================

def refresh_participants(frame):
    """
    Rafraichit la liste des participants.

    Args:
        frame: Le frame contenant le treeview et les variables
    """
    # Vider le tableau
    for item in frame.tree.get_children():
        frame.tree.delete(item)

    # Recuperer les participants
    participants = frame.data_manager.get_participants()

    # Compteurs par role
    role_count = {}

    # Remplir le tableau
    for p in sorted(participants, key=lambda x: x.get('nom', '')):
        # Compter les roles
        role = p.get('role', 'Participant')
        role_count[role] = role_count.get(role, 0) + 1

        frame.tree.insert(
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
    frame.var_total.set("{} participant(s)".format(total))

    # Afficher le compte par role
    role_text = " | ".join(["{}: {}".format(role, count) for role, count in role_count.items()])
    frame.role_counts.set(role_text)


# ============================================
# FONCTION PRINCIPALE DE CREATION DU FRAME
# ============================================

def ParticipantsFrame(parent, data_manager):
    """
    Cree et retourne le frame des participants.

    Ce frame utilise le gestionnaire PACK pour organiser
    les elements verticalement.

    Args:
        parent: Le widget parent (Notebook)
        data_manager: Reference au gestionnaire de donnees

    Returns:
        Le frame configure avec tous ses widgets
    """
    # Creer le frame principal
    frame = ttk.Frame(parent)

    # Stocker les references
    frame.data_manager = data_manager
    frame.selected_id = None

    # Variables du formulaire
    frame.var_nom = tk.StringVar()
    frame.var_prenom = tk.StringVar()
    frame.var_email = tk.StringVar()
    frame.var_telephone = tk.StringVar()
    frame.var_role = tk.StringVar()
    frame.var_date_naissance = tk.StringVar()
    frame.var_allergies = tk.StringVar()
    frame.var_notes = tk.StringVar()

    # ============================================
    # EN-TETE (utilise PACK)
    # ============================================

    header = tk.Frame(frame, bg=COLORS["primary"], pady=15)
    header.pack(fill="x", padx=10, pady=(10, 0))

    tk.Label(
        header,
        text="Liste des Participants",
        font=FONTS["title"],
        fg=COLORS["text_light"],
        bg=COLORS["primary"]
    ).pack()

    # ============================================
    # CONTENEUR PRINCIPAL (utilise PACK)
    # ============================================

    main_container = ttk.Frame(frame)
    main_container.pack(fill="both", expand=True, padx=10, pady=10)

    # ============================================
    # FORMULAIRE (utilise PACK)
    # ============================================

    form_frame = ttk.LabelFrame(main_container, text="Informations du participant", padding=15)
    form_frame.pack(fill="x", pady=(0, 10))

    # Ligne 1: Nom et Prenom
    row1 = ttk.Frame(form_frame)
    row1.pack(fill="x", pady=5)

    ttk.Label(row1, text="Nom:", width=12).pack(side="left")
    ttk.Entry(row1, textvariable=frame.var_nom, width=20).pack(side="left", padx=5)

    ttk.Label(row1, text="Prenom:", width=10).pack(side="left", padx=(20, 0))
    ttk.Entry(row1, textvariable=frame.var_prenom, width=20).pack(side="left", padx=5)

    ttk.Label(row1, text="Role:", width=8).pack(side="left", padx=(20, 0))
    ttk.Combobox(
        row1,
        textvariable=frame.var_role,
        values=PARTICIPANT_ROLES,
        width=18
    ).pack(side="left", padx=5)

    # Ligne 2: Contact
    row2 = ttk.Frame(form_frame)
    row2.pack(fill="x", pady=5)

    ttk.Label(row2, text="Email:", width=12).pack(side="left")
    ttk.Entry(row2, textvariable=frame.var_email, width=30).pack(side="left", padx=5)

    ttk.Label(row2, text="Telephone:", width=12).pack(side="left", padx=(20, 0))
    ttk.Entry(row2, textvariable=frame.var_telephone, width=20).pack(side="left", padx=5)

    # Ligne 3: Date de naissance et allergies
    row3 = ttk.Frame(form_frame)
    row3.pack(fill="x", pady=5)

    ttk.Label(row3, text="Naissance:", width=12).pack(side="left")
    ttk.Entry(row3, textvariable=frame.var_date_naissance, width=15).pack(side="left", padx=5)
    ttk.Label(row3, text="(AAAA-MM-JJ)", font=FONTS["small"]).pack(side="left")

    ttk.Label(row3, text="Allergies:", width=12).pack(side="left", padx=(20, 0))
    ttk.Entry(row3, textvariable=frame.var_allergies, width=30).pack(side="left", padx=5)

    # Ligne 4: Notes
    row4 = ttk.Frame(form_frame)
    row4.pack(fill="x", pady=5)

    ttk.Label(row4, text="Notes:", width=12).pack(side="left")
    ttk.Entry(row4, textvariable=frame.var_notes, width=60).pack(side="left", padx=5, fill="x", expand=True)

    # Boutons
    btn_frame = ttk.Frame(form_frame)
    btn_frame.pack(fill="x", pady=10)

    ttk.Button(
        btn_frame,
        text="Ajouter",
        command=lambda: add_participant(frame)
    ).pack(side="left", padx=5)

    ttk.Button(
        btn_frame,
        text="Modifier",
        command=lambda: update_participant(frame)
    ).pack(side="left", padx=5)

    ttk.Button(
        btn_frame,
        text="Supprimer",
        command=lambda: delete_participant(frame)
    ).pack(side="left", padx=5)

    ttk.Button(
        btn_frame,
        text="Effacer",
        command=lambda: clear_form(frame)
    ).pack(side="left", padx=5)

    # ============================================
    # LISTE DES PARTICIPANTS (utilise PACK)
    # ============================================

    list_frame = ttk.LabelFrame(main_container, text="Participants inscrits", padding=10)
    list_frame.pack(fill="both", expand=True)

    # Container pour le Treeview et scrollbar
    tree_container = ttk.Frame(list_frame)
    tree_container.pack(fill="both", expand=True)

    # Colonnes
    columns = ("nom", "prenom", "role", "email", "telephone")

    frame.tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    # En-tetes
    frame.tree.heading("nom", text="Nom")
    frame.tree.heading("prenom", text="Prenom")
    frame.tree.heading("role", text="Role")
    frame.tree.heading("email", text="Email")
    frame.tree.heading("telephone", text="Telephone")

    # Largeurs
    frame.tree.column("nom", width=120)
    frame.tree.column("prenom", width=120)
    frame.tree.column("role", width=150)
    frame.tree.column("email", width=200)
    frame.tree.column("telephone", width=120)

    # PACK le treeview
    frame.tree.pack(side="left", fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(
        tree_container,
        orient="vertical",
        command=frame.tree.yview
    )
    scrollbar.pack(side="right", fill="y")
    frame.tree.configure(yscrollcommand=scrollbar.set)

    # Evenements
    frame.tree.bind("<<TreeviewSelect>>", lambda e: on_select(frame, e))
    frame.tree.bind("<Double-1>", lambda e: on_double_click(frame, e))

    # ============================================
    # RESUME (utilise PACK)
    # ============================================

    summary_frame = ttk.Frame(main_container)
    summary_frame.pack(fill="x", pady=10)

    frame.var_total = tk.StringVar(value="0 participant(s)")

    ttk.Label(
        summary_frame,
        textvariable=frame.var_total,
        font=FONTS["body_bold"]
    ).pack(side="left")

    # Compteurs par role
    frame.role_counts = tk.StringVar(value="")
    ttk.Label(
        summary_frame,
        textvariable=frame.role_counts,
        font=FONTS["small"]
    ).pack(side="right")

    # ============================================
    # ATTACHER LA METHODE REFRESH AU FRAME
    # ============================================

    frame.refresh = lambda: refresh_participants(frame)

    # Charger les donnees initiales
    frame.refresh()

    return frame
