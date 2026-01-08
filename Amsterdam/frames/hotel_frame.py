"""
hotel_frame.py - Informations sur l'hebergement pour le voyage a Amsterdam.

Ce module affiche et permet de modifier les informations de l'hotel:
- Nom, adresse, contact
- Dates de check-in/check-out
- Numero de reservation
- Services inclus

IMPORTANT: Ce frame utilise le gestionnaire de layout PACK
pour empiler les widgets verticalement.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, format_date


# ============================================
# FONCTIONS DE GESTION DE L'HOTEL
# ============================================

def save_hotel(frame):
    """
    Sauvegarde les informations de l'hotel.

    Args:
        frame: Le frame contenant les variables
    """
    # Recuperer les notes
    notes = frame.notes_text.get("1.0", "end-1c")

    # Valider le nombre de chambres
    try:
        nb_chambres = int(frame.var_nombre_chambres.get() or 0)
    except ValueError:
        nb_chambres = 0

    # Creer l'objet hotel
    hotel = {
        "nom": frame.var_nom.get(),
        "adresse": frame.var_adresse.get(),
        "telephone": frame.var_telephone.get(),
        "email": frame.var_email.get(),
        "site_web": frame.var_site_web.get(),
        "date_checkin": frame.var_date_checkin.get(),
        "heure_checkin": frame.var_heure_checkin.get(),
        "date_checkout": frame.var_date_checkout.get(),
        "heure_checkout": frame.var_heure_checkout.get(),
        "numero_reservation": frame.var_numero_reservation.get(),
        "nombre_chambres": nb_chambres,
        "type_chambre": frame.var_type_chambre.get(),
        "petit_dejeuner": frame.var_petit_dejeuner.get(),
        "wifi": frame.var_wifi.get(),
        "notes": notes
    }

    frame.data_manager.update_hotel(hotel)

    # Mettre a jour l'affichage rapide
    update_quick_info(frame)

    messagebox.showinfo("Succes", "Informations de l'hotel sauvegardees !")


def update_quick_info(frame):
    """
    Met a jour l'affichage des informations rapides.

    Args:
        frame: Le frame contenant le label quick_info
    """
    hotel = frame.data_manager.get_hotel()

    info_text = """
Hotel: {nom}
Adresse: {adresse}
Telephone: {telephone}
Email: {email}

Check-in: {checkin_date} a {checkin_heure}
Check-out: {checkout_date} a {checkout_heure}

