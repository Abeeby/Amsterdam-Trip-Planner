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

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, BUDGET_CATEGORIES, format_currency


# ============================================
# FONCTIONS DE GESTION DU BUDGET
# ============================================

def save_budget_prevu(frame):
    """
    Sauvegarde le budget prevu.

    Args:
        frame: Le frame contenant les variables
    """
    try:
        montant = float(frame.var_budget_prevu.get().replace(",", ".").replace(" ", "").replace("EUR", ""))
        frame.data_manager.update_budget_prevu(montant)
        refresh_budget(frame)
        messagebox.showinfo("Succes", "Budget prevu mis a jour !")
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un montant valide.")


def add_expense(frame):
    """
    Ajoute une nouvelle depense.

    Args:
        frame: Le frame contenant les variables
    """
    # Validations
    if not frame.var_categorie.get():
        messagebox.showwarning("Attention", "Veuillez selectionner une categorie.")
        return

    try:
        montant = float(frame.var_montant.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Erreur", "Le montant doit etre un nombre.")
        return

    if montant <= 0:
        messagebox.showwarning("Attention", "Le montant doit etre positif.")
        return

    # Creer la depense
    depense = {
        "date": frame.var_date.get() or "Non specifie",
        "categorie": frame.var_categorie.get(),
        "montant": montant,
        "description": frame.var_description.get().strip(),
        "participant": frame.var_participant.get() or "Groupe"
    }

    frame.data_manager.add_depense(depense)
    refresh_budget(frame)
    clear_form(frame)

    messagebox.showinfo("Succes", "Depense ajoutee !")


def delete_expense(frame):
    """
    Supprime la depense selectionnee.

    Args:
        frame: Le frame contenant les variables
    """
    if not frame.selected_id:
        messagebox.showwarning("Attention", "Veuillez selectionner une depense.")
        return

    confirm = messagebox.askyesno(
        "Confirmation",
        "Supprimer cette depense ?"
    )

    if confirm:
        frame.data_manager.delete_depense(frame.selected_id)
        refresh_budget(frame)
        clear_form(frame)


def clear_form(frame):
    """
    Efface le formulaire.

    Args:
        frame: Le frame contenant les variables
    """
    frame.var_date.set("")
    frame.var_categorie.set("")
    frame.var_montant.set("")
    frame.var_description.set("")
    frame.var_participant.set("")
    frame.selected_id = None


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


# ============================================
# FONCTIONS D'AFFICHAGE
# ============================================

def update_categories_display(frame):
    """
    Met a jour l'affichage des categories.

    Args:
        frame: Le frame contenant le container des categories
    """
    # Nettoyer
    for widget in frame.categories_container.winfo_children():
        widget.destroy()

    # Obtenir les totaux par categorie
    totaux = frame.data_manager.get_depenses_by_category()
    total = sum(totaux.values())

    if total == 0:
        ttk.Label(
            frame.categories_container,
            text="Aucune depense enregistree",
            font=FONTS["body"]
        ).grid(row=0, column=0, pady=20)
        return

    # Creer une barre pour chaque categorie
    row = 0

    for i, cat in enumerate(BUDGET_CATEGORIES):
        montant = totaux.get(cat, 0)
        if montant > 0:
            pourcentage = (montant / total) * 100

            # Label categorie
            ttk.Label(
                frame.categories_container,
                text=f"{cat}:",
                font=FONTS["body"]
            ).grid(row=row, column=0, sticky="w", padx=5, pady=2)

            # Barre de progression
            progress = ttk.Progressbar(
                frame.categories_container,
                length=150,
                maximum=100,
                value=pourcentage
            )
            progress.grid(row=row, column=1, sticky="ew", padx=5, pady=2)

            # Montant et pourcentage
            ttk.Label(
                frame.categories_container,
                text=f"{format_currency(montant)} ({pourcentage:.1f}%)",
                font=FONTS["small"]
            ).grid(row=row, column=2, sticky="w", padx=5, pady=2)

            row += 1


def update_participants_list(frame):
    """
    Met a jour la liste des participants dans le combobox.

    Args:
        frame: Le frame contenant le combobox
    """
    participants = frame.data_manager.get_participants()
    noms = ["Groupe"] + [f"{p.get('prenom', '')} {p.get('nom', '')}" for p in participants]
    frame.participant_combo["values"] = noms


# ============================================
# FONCTION DE RAFRAICHISSEMENT
# ============================================

def refresh_budget(frame):
    """
    Rafraichit toutes les donnees.

    Args:
        frame: Le frame contenant toutes les variables
    """
    # Budget
    budget = frame.data_manager.get_budget()
    budget_prevu = budget.get('budget_prevu', 0)
    frame.var_budget_prevu.set(str(budget_prevu))

    # Total depenses
    total = frame.data_manager.get_total_depenses()
    frame.var_total_depenses.set(format_currency(total))

    # Restant
    restant = budget_prevu - total
    frame.var_budget_restant.set(format_currency(restant))

    # Couleur selon le restant
    if restant < 0:
        frame.label_restant.configure(foreground=COLORS["danger"])
    elif restant < budget_prevu * 0.2:
        frame.label_restant.configure(foreground=COLORS["warning"])
    else:
        frame.label_restant.configure(foreground=COLORS["success"])

    # Vider le tableau
    for item in frame.tree.get_children():
        frame.tree.delete(item)

    # Remplir le tableau
    depenses = frame.data_manager.get_depenses()
    for dep in sorted(depenses, key=lambda x: x.get('date', ''), reverse=True):
        frame.tree.insert(
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
    update_categories_display(frame)

    # Mettre a jour les participants
    update_participants_list(frame)


# ============================================
# FONCTION PRINCIPALE DE CREATION DU FRAME
# ============================================

def BudgetFrame(parent, data_manager):
    """
    Cree et retourne le frame du budget.

    Ce frame utilise le gestionnaire GRID pour organiser
    le formulaire de depenses et l'affichage du budget.

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
    frame.var_date = tk.StringVar()
    frame.var_categorie = tk.StringVar()
    frame.var_montant = tk.StringVar()
    frame.var_description = tk.StringVar()
    frame.var_participant = tk.StringVar()

    # Variables du budget
    frame.var_budget_prevu = tk.StringVar()
    frame.var_total_depenses = tk.StringVar(value="0,00 EUR")
    frame.var_budget_restant = tk.StringVar(value="0,00 EUR")

    # Configuration du grid principal
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)
    frame.rowconfigure(2, weight=1)

    # ============================================
    # RESUME DU BUDGET (utilise GRID)
    # ============================================

    summary_frame = ttk.LabelFrame(frame, text="Resume du budget", padding=15)
    summary_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    # Configuration du grid du resume
    summary_frame.columnconfigure(1, weight=1)
    summary_frame.columnconfigure(3, weight=1)
    summary_frame.columnconfigure(5, weight=1)

    # Budget prevu
    ttk.Label(
        summary_frame,
        text="Budget prevu:",
        font=FONTS["body_bold"]
    ).grid(row=0, column=0, sticky="e", padx=5, pady=5)

    budget_entry = ttk.Entry(
        summary_frame,
        textvariable=frame.var_budget_prevu,
        width=15,
        font=FONTS["body"]
    )
    budget_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    ttk.Button(
        summary_frame,
        text="OK",
        width=3,
        command=lambda: save_budget_prevu(frame)
    ).grid(row=0, column=2, padx=2)

    # Total depenses
    ttk.Label(
        summary_frame,
        text="Total depense:",
        font=FONTS["body_bold"]
    ).grid(row=0, column=3, sticky="e", padx=5, pady=5)

    ttk.Label(
        summary_frame,
        textvariable=frame.var_total_depenses,
        font=("Segoe UI", 14, "bold"),
        foreground=COLORS["danger"]
    ).grid(row=0, column=4, sticky="w", padx=5, pady=5)

    # Budget restant
    ttk.Label(
        summary_frame,
        text="Reste:",
        font=FONTS["body_bold"]
    ).grid(row=0, column=5, sticky="e", padx=5, pady=5)

    frame.label_restant = ttk.Label(
        summary_frame,
        textvariable=frame.var_budget_restant,
        font=("Segoe UI", 14, "bold"),
        foreground=COLORS["success"]
    )
    frame.label_restant.grid(row=0, column=6, sticky="w", padx=5, pady=5)

    # ============================================
    # FORMULAIRE D'AJOUT DE DEPENSE (utilise GRID)
    # ============================================

    form_frame = ttk.LabelFrame(frame, text="Ajouter une depense", padding=15)
    form_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    # Configuration du grid du formulaire
    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(3, weight=1)
    form_frame.columnconfigure(5, weight=1)

    # Ligne 1: Date, Categorie
    ttk.Label(form_frame, text="Date:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_date, width=15).grid(
        row=0, column=1, sticky="w", padx=5, pady=5
    )

    ttk.Label(form_frame, text="Categorie:").grid(
        row=0, column=2, sticky="e", padx=5, pady=5
    )
    categorie_combo = ttk.Combobox(
        form_frame,
        textvariable=frame.var_categorie,
        values=BUDGET_CATEGORIES,
        state="readonly",
        width=15
    )
    categorie_combo.grid(row=0, column=3, sticky="w", padx=5, pady=5)

    ttk.Label(form_frame, text="Montant (EUR):").grid(
        row=0, column=4, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_montant, width=12).grid(
        row=0, column=5, sticky="w", padx=5, pady=5
    )

    # Ligne 2: Description, Participant
    ttk.Label(form_frame, text="Description:").grid(
        row=1, column=0, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_description, width=40).grid(
        row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5
    )

    ttk.Label(form_frame, text="Paye par:").grid(
        row=1, column=4, sticky="e", padx=5, pady=5
    )
    frame.participant_combo = ttk.Combobox(
        form_frame,
        textvariable=frame.var_participant,
        values=["Groupe"],
        width=15
    )
    frame.participant_combo.grid(row=1, column=5, sticky="w", padx=5, pady=5)

    # Ligne 3: Boutons
    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=2, column=0, columnspan=6, pady=10)

    ttk.Button(
        btn_frame,
        text="Ajouter",
        command=lambda: add_expense(frame)
    ).grid(row=0, column=0, padx=5)

    ttk.Button(
        btn_frame,
        text="Supprimer",
        command=lambda: delete_expense(frame)
    ).grid(row=0, column=1, padx=5)

    ttk.Button(
        btn_frame,
        text="Effacer",
        command=lambda: clear_form(frame)
    ).grid(row=0, column=2, padx=5)

    # ============================================
    # TABLEAU DES DEPENSES (utilise GRID)
    # ============================================

    table_frame = ttk.LabelFrame(frame, text="Liste des depenses", padding=10)
    table_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    # Colonnes du Treeview
    columns = ("date", "categorie", "montant", "description", "participant")

    frame.tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    # En-tetes
    frame.tree.heading("date", text="Date")
    frame.tree.heading("categorie", text="Categorie")
    frame.tree.heading("montant", text="Montant")
    frame.tree.heading("description", text="Description")
    frame.tree.heading("participant", text="Paye par")

    # Largeurs
    frame.tree.column("date", width=100, anchor="center")
    frame.tree.column("categorie", width=100)
    frame.tree.column("montant", width=100, anchor="e")
    frame.tree.column("description", width=200)
    frame.tree.column("participant", width=100)

    frame.tree.grid(row=0, column=0, sticky="nsew")

    # Scrollbar
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=frame.tree.yview
    )
    scrollbar.grid(row=0, column=1, sticky="ns")
    frame.tree.configure(yscrollcommand=scrollbar.set)

    # Selection
    frame.tree.bind("<<TreeviewSelect>>", lambda e: on_select(frame, e))

    # ============================================
    # REPARTITION PAR CATEGORIE (utilise GRID)
    # ============================================

    cat_frame = ttk.LabelFrame(frame, text="Repartition par categorie", padding=10)
    cat_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

    cat_frame.columnconfigure(0, weight=1)
    cat_frame.rowconfigure(0, weight=1)

    # Frame pour les barres de progression
    frame.categories_container = ttk.Frame(cat_frame)
    frame.categories_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    frame.categories_container.columnconfigure(1, weight=1)

    # ============================================
    # ATTACHER LA METHODE REFRESH AU FRAME
    # ============================================

    frame.refresh = lambda: refresh_budget(frame)

    # Charger les donnees initiales
    frame.refresh()

    return frame
