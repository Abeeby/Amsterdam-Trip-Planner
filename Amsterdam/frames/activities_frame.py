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
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, format_date, format_currency


# ============================================
# FONCTIONS DE GESTION DU FORMULAIRE
# ============================================

def clear_form(frame):
    """
    Efface tous les champs du formulaire.

    Args:
        frame: Le frame contenant les variables du formulaire
    """
    frame.var_date.set("")
    frame.var_nom.set("")
    frame.var_lieu.set("")
    frame.var_horaire.set("")
    frame.var_duree.set("")
    frame.var_prix.set("")
    frame.var_description.set("")
    frame.selected_id = None

    # Deselectionner dans le treeview
    for item in frame.tree.selection():
        frame.tree.selection_remove(item)


def add_activity(frame):
    """
    Ajoute une nouvelle activite.

    Args:
        frame: Le frame contenant les variables et le data_manager
    """
    # Valider les champs obligatoires
    if not frame.var_nom.get().strip():
        messagebox.showwarning("Attention", "Le nom de l'activite est obligatoire.")
        return

    if not frame.var_date.get().strip():
        messagebox.showwarning("Attention", "La date est obligatoire.")
        return

    # Valider le format de la date
    try:
        datetime.strptime(frame.var_date.get(), "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Erreur", "Format de date invalide. Utilisez AAAA-MM-JJ")
        return

    # Valider le prix
    try:
        prix = float(frame.var_prix.get() or 0)
    except ValueError:
        messagebox.showerror("Erreur", "Le prix doit etre un nombre.")
        return

    # Creer l'activite
    activite = {
        "date": frame.var_date.get(),
        "nom": frame.var_nom.get().strip(),
        "lieu": frame.var_lieu.get().strip(),
        "horaire": frame.var_horaire.get().strip(),
        "duree": frame.var_duree.get().strip(),
        "prix": prix,
        "description": frame.var_description.get().strip()
    }

    # Ajouter via le data manager
    frame.data_manager.add_activite(activite)

    # Rafraichir et vider le formulaire
    refresh_activities(frame)
    clear_form(frame)

    messagebox.showinfo("Succes", "Activite ajoutee avec succes !")


def update_activity(frame):
    """
    Met a jour l'activite selectionnee.

    Args:
        frame: Le frame contenant les variables et le data_manager
    """
    if not frame.selected_id:
        messagebox.showwarning("Attention", "Veuillez selectionner une activite.")
        return

    # Valider les champs
    if not frame.var_nom.get().strip():
        messagebox.showwarning("Attention", "Le nom de l'activite est obligatoire.")
        return

    try:
        prix = float(frame.var_prix.get() or 0)
    except ValueError:
        messagebox.showerror("Erreur", "Le prix doit etre un nombre.")
        return

    # Creer l'activite mise a jour
    activite = {
        "date": frame.var_date.get(),
        "nom": frame.var_nom.get().strip(),
        "lieu": frame.var_lieu.get().strip(),
        "horaire": frame.var_horaire.get().strip(),
        "duree": frame.var_duree.get().strip(),
        "prix": prix,
        "description": frame.var_description.get().strip()
    }

    # Mettre a jour via le data manager
    frame.data_manager.update_activite(frame.selected_id, activite)

    # Rafraichir et vider
    refresh_activities(frame)
    clear_form(frame)

    messagebox.showinfo("Succes", "Activite modifiee avec succes !")


def delete_activity(frame):
    """
    Supprime l'activite selectionnee.

    Args:
        frame: Le frame contenant le data_manager et l'ID selectionne
    """
    if not frame.selected_id:
        messagebox.showwarning("Attention", "Veuillez selectionner une activite.")
        return

    # Confirmation
    confirm = messagebox.askyesno(
        "Confirmation",
        "Etes-vous sur de vouloir supprimer cette activite ?"
    )

    if confirm:
        frame.data_manager.delete_activite(frame.selected_id)
        refresh_activities(frame)
        clear_form(frame)
        messagebox.showinfo("Succes", "Activite supprimee.")