Reservation: {reservation}
    """.format(
        nom=hotel.get('nom', 'Non defini'),
        adresse=hotel.get('adresse', 'Non definie'),
        telephone=hotel.get('telephone', 'Non defini'),
        email=hotel.get('email', 'Non defini'),
        checkin_date=format_date(hotel.get('date_checkin', '')),
        checkin_heure=hotel.get('heure_checkin', ''),
        checkout_date=format_date(hotel.get('date_checkout', '')),
        checkout_heure=hotel.get('heure_checkout', ''),
        reservation=hotel.get('numero_reservation', 'Non defini')
    )

    frame.quick_info.configure(text=info_text.strip())


def refresh_hotel(frame):
    """
    Rafraichit les donnees depuis le data manager.

    Args:
        frame: Le frame contenant les variables
    """
    hotel = frame.data_manager.get_hotel()

    # Remplir les champs
    frame.var_nom.set(hotel.get('nom', ''))
    frame.var_adresse.set(hotel.get('adresse', ''))
    frame.var_telephone.set(hotel.get('telephone', ''))
    frame.var_email.set(hotel.get('email', ''))
    frame.var_site_web.set(hotel.get('site_web', ''))
    frame.var_date_checkin.set(hotel.get('date_checkin', ''))
    frame.var_heure_checkin.set(hotel.get('heure_checkin', ''))
    frame.var_date_checkout.set(hotel.get('date_checkout', ''))
    frame.var_heure_checkout.set(hotel.get('heure_checkout', ''))
    frame.var_numero_reservation.set(hotel.get('numero_reservation', ''))
    frame.var_nombre_chambres.set(str(hotel.get('nombre_chambres', '')))
    frame.var_type_chambre.set(hotel.get('type_chambre', ''))
    frame.var_petit_dejeuner.set(hotel.get('petit_dejeuner', False))
    frame.var_wifi.set(hotel.get('wifi', False))

    # Notes
    frame.notes_text.delete("1.0", "end")
    frame.notes_text.insert("1.0", hotel.get('notes', ''))

    # Info rapide
    update_quick_info(frame)


# ============================================
# FONCTION PRINCIPALE DE CREATION DU FRAME
# ============================================

def HotelFrame(parent, data_manager):
    """
    Cree et retourne le frame de l'hotel.

    Ce frame utilise le gestionnaire PACK pour empiler
    les differentes sections d'informations verticalement.

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

    # Variables du formulaire
    frame.var_nom = tk.StringVar()
    frame.var_adresse = tk.StringVar()
    frame.var_telephone = tk.StringVar()
    frame.var_email = tk.StringVar()
    frame.var_site_web = tk.StringVar()
    frame.var_date_checkin = tk.StringVar()
    frame.var_heure_checkin = tk.StringVar()
    frame.var_date_checkout = tk.StringVar()
    frame.var_heure_checkout = tk.StringVar()
    frame.var_numero_reservation = tk.StringVar()
    frame.var_nombre_chambres = tk.StringVar()
    frame.var_type_chambre = tk.StringVar()
    frame.var_petit_dejeuner = tk.BooleanVar()
    frame.var_wifi = tk.BooleanVar()
    frame.var_notes = tk.StringVar()

    # ============================================
    # SCROLLABLE CONTAINER (utilise PACK)
    # ============================================

    # Canvas pour le scroll
    canvas = tk.Canvas(frame, bg=COLORS["background"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)

    # Frame scrollable
    scrollable_frame = ttk.Frame(canvas)

    # Configurer le scroll
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # PACK le canvas et scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Scroll avec la molette
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
        int(-1 * (e.delta / 120)), "units"
    ))

    # ============================================
    # EN-TETE (utilise PACK)
    # ============================================

    header_frame = tk.Frame(scrollable_frame, bg=COLORS["primary"], pady=20)
    header_frame.pack(fill="x", padx=20, pady=(10, 20))

    tk.Label(
        header_frame,
        text="HOTEL",
        font=("Segoe UI", 48, "bold"),
        bg=COLORS["primary"],
        fg=COLORS["text_light"]
    ).pack()

    tk.Label(
        header_frame,
        text="Informations Hebergement",
        font=FONTS["title"],
        fg=COLORS["text_light"],
        bg=COLORS["primary"]
    ).pack()

    # ============================================
    # SECTION: INFORMATIONS GENERALES (utilise PACK)
    # ============================================

    general_frame = ttk.LabelFrame(
        scrollable_frame,
        text="Informations generales",
        padding=15
    )
    general_frame.pack(fill="x", padx=20, pady=10)

    # Nom de l'hotel
    row1 = ttk.Frame(general_frame)
    row1.pack(fill="x", pady=5)

    ttk.Label(row1, text="Nom de l'hotel:", width=20).pack(side="left")
    ttk.Entry(row1, textvariable=frame.var_nom, width=50).pack(side="left", fill="x", expand=True)

    # Adresse
    row2 = ttk.Frame(general_frame)
    row2.pack(fill="x", pady=5)

    ttk.Label(row2, text="Adresse:", width=20).pack(side="left")
    ttk.Entry(row2, textvariable=frame.var_adresse, width=50).pack(side="left", fill="x", expand=True)

    # Telephone
    row3 = ttk.Frame(general_frame)
    row3.pack(fill="x", pady=5)

    ttk.Label(row3, text="Telephone:", width=20).pack(side="left")
    ttk.Entry(row3, textvariable=frame.var_telephone, width=30).pack(side="left")

    # Email
    row4 = ttk.Frame(general_frame)
    row4.pack(fill="x", pady=5)

    ttk.Label(row4, text="Email:", width=20).pack(side="left")
    ttk.Entry(row4, textvariable=frame.var_email, width=40).pack(side="left")

    # Site web
    row5 = ttk.Frame(general_frame)
    row5.pack(fill="x", pady=5)

    ttk.Label(row5, text="Site web:", width=20).pack(side="left")
    ttk.Entry(row5, textvariable=frame.var_site_web, width=40).pack(side="left")

    # ============================================
    # SECTION: DATES (utilise PACK)
    # ============================================

    dates_frame = ttk.LabelFrame(
        scrollable_frame,
        text="Dates de sejour",
        padding=15
    )
    dates_frame.pack(fill="x", padx=20, pady=10)

    # Check-in
    checkin_row = ttk.Frame(dates_frame)
    checkin_row.pack(fill="x", pady=5)

    ttk.Label(checkin_row, text="Check-in:", width=20).pack(side="left")
    ttk.Entry(checkin_row, textvariable=frame.var_date_checkin, width=15).pack(side="left", padx=5)
    ttk.Label(checkin_row, text="a").pack(side="left", padx=5)
    ttk.Entry(checkin_row, textvariable=frame.var_heure_checkin, width=10).pack(side="left")
    ttk.Label(checkin_row, text="(AAAA-MM-JJ)", font=FONTS["small"]).pack(side="left", padx=10)

    # Check-out
    checkout_row = ttk.Frame(dates_frame)
    checkout_row.pack(fill="x", pady=5)

    ttk.Label(checkout_row, text="Check-out:", width=20).pack(side="left")
    ttk.Entry(checkout_row, textvariable=frame.var_date_checkout, width=15).pack(side="left", padx=5)
    ttk.Label(checkout_row, text="a").pack(side="left", padx=5)
    ttk.Entry(checkout_row, textvariable=frame.var_heure_checkout, width=10).pack(side="left")

    # ============================================
    # SECTION: RESERVATION (utilise PACK)
    # ============================================

    resa_frame = ttk.LabelFrame(
        scrollable_frame,
        text="Reservation",
        padding=15
    )
    resa_frame.pack(fill="x", padx=20, pady=10)

    # Numero de reservation
    resa_row1 = ttk.Frame(resa_frame)
    resa_row1.pack(fill="x", pady=5)

    ttk.Label(resa_row1, text="N de reservation:", width=20).pack(side="left")
    ttk.Entry(resa_row1, textvariable=frame.var_numero_reservation, width=25).pack(side="left")

    # Chambres
    resa_row2 = ttk.Frame(resa_frame)
    resa_row2.pack(fill="x", pady=5)

    ttk.Label(resa_row2, text="Nombre de chambres:", width=20).pack(side="left")
    ttk.Entry(resa_row2, textvariable=frame.var_nombre_chambres, width=10).pack(side="left", padx=5)

    ttk.Label(resa_row2, text="Type:", width=10).pack(side="left", padx=10)
    type_combo = ttk.Combobox(
        resa_row2,
        textvariable=frame.var_type_chambre,
        values=["Simple", "Double", "Twin", "Triple", "Suite"],
        width=15
    )
    type_combo.pack(side="left")

    # ============================================
    # SECTION: SERVICES (utilise PACK)
    # ============================================

    services_frame = ttk.LabelFrame(
        scrollable_frame,
        text="Services inclus",
        padding=15
    )
    services_frame.pack(fill="x", padx=20, pady=10)

    services_row = ttk.Frame(services_frame)
    services_row.pack(fill="x", pady=5)

    ttk.Checkbutton(
        services_row,
        text="Petit-dejeuner inclus",
        variable=frame.var_petit_dejeuner
    ).pack(side="left", padx=20)

    ttk.Checkbutton(
        services_row,
        text="WiFi gratuit",
        variable=frame.var_wifi
    ).pack(side="left", padx=20)

    # ============================================
    # SECTION: NOTES (utilise PACK)
    # ============================================

    notes_frame = ttk.LabelFrame(
        scrollable_frame,
        text="Notes",
        padding=15
    )
    notes_frame.pack(fill="x", padx=20, pady=10)

    frame.notes_text = tk.Text(
        notes_frame,
        height=4,
        font=FONTS["body"],
        wrap="word"
    )
    frame.notes_text.pack(fill="x", pady=5)

    # ============================================
    # BOUTONS (utilise PACK)
    # ============================================

    btn_frame = ttk.Frame(scrollable_frame)
    btn_frame.pack(fill="x", padx=20, pady=20)

    ttk.Button(
        btn_frame,
        text="Sauvegarder les modifications",
        command=lambda: save_hotel(frame)
    ).pack(side="left", padx=10)

    ttk.Button(
        btn_frame,
        text="Reinitialiser",
        command=lambda: refresh_hotel(frame)
    ).pack(side="left", padx=10)

    # ============================================
    # CARTE INFO RAPIDE (utilise PACK)
    # ============================================

    quick_frame = tk.Frame(
        scrollable_frame,
        bg="white",
        padx=20,
        pady=15,
        relief="solid",
        bd=1
    )
    quick_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(
        quick_frame,
        text="Acces rapide",
        font=FONTS["heading"],
        bg="white"
    ).pack(anchor="w")

    frame.quick_info = tk.Label(
        quick_frame,
        text="",
        font=FONTS["body"],
        bg="white",
        justify="left"
    )
    frame.quick_info.pack(anchor="w", pady=10)

    # ============================================
    # ATTACHER LA METHODE REFRESH AU FRAME
    # ============================================

    frame.refresh = lambda: refresh_hotel(frame)

    # Charger les donnees initiales
    frame.refresh()

    return frame
