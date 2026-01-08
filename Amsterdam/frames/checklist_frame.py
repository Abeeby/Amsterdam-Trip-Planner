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

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, CHECKLIST_CATEGORIES


# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def get_category_icon(category):
    """
    Retourne l'emoji correspondant a la categorie.

    Args:
        category: Le nom de la categorie

    Returns:
        L'emoji correspondant
    """
    icons = {
        "Documents": "📄",
        "Vetements": "👕",
        "Electronique": "📱",
        "Hygiene": "🧴",
        "Medicaments": "💊",
        "Autre": "📦"
    }
    return icons.get(category, "📦")


# ============================================
# FONCTIONS DE GESTION DES ITEMS
# ============================================

def add_item(frame):
    """
    Ajoute un nouvel item a la checklist.

    Args:
        frame: Le frame contenant les variables
    """
    item_text = frame.var_item.get().strip()
    categorie = frame.var_categorie.get()

    if not item_text:
        messagebox.showwarning("Attention", "Veuillez entrer un item.")
        return

    if not categorie:
        messagebox.showwarning("Attention", "Veuillez selectionner une categorie.")
        return

    item = {
        "item": item_text,
        "categorie": categorie,
        "checked": False
    }

    frame.data_manager.add_checklist_item(item)

    # Vider le champ
    frame.var_item.set("")

    # Rafraichir
    refresh_checklist(frame)


def toggle_item(frame, item_id):
    """
    Inverse l'etat d'un item.

    Args:
        frame: Le frame contenant le data_manager
        item_id: L'ID de l'item a inverser
    """
    frame.data_manager.toggle_checklist_item(item_id)
    update_progress(frame)


def delete_item(frame, item_id):
    """
    Supprime un item.

    Args:
        frame: Le frame contenant le data_manager
        item_id: L'ID de l'item a supprimer
    """
    frame.data_manager.delete_checklist_item(item_id)
    refresh_checklist(frame)


def check_all(frame):
    """
    Coche tous les items.

    Args:
        frame: Le frame contenant le data_manager
    """
    checklist = frame.data_manager.get_checklist()

    for item in checklist:
        if not item.get('checked', False):
            frame.data_manager.toggle_checklist_item(item['id'])

    refresh_checklist(frame)


def uncheck_all(frame):
    """
    Decoche tous les items.

    Args:
        frame: Le frame contenant le data_manager
    """
    checklist = frame.data_manager.get_checklist()

    for item in checklist:
        if item.get('checked', False):
            frame.data_manager.toggle_checklist_item(item['id'])

    refresh_checklist(frame)


def delete_checked(frame):
    """
    Supprime tous les items coches.

    Args:
        frame: Le frame contenant le data_manager
    """
    checklist = frame.data_manager.get_checklist()
    checked_items = [item for item in checklist if item.get('checked', False)]

    if not checked_items:
        messagebox.showinfo("Info", "Aucun item coche a supprimer.")
        return

    confirm = messagebox.askyesno(
        "Confirmation",
        "Supprimer {} item(s) coche(s) ?".format(len(checked_items))
    )

    if confirm:
        for item in checked_items:
            frame.data_manager.delete_checklist_item(item['id'])

        refresh_checklist(frame)


# ============================================
# FONCTIONS DE MISE A JOUR
# ============================================

def update_progress(frame):
    """
    Met a jour la barre de progression.

    Args:
        frame: Le frame contenant les variables de progression
    """
    checked, total, percentage = frame.data_manager.get_checklist_progress()

    frame.var_progress.set("{}%".format(percentage))
    frame.var_progress_text.set("{}/{} items coches".format(checked, total))
    frame.progressbar["value"] = percentage

    # Mettre a jour les checkbuttons
    checklist = frame.data_manager.get_checklist()
    for item in checklist:
        item_id = item.get('id')
        if item_id in frame.checkbuttons:
            frame.checkbuttons[item_id].set(item.get('checked', False))


def refresh_checklist(frame):
    """
    Rafraichit la liste complete.

    Args:
        frame: Le frame contenant le data_manager et les widgets
    """
    # Nettoyer
    for widget in frame.items_frame.winfo_children():
        widget.destroy()

    frame.checkbuttons.clear()

    # Recuperer les items
    checklist = frame.data_manager.get_checklist()

    # Organiser par categorie
    by_category = {}
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
        icon = get_category_icon(categorie)
        cat_label = tk.Label(
            frame.items_frame,
            text="{} {}".format(icon, categorie),
            font=FONTS["heading"],
            bg="white",
            fg=COLORS["secondary"]
        )
        cat_label.grid(row=row, column=0, columnspan=3, sticky="w", padx=10, pady=(15, 5))
        row += 1

        # Separateur
        sep = ttk.Separator(frame.items_frame, orient="horizontal")
        sep.grid(row=row, column=0, columnspan=3, sticky="ew", padx=10)
        row += 1

        # Items de cette categorie
        for item in items:
            item_id = item.get('id')

            # Variable pour la checkbox
            var = tk.BooleanVar(value=item.get('checked', False))
            frame.checkbuttons[item_id] = var

            # Checkbox avec le texte
            cb = tk.Checkbutton(
                frame.items_frame,
                text=item.get('item', ''),
                variable=var,
                font=FONTS["body"],
                bg="white",
                activebackground="white",
                command=lambda iid=item_id: toggle_item(frame, iid)
            )
            cb.grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=2)

            # Bouton supprimer
            del_btn = tk.Button(
                frame.items_frame,
                text="X",
                font=("Segoe UI", 8),
                bg="white",
                relief="flat",
                cursor="hand2",
                command=lambda iid=item_id: delete_item(frame, iid)
            )
            del_btn.grid(row=row, column=2, sticky="e", padx=10)

            row += 1

    # Si aucun item
    if not checklist:
        tk.Label(
            frame.items_frame,
            text="Aucun item dans la checklist.\nAjoutez des affaires a emporter !",
            font=FONTS["body"],
            bg="white",
            fg="#666666",
            justify="center"
        ).grid(row=0, column=0, pady=50, padx=50)

    # Mettre a jour la progression
    update_progress(frame)


