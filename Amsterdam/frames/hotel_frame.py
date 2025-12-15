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
from typing import Any, Dict

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, FONTS, format_date


class HotelFrame(ttk.Frame):
    """
    Frame d'affichage des informations de l'hotel.
    
    Ce frame utilise le gestionnaire PACK pour empiler
    les differentes sections d'informations verticalement.
    
    Attributes:
        data_manager: Reference au gestionnaire de donnees
    """
    
    def __init__(self, parent: tk.Widget, data_manager: Any) -> None:
        """
        Initialise le frame de l'hotel.
        
        Args:
            parent: Le widget parent (Notebook)
            data_manager: Reference au gestionnaire de donnees
        """
        super().__init__(parent)
        
        self.data_manager = data_manager
        
        # Variables du formulaire
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
        self.var_adresse = tk.StringVar()
        self.var_telephone = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_site_web = tk.StringVar()
        self.var_date_checkin = tk.StringVar()
        self.var_heure_checkin = tk.StringVar()
        self.var_date_checkout = tk.StringVar()
        self.var_heure_checkout = tk.StringVar()
        self.var_numero_reservation = tk.StringVar()
        self.var_nombre_chambres = tk.StringVar()
        self.var_type_chambre = tk.StringVar()
        self.var_petit_dejeuner = tk.BooleanVar()
        self.var_wifi = tk.BooleanVar()
        self.var_notes = tk.StringVar()
    
    def _create_widgets(self) -> None:
        """
        Cree tous les widgets du frame.
        
        Utilise PACK pour organiser les elements verticalement.
        """
        # ============================================
        # SCROLLABLE CONTAINER (utilise PACK)
        # ============================================
        
        # Canvas pour le scroll
        canvas = tk.Canvas(self, bg=COLORS["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        
        # Frame scrollable
        self.scrollable_frame = ttk.Frame(canvas)
        
        # Configurer le scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
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
        
        header_frame = tk.Frame(self.scrollable_frame, bg=COLORS["primary"], pady=20)
        header_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        tk.Label(
            header_frame,
            text="🏨",
            font=("Segoe UI Emoji", 48),
            bg=COLORS["primary"]
        ).pack()
        
        tk.Label(
            header_frame,
            text="Informations Hébergement",
            font=FONTS["title"],
            fg=COLORS["text_light"],
            bg=COLORS["primary"]
        ).pack()
        
        # ============================================
        # SECTION: INFORMATIONS GENERALES (utilise PACK)
        # ============================================
        
        general_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="📋 Informations générales",
            padding=15
        )
        general_frame.pack(fill="x", padx=20, pady=10)
        
        # Nom de l'hotel
        row1 = ttk.Frame(general_frame)
        row1.pack(fill="x", pady=5)
        
        ttk.Label(row1, text="Nom de l'hôtel:", width=20).pack(side="left")
        ttk.Entry(row1, textvariable=self.var_nom, width=50).pack(side="left", fill="x", expand=True)
        
        # Adresse
        row2 = ttk.Frame(general_frame)
        row2.pack(fill="x", pady=5)
        
        ttk.Label(row2, text="Adresse:", width=20).pack(side="left")
        ttk.Entry(row2, textvariable=self.var_adresse, width=50).pack(side="left", fill="x", expand=True)
        
        # Telephone
        row3 = ttk.Frame(general_frame)
        row3.pack(fill="x", pady=5)
        
        ttk.Label(row3, text="Téléphone:", width=20).pack(side="left")
        ttk.Entry(row3, textvariable=self.var_telephone, width=30).pack(side="left")
        
        # Email
        row4 = ttk.Frame(general_frame)
        row4.pack(fill="x", pady=5)
        
        ttk.Label(row4, text="Email:", width=20).pack(side="left")
        ttk.Entry(row4, textvariable=self.var_email, width=40).pack(side="left")
        
        # Site web
        row5 = ttk.Frame(general_frame)
        row5.pack(fill="x", pady=5)
        
        ttk.Label(row5, text="Site web:", width=20).pack(side="left")
        ttk.Entry(row5, textvariable=self.var_site_web, width=40).pack(side="left")
        
        # ============================================
        # SECTION: DATES (utilise PACK)
        # ============================================
        
        dates_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="📅 Dates de séjour",
            padding=15
        )
        dates_frame.pack(fill="x", padx=20, pady=10)
        
        # Check-in
        checkin_row = ttk.Frame(dates_frame)
        checkin_row.pack(fill="x", pady=5)
        
        ttk.Label(checkin_row, text="Check-in:", width=20).pack(side="left")
        ttk.Entry(checkin_row, textvariable=self.var_date_checkin, width=15).pack(side="left", padx=5)
        ttk.Label(checkin_row, text="à").pack(side="left", padx=5)
        ttk.Entry(checkin_row, textvariable=self.var_heure_checkin, width=10).pack(side="left")
        ttk.Label(checkin_row, text="(AAAA-MM-JJ)", font=FONTS["small"]).pack(side="left", padx=10)
        
        # Check-out
        checkout_row = ttk.Frame(dates_frame)
        checkout_row.pack(fill="x", pady=5)
        
        ttk.Label(checkout_row, text="Check-out:", width=20).pack(side="left")
        ttk.Entry(checkout_row, textvariable=self.var_date_checkout, width=15).pack(side="left", padx=5)
        ttk.Label(checkout_row, text="à").pack(side="left", padx=5)
        ttk.Entry(checkout_row, textvariable=self.var_heure_checkout, width=10).pack(side="left")
        
        # ============================================
        # SECTION: RESERVATION (utilise PACK)
        # ============================================
        
        resa_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="🔖 Réservation",
            padding=15
        )
        resa_frame.pack(fill="x", padx=20, pady=10)
        
        # Numero de reservation
        resa_row1 = ttk.Frame(resa_frame)
        resa_row1.pack(fill="x", pady=5)
        
        ttk.Label(resa_row1, text="N° de réservation:", width=20).pack(side="left")
        ttk.Entry(resa_row1, textvariable=self.var_numero_reservation, width=25).pack(side="left")
        
        # Chambres
        resa_row2 = ttk.Frame(resa_frame)
        resa_row2.pack(fill="x", pady=5)
        
        ttk.Label(resa_row2, text="Nombre de chambres:", width=20).pack(side="left")
        ttk.Entry(resa_row2, textvariable=self.var_nombre_chambres, width=10).pack(side="left", padx=5)
        
        ttk.Label(resa_row2, text="Type:", width=10).pack(side="left", padx=10)
        type_combo = ttk.Combobox(
            resa_row2,
            textvariable=self.var_type_chambre,
            values=["Simple", "Double", "Twin", "Triple", "Suite"],
            width=15
        )
        type_combo.pack(side="left")
        
        # ============================================
        # SECTION: SERVICES (utilise PACK)
        # ============================================
        
        services_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="✨ Services inclus",
            padding=15
        )
        services_frame.pack(fill="x", padx=20, pady=10)
        
        services_row = ttk.Frame(services_frame)
        services_row.pack(fill="x", pady=5)
        
        ttk.Checkbutton(
            services_row,
            text="🍳 Petit-déjeuner inclus",
            variable=self.var_petit_dejeuner
        ).pack(side="left", padx=20)
        
        ttk.Checkbutton(
            services_row,
            text="📶 WiFi gratuit",
            variable=self.var_wifi
        ).pack(side="left", padx=20)
        
        # ============================================
        # SECTION: NOTES (utilise PACK)
        # ============================================
        
        notes_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="📝 Notes",
            padding=15
        )
        notes_frame.pack(fill="x", padx=20, pady=10)
        
        self.notes_text = tk.Text(
            notes_frame,
            height=4,
            font=FONTS["body"],
            wrap="word"
        )
        self.notes_text.pack(fill="x", pady=5)
        
        # ============================================
        # BOUTONS (utilise PACK)
        # ============================================
        
        btn_frame = ttk.Frame(self.scrollable_frame)
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        ttk.Button(
            btn_frame,
            text="💾 Sauvegarder les modifications",
            command=self._save_hotel
        ).pack(side="left", padx=10)
        
        ttk.Button(
            btn_frame,
            text="🔄 Réinitialiser",
            command=self.refresh
        ).pack(side="left", padx=10)
        
        # ============================================
        # CARTE INFO RAPIDE (utilise PACK)
        # ============================================
        
        quick_frame = tk.Frame(
            self.scrollable_frame,
            bg="white",
            padx=20,
            pady=15,
            relief="solid",
            bd=1
        )
        quick_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            quick_frame,
            text="📍 Accès rapide",
            font=FONTS["heading"],
            bg="white"
        ).pack(anchor="w")
        
        self.quick_info = tk.Label(
            quick_frame,
            text="",
            font=FONTS["body"],
            bg="white",
            justify="left"
        )
        self.quick_info.pack(anchor="w", pady=10)
    
    def _save_hotel(self) -> None:
        """
        Sauvegarde les informations de l'hotel.
        """
        # Recuperer les notes
        notes = self.notes_text.get("1.0", "end-1c")
        
        # Valider le nombre de chambres
        try:
            nb_chambres = int(self.var_nombre_chambres.get() or 0)
        except ValueError:
            nb_chambres = 0
        
        # Creer l'objet hotel
        hotel = {
            "nom": self.var_nom.get(),
            "adresse": self.var_adresse.get(),
            "telephone": self.var_telephone.get(),
            "email": self.var_email.get(),
            "site_web": self.var_site_web.get(),
            "date_checkin": self.var_date_checkin.get(),
            "heure_checkin": self.var_heure_checkin.get(),
            "date_checkout": self.var_date_checkout.get(),
            "heure_checkout": self.var_heure_checkout.get(),
            "numero_reservation": self.var_numero_reservation.get(),
            "nombre_chambres": nb_chambres,
            "type_chambre": self.var_type_chambre.get(),
            "petit_dejeuner": self.var_petit_dejeuner.get(),
            "wifi": self.var_wifi.get(),
            "notes": notes
        }
        
        self.data_manager.update_hotel(hotel)
        
        # Mettre a jour l'affichage rapide
        self._update_quick_info()
        
        messagebox.showinfo("Succès", "Informations de l'hôtel sauvegardées !")
    
    def _update_quick_info(self) -> None:
        """
        Met a jour l'affichage des informations rapides.
        """
        hotel = self.data_manager.get_hotel()
        
        info_text = f"""
🏨 {hotel.get('nom', 'Non défini')}
📍 {hotel.get('adresse', 'Non définie')}
📞 {hotel.get('telephone', 'Non défini')}
📧 {hotel.get('email', 'Non défini')}

📅 Check-in: {format_date(hotel.get('date_checkin', ''))} à {hotel.get('heure_checkin', '')}
📅 Check-out: {format_date(hotel.get('date_checkout', ''))} à {hotel.get('heure_checkout', '')}

🔖 Réservation: {hotel.get('numero_reservation', 'Non défini')}
        """
        
        self.quick_info.configure(text=info_text.strip())
    
    def refresh(self) -> None:
        """
        Rafraichit les donnees depuis le data manager.
        """
        hotel = self.data_manager.get_hotel()
        
        # Remplir les champs
        self.var_nom.set(hotel.get('nom', ''))
        self.var_adresse.set(hotel.get('adresse', ''))
        self.var_telephone.set(hotel.get('telephone', ''))
        self.var_email.set(hotel.get('email', ''))
        self.var_site_web.set(hotel.get('site_web', ''))
        self.var_date_checkin.set(hotel.get('date_checkin', ''))
        self.var_heure_checkin.set(hotel.get('heure_checkin', ''))
        self.var_date_checkout.set(hotel.get('date_checkout', ''))
        self.var_heure_checkout.set(hotel.get('heure_checkout', ''))
        self.var_numero_reservation.set(hotel.get('numero_reservation', ''))
        self.var_nombre_chambres.set(str(hotel.get('nombre_chambres', '')))
        self.var_type_chambre.set(hotel.get('type_chambre', ''))
        self.var_petit_dejeuner.set(hotel.get('petit_dejeuner', False))
        self.var_wifi.set(hotel.get('wifi', False))
        
        # Notes
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", hotel.get('notes', ''))
        
        # Info rapide
        self._update_quick_info()