# ============================================
# FONCTIONS DE CALLBACKS
# ============================================

def on_select(frame, event):
    """
    Callback lors de la selection d'une ligne.

    Args:
        frame: Le frame contenant le treeview
        event: L'evenement tkinter
    """
    selection = frame.tree.selection()
    if not selection:
        return

    # Recuperer l'ID stocke dans le tag
    item = selection[0]
    tags = frame.tree.item(item)["tags"]
    frame.selected_id = tags[0] if tags else None


def on_double_click(frame, event):
    """
    Callback lors du double-clic sur une ligne.

    Remplit le formulaire avec les donnees de l'activite.

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

    # Trouver l'activite correspondante
    activites = frame.data_manager.get_activites()
    for activite in activites:
        if activite.get('id') == frame.selected_id:
            # Remplir le formulaire
            frame.var_date.set(activite.get('date', ''))
            frame.var_nom.set(activite.get('nom', ''))
            frame.var_lieu.set(activite.get('lieu', ''))
            frame.var_horaire.set(activite.get('horaire', ''))
            frame.var_duree.set(activite.get('duree', ''))
            frame.var_prix.set(str(activite.get('prix', '')))
            frame.var_description.set(activite.get('description', ''))
            break


# ============================================
# FONCTION DE RAFRAICHISSEMENT
# ============================================

def refresh_activities(frame):
    """
    Rafraichit le tableau des activites.

    Args:
        frame: Le frame contenant le treeview et le data_manager
    """
    # Vider le tableau
    for item in frame.tree.get_children():
        frame.tree.delete(item)

    # Recuperer les activites
    activites = frame.data_manager.get_activites()

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

        frame.tree.insert(
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
    frame.var_total_activities.set(str(len(activites)))
    frame.var_total_prix.set(format_currency(total_prix))


# ============================================
# FONCTION PRINCIPALE DE CREATION DU FRAME
# ============================================

def ActivitiesFrame(parent, data_manager):
    """
    Cree et retourne le frame des activites.

    Ce frame utilise le gestionnaire GRID pour organiser
    le formulaire et le tableau des activites.

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

    # Variables pour le formulaire
    frame.var_date = tk.StringVar()
    frame.var_nom = tk.StringVar()
    frame.var_lieu = tk.StringVar()
    frame.var_horaire = tk.StringVar()
    frame.var_duree = tk.StringVar()
    frame.var_prix = tk.StringVar()
    frame.var_description = tk.StringVar()

    # Configuration du grid principal
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    # ============================================
    # FORMULAIRE D'AJOUT/MODIFICATION (utilise GRID)
    # ============================================

    form_frame = ttk.LabelFrame(frame, text="Nouvelle activite", padding=15)
    form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    # Configuration des colonnes du formulaire
    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(3, weight=1)
    form_frame.columnconfigure(5, weight=1)

    # Ligne 1: Date, Nom, Lieu
    ttk.Label(form_frame, text="Date:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_date, width=15).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )
    ttk.Label(form_frame, text="(AAAA-MM-JJ)", font=FONTS["small"]).grid(
        row=0, column=2, sticky="w"
    )

    ttk.Label(form_frame, text="Nom:").grid(
        row=0, column=3, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_nom, width=30).grid(
        row=0, column=4, columnspan=2, sticky="ew", padx=5, pady=5
    )

    # Ligne 2: Lieu, Horaire, Duree
    ttk.Label(form_frame, text="Lieu:").grid(
        row=1, column=0, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_lieu, width=30).grid(
        row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5
    )

    ttk.Label(form_frame, text="Horaire:").grid(
        row=1, column=3, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_horaire, width=10).grid(
        row=1, column=4, sticky="w", padx=5, pady=5
    )

    ttk.Label(form_frame, text="Duree:").grid(
        row=1, column=5, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_duree, width=10).grid(
        row=1, column=6, sticky="w", padx=5, pady=5
    )

    # Ligne 3: Prix, Description
    ttk.Label(form_frame, text="Prix (EUR):").grid(
        row=2, column=0, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_prix, width=10).grid(
        row=2, column=1, sticky="w", padx=5, pady=5
    )

    ttk.Label(form_frame, text="Description:").grid(
        row=2, column=3, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_description, width=40).grid(
        row=2, column=4, columnspan=3, sticky="ew", padx=5, pady=5
    )

    # Ligne 4: Boutons
    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=3, column=0, columnspan=7, pady=10)

    ttk.Button(
        btn_frame,
        text="Ajouter",
        command=lambda: add_activity(frame)
    ).grid(row=0, column=0, padx=5)

    ttk.Button(
        btn_frame,
        text="Modifier",
        command=lambda: update_activity(frame)
    ).grid(row=0, column=1, padx=5)

    ttk.Button(
        btn_frame,
        text="Supprimer",
        command=lambda: delete_activity(frame)
    ).grid(row=0, column=2, padx=5)

    ttk.Button(
        btn_frame,
        text="Effacer",
        command=lambda: clear_form(frame)
    ).grid(row=0, column=3, padx=5)

    # ============================================
    # TABLEAU DES ACTIVITES (utilise GRID)
    # ============================================

    table_frame = ttk.LabelFrame(frame, text="Liste des activites", padding=10)
    table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Configuration du grid pour le tableau
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    # Colonnes du Treeview
    columns = ("date", "nom", "lieu", "horaire", "duree", "prix")

    # Creer le Treeview
    frame.tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    # Configurer les en-tetes
    frame.tree.heading("date", text="Date")
    frame.tree.heading("nom", text="Activite")
    frame.tree.heading("lieu", text="Lieu")
    frame.tree.heading("horaire", text="Horaire")
    frame.tree.heading("duree", text="Duree")
    frame.tree.heading("prix", text="Prix")

    # Configurer les largeurs des colonnes
    frame.tree.column("date", width=100, anchor="center")
    frame.tree.column("nom", width=200)
    frame.tree.column("lieu", width=200)
    frame.tree.column("horaire", width=80, anchor="center")
    frame.tree.column("duree", width=80, anchor="center")
    frame.tree.column("prix", width=80, anchor="e")

    # Placer avec GRID
    frame.tree.grid(row=0, column=0, sticky="nsew")

    # Scrollbar verticale
    scrollbar_y = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=frame.tree.yview
    )
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    frame.tree.configure(yscrollcommand=scrollbar_y.set)

    # Scrollbar horizontale
    scrollbar_x = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=frame.tree.xview
    )
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    frame.tree.configure(xscrollcommand=scrollbar_x.set)

    # Evenement de selection
    frame.tree.bind("<<TreeviewSelect>>", lambda e: on_select(frame, e))
    frame.tree.bind("<Double-1>", lambda e: on_double_click(frame, e))

    # ============================================
    # RESUME (utilise GRID)
    # ============================================

    summary_frame = ttk.Frame(frame)
    summary_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

    # Configuration du grid pour le resume
    summary_frame.columnconfigure(1, weight=1)

    frame.var_total_activities = tk.StringVar(value="0")
    frame.var_total_prix = tk.StringVar(value="0,00 EUR")

    ttk.Label(
        summary_frame,
        text="Total activites:",
        font=FONTS["body_bold"]
    ).grid(row=0, column=0, padx=5)

    ttk.Label(
        summary_frame,
        textvariable=frame.var_total_activities,
        font=FONTS["body"]
    ).grid(row=0, column=1, sticky="w", padx=5)

    ttk.Label(
        summary_frame,
        text="Cout total:",
        font=FONTS["body_bold"]
    ).grid(row=0, column=2, padx=5)

    ttk.Label(
        summary_frame,
        textvariable=frame.var_total_prix,
        font=FONTS["body"],
        foreground=COLORS["primary"]
    ).grid(row=0, column=3, sticky="w", padx=5)

    # ============================================
    # ATTACHER LA METHODE REFRESH AU FRAME
    # ============================================

    frame.refresh = lambda: refresh_activities(frame)

    # Charger les donnees initiales
    frame.refresh()

    return frame