# ============================================
# FONCTION PRINCIPALE DE CREATION DU FRAME
# ============================================

def ChecklistFrame(parent, data_manager):
    """
    Cree et retourne le frame de la checklist.

    Ce frame utilise une combinaison de PACK et GRID:
    - PACK pour l'organisation generale verticale
    - GRID pour le formulaire et les boutons

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
    frame.checkbuttons = {}

    # Variables
    frame.var_item = tk.StringVar()
    frame.var_categorie = tk.StringVar()
    frame.var_progress = tk.StringVar(value="0%")
    frame.var_progress_text = tk.StringVar(value="0/0 items coches")

    # ============================================
    # EN-TETE (utilise PACK)
    # ============================================

    header = tk.Frame(frame, bg=COLORS["success"], pady=15)
    header.pack(fill="x", padx=10, pady=(10, 0))

    tk.Label(
        header,
        text="Checklist - Affaires a emporter",
        font=FONTS["title"],
        fg=COLORS["text_light"],
        bg=COLORS["success"]
    ).pack()

    # ============================================
    # BARRE DE PROGRESSION (utilise PACK)
    # ============================================

    progress_frame = ttk.Frame(frame)
    progress_frame.pack(fill="x", padx=20, pady=15)

    # Label de progression
    ttk.Label(
        progress_frame,
        textvariable=frame.var_progress_text,
        font=FONTS["body_bold"]
    ).pack(side="left")

    # Pourcentage
    ttk.Label(
        progress_frame,
        textvariable=frame.var_progress,
        font=("Segoe UI", 18, "bold"),
        foreground=COLORS["success"]
    ).pack(side="right")

    # Barre de progression
    frame.progressbar = ttk.Progressbar(
        progress_frame,
        length=400,
        maximum=100,
        mode="determinate"
    )
    frame.progressbar.pack(side="right", padx=20)

    # ============================================
    # FORMULAIRE D'AJOUT (utilise GRID dans un frame PACK)
    # ============================================

    form_frame = ttk.LabelFrame(frame, text="Ajouter un item", padding=15)
    form_frame.pack(fill="x", padx=20, pady=10)

    # Utiliser GRID pour le formulaire
    form_frame.columnconfigure(1, weight=1)

    # Item
    ttk.Label(form_frame, text="Item:").grid(
        row=0, column=0, sticky="e", padx=5, pady=5
    )
    ttk.Entry(form_frame, textvariable=frame.var_item, width=50).grid(
        row=0, column=1, sticky="ew", padx=5, pady=5
    )

    # Categorie
    ttk.Label(form_frame, text="Categorie:").grid(
        row=0, column=2, sticky="e", padx=5, pady=5
    )
    ttk.Combobox(
        form_frame,
        textvariable=frame.var_categorie,
        values=CHECKLIST_CATEGORIES,
        width=15,
        state="readonly"
    ).grid(row=0, column=3, sticky="w", padx=5, pady=5)

    # Boutons (utilise GRID)
    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=1, column=0, columnspan=4, pady=10)

    ttk.Button(
        btn_frame,
        text="Ajouter",
        command=lambda: add_item(frame)
    ).grid(row=0, column=0, padx=5)

    ttk.Button(
        btn_frame,
        text="Tout cocher",
        command=lambda: check_all(frame)
    ).grid(row=0, column=1, padx=5)

    ttk.Button(
        btn_frame,
        text="Tout decocher",
        command=lambda: uncheck_all(frame)
    ).grid(row=0, column=2, padx=5)

    ttk.Button(
        btn_frame,
        text="Supprimer coches",
        command=lambda: delete_checked(frame)
    ).grid(row=0, column=3, padx=5)

    # ============================================
    # LISTE DES ITEMS (utilise PACK)
    # ============================================

    list_frame = ttk.Frame(frame)
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Canvas pour le scroll
    canvas = tk.Canvas(list_frame, bg="white", highlightthickness=1, highlightbackground=COLORS["border"])
    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)

    frame.items_frame = ttk.Frame(canvas)

    # Configurer le scroll
    frame.items_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame.items_frame, anchor="nw")
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

    legend_frame = ttk.LabelFrame(frame, text="Categories", padding=10)
    legend_frame.pack(fill="x", padx=20, pady=10)

    # Utiliser GRID pour les categories
    for i, cat in enumerate(CHECKLIST_CATEGORIES):
        col = i % 3
        row = i // 3

        icon = get_category_icon(cat)
        ttk.Label(
            legend_frame,
            text="{} {}".format(icon, cat),
            font=FONTS["body"]
        ).grid(row=row, column=col, sticky="w", padx=15, pady=2)

    # ============================================
    # ATTACHER LA METHODE REFRESH AU FRAME
    # ============================================

    frame.refresh = lambda: refresh_checklist(frame)

    # Charger les donnees initiales
    frame.refresh()

    return frame
