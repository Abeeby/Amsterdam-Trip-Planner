"""
data_manager.py - Gestionnaire de donnees pour l'application Amsterdam Trip Planner.

Ce module gere toutes les operations de lecture et d'ecriture des donnees
dans le fichier JSON. Il assure la persistance des donnees entre les sessions.
"""

import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from config import DATA_FILE, DATA_DIR, DEFAULT_DATA


class DataManager:
    """
    Gestionnaire centralise pour la sauvegarde et le chargement des donnees.
    
    Cette classe utilise le pattern Singleton pour s'assurer qu'une seule
    instance gere les donnees dans toute l'application.
    
    Attributes:
        data (dict): Les donnees actuelles en memoire
        data_file (str): Chemin vers le fichier de donnees JSON
    """
    
    _instance: Optional['DataManager'] = None
    
    def __new__(cls) -> 'DataManager':
        """
        Implemente le pattern Singleton.
        
        Returns:
            DataManager: L'instance unique du gestionnaire
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        """
        Initialise le gestionnaire de donnees.
        
        Charge les donnees depuis le fichier JSON ou cree des donnees
        par defaut si le fichier n'existe pas.
        """
        # Evite la reinitialisation (pattern Singleton)
        if self._initialized:
            return
        
        self.data_file: str = DATA_FILE
        self.data: Dict[str, Any] = {}
        
        # S'assurer que le repertoire data existe
        self._ensure_data_directory()
        
        # Charger les donnees
        self.load_data()
        
        self._initialized = True
    
    def _ensure_data_directory(self) -> None:
        """
        Cree le repertoire data s'il n'existe pas.
        """
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"[DataManager] Répertoire créé: {DATA_DIR}")
    
    def load_data(self) -> Dict[str, Any]:
        """
        Charge les donnees depuis le fichier JSON.
        
        Si le fichier n'existe pas ou est corrompu, utilise les donnees
        par defaut definies dans config.py.
        
        Returns:
            dict: Les donnees chargees
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"[DataManager] Données chargées depuis {self.data_file}")
            else:
                # Utiliser les donnees par defaut
                self.data = DEFAULT_DATA.copy()
                self.save_data()  # Sauvegarder les donnees par defaut
                print("[DataManager] Fichier de données créé avec les valeurs par défaut")
        except json.JSONDecodeError as e:
            print(f"[DataManager] Erreur de lecture JSON: {e}")
            print("[DataManager] Utilisation des données par défaut")
            self.data = DEFAULT_DATA.copy()
            self.save_data()
        except Exception as e:
            print(f"[DataManager] Erreur inattendue: {e}")
            self.data = DEFAULT_DATA.copy()
        
        return self.data
    
    def save_data(self) -> bool:
        """
        Sauvegarde les donnees dans le fichier JSON.
        
        Returns:
            bool: True si la sauvegarde a reussi, False sinon
        """
        try:
            # Ajouter un timestamp de derniere modification
            self.data['last_modified'] = datetime.now().isoformat()
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            
            print(f"[DataManager] Données sauvegardées dans {self.data_file}")
            return True
        except Exception as e:
            print(f"[DataManager] Erreur de sauvegarde: {e}")
            return False
    
    # ============================================
    # METHODES POUR LES INFORMATIONS DU VOYAGE
    # ============================================
    
    def get_voyage_info(self) -> Dict[str, Any]:
        """
        Recupere les informations generales du voyage.
        
        Returns:
            dict: Les informations du voyage
        """
        return self.data.get('voyage_info', {})
    
    def update_voyage_info(self, info: Dict[str, Any]) -> None:
        """
        Met a jour les informations du voyage.
        
        Args:
            info: Les nouvelles informations
        """
        self.data['voyage_info'] = info
        self.save_data()
    
    # ============================================
    # METHODES POUR LES ACTIVITES
    # ============================================
    
    def get_activites(self) -> List[Dict[str, Any]]:
        """
        Recupere la liste des activites.
        
        Returns:
            list: Liste des activites
        """
        return self.data.get('activites', [])
    
    def add_activite(self, activite: Dict[str, Any]) -> int:
        """
        Ajoute une nouvelle activite.
        
        Args:
            activite: Les donnees de l'activite
            
        Returns:
            int: L'ID de la nouvelle activite
        """
        activites = self.get_activites()
        
        # Generer un nouvel ID
        new_id = max([a.get('id', 0) for a in activites], default=0) + 1
        activite['id'] = new_id
        
        activites.append(activite)
        self.data['activites'] = activites
        self.save_data()
        
        return new_id
    
    def update_activite(self, activite_id: int, activite: Dict[str, Any]) -> bool:
        """
        Met a jour une activite existante.
        
        Args:
            activite_id: L'ID de l'activite a modifier
            activite: Les nouvelles donnees
            
        Returns:
            bool: True si la mise a jour a reussi
        """
        activites = self.get_activites()
        
        for i, a in enumerate(activites):
            if a.get('id') == activite_id:
                activite['id'] = activite_id
                activites[i] = activite
                self.data['activites'] = activites
                self.save_data()
                return True
        
        return False
    
    def delete_activite(self, activite_id: int) -> bool:
        """
        Supprime une activite.
        
        Args:
            activite_id: L'ID de l'activite a supprimer
            
        Returns:
            bool: True si la suppression a reussi
        """
        activites = self.get_activites()
        initial_count = len(activites)
        
        activites = [a for a in activites if a.get('id') != activite_id]
        
        if len(activites) < initial_count:
            self.data['activites'] = activites
            self.save_data()
            return True
        
        return False
    
    # ============================================
    # METHODES POUR LE BUDGET
    # ============================================
    
    def get_budget(self) -> Dict[str, Any]:
        """
        Recupere les informations de budget.
        
        Returns:
            dict: Les donnees du budget
        """
        return self.data.get('budget', {'budget_prevu': 0, 'depenses': []})
    
    def get_depenses(self) -> List[Dict[str, Any]]:
        """
        Recupere la liste des depenses.
        
        Returns:
            list: Liste des depenses
        """
        return self.get_budget().get('depenses', [])
    
    def add_depense(self, depense: Dict[str, Any]) -> int:
        """
        Ajoute une nouvelle depense.
        
        Args:
            depense: Les donnees de la depense
            
        Returns:
            int: L'ID de la nouvelle depense
        """
        budget = self.get_budget()
        depenses = budget.get('depenses', [])
        
        # Generer un nouvel ID
        new_id = max([d.get('id', 0) for d in depenses], default=0) + 1
        depense['id'] = new_id
        
        depenses.append(depense)
        budget['depenses'] = depenses
        self.data['budget'] = budget
        self.save_data()
        
        return new_id
    
    def update_budget_prevu(self, montant: float) -> None:
        """
        Met a jour le budget prevu.
        
        Args:
            montant: Le nouveau budget prevu
        """
        budget = self.get_budget()
        budget['budget_prevu'] = montant
        self.data['budget'] = budget
        self.save_data()
    
    def delete_depense(self, depense_id: int) -> bool:
        """
        Supprime une depense.
        
        Args:
            depense_id: L'ID de la depense a supprimer
            
        Returns:
            bool: True si la suppression a reussi
        """
        budget = self.get_budget()
        depenses = budget.get('depenses', [])
        initial_count = len(depenses)
        
        depenses = [d for d in depenses if d.get('id') != depense_id]
        
        if len(depenses) < initial_count:
            budget['depenses'] = depenses
            self.data['budget'] = budget
            self.save_data()
            return True
        
        return False
    
    def get_total_depenses(self) -> float:
        """
        Calcule le total des depenses.
        
        Returns:
            float: Le total des depenses
        """
        depenses = self.get_depenses()
        return sum(d.get('montant', 0) for d in depenses)
    
    def get_depenses_by_category(self) -> Dict[str, float]:
        """
        Calcule le total des depenses par categorie.
        
        Returns:
            dict: Total par categorie
        """
        depenses = self.get_depenses()
        totaux = {}
        
        for d in depenses:
            cat = d.get('categorie', 'Autre')
            totaux[cat] = totaux.get(cat, 0) + d.get('montant', 0)
        
        return totaux
    
    # ============================================
    # METHODES POUR L'HOTEL
    # ============================================
    
    def get_hotel(self) -> Dict[str, Any]:
        """
        Recupere les informations de l'hotel.
        
        Returns:
            dict: Les donnees de l'hotel
        """
        return self.data.get('hotel', {})
    
    def update_hotel(self, hotel: Dict[str, Any]) -> None:
        """
        Met a jour les informations de l'hotel.
        
        Args:
            hotel: Les nouvelles informations
        """
        self.data['hotel'] = hotel
        self.save_data()
    
    # ============================================
    # METHODES POUR LE TRANSPORT
    # ============================================
    
    def get_transport(self) -> Dict[str, Any]:
        """
        Recupere les informations de transport.
        
        Returns:
            dict: Les donnees de transport
        """
        return self.data.get('transport', {})
    
    def update_transport(self, transport: Dict[str, Any]) -> None:
        """
        Met a jour les informations de transport.
        
        Args:
            transport: Les nouvelles informations
        """
        self.data['transport'] = transport
        self.save_data()
    
    # ============================================
    # METHODES POUR LES PARTICIPANTS
    # ============================================
    
    def get_participants(self) -> List[Dict[str, Any]]:
        """
        Recupere la liste des participants.
        
        Returns:
            list: Liste des participants
        """
        return self.data.get('participants', [])
    
    def add_participant(self, participant: Dict[str, Any]) -> int:
        """
        Ajoute un nouveau participant.
        
        Args:
            participant: Les donnees du participant
            
        Returns:
            int: L'ID du nouveau participant
        """
        participants = self.get_participants()
        
        # Generer un nouvel ID
        new_id = max([p.get('id', 0) for p in participants], default=0) + 1
        participant['id'] = new_id
        
        participants.append(participant)
        self.data['participants'] = participants
        self.save_data()
        
        return new_id
    
    def update_participant(self, participant_id: int, participant: Dict[str, Any]) -> bool:
        """
        Met a jour un participant existant.
        
        Args:
            participant_id: L'ID du participant a modifier
            participant: Les nouvelles donnees
            
        Returns:
            bool: True si la mise a jour a reussi
        """
        participants = self.get_participants()
        
        for i, p in enumerate(participants):
            if p.get('id') == participant_id:
                participant['id'] = participant_id
                participants[i] = participant
                self.data['participants'] = participants
                self.save_data()
                return True
        
        return False
    
    def delete_participant(self, participant_id: int) -> bool:
        """
        Supprime un participant.
        
        Args:
            participant_id: L'ID du participant a supprimer
            
        Returns:
            bool: True si la suppression a reussi
        """
        participants = self.get_participants()
        initial_count = len(participants)
        
        participants = [p for p in participants if p.get('id') != participant_id]
        
        if len(participants) < initial_count:
            self.data['participants'] = participants
            self.save_data()
            return True
        
        return False
    
    # ============================================
    # METHODES POUR LA CHECKLIST
    # ============================================
    
    def get_checklist(self) -> List[Dict[str, Any]]:
        """
        Recupere la checklist.
        
        Returns:
            list: Liste des items de la checklist
        """
        return self.data.get('checklist', [])
    
    def add_checklist_item(self, item: Dict[str, Any]) -> int:
        """
        Ajoute un item a la checklist.
        
        Args:
            item: Les donnees de l'item
            
        Returns:
            int: L'ID du nouvel item
        """
        checklist = self.get_checklist()
        
        # Generer un nouvel ID
        new_id = max([i.get('id', 0) for i in checklist], default=0) + 1
        item['id'] = new_id
        item['checked'] = item.get('checked', False)
        
        checklist.append(item)
        self.data['checklist'] = checklist
        self.save_data()
        
        return new_id
    
    def toggle_checklist_item(self, item_id: int) -> bool:
        """
        Inverse l'etat checked d'un item.
        
        Args:
            item_id: L'ID de l'item
            
        Returns:
            bool: Le nouvel etat de l'item
        """
        checklist = self.get_checklist()
        
        for item in checklist:
            if item.get('id') == item_id:
                item['checked'] = not item.get('checked', False)
                self.data['checklist'] = checklist
                self.save_data()
                return item['checked']
        
        return False
    
    def delete_checklist_item(self, item_id: int) -> bool:
        """
        Supprime un item de la checklist.
        
        Args:
            item_id: L'ID de l'item a supprimer
            
        Returns:
            bool: True si la suppression a reussi
        """
        checklist = self.get_checklist()
        initial_count = len(checklist)
        
        checklist = [i for i in checklist if i.get('id') != item_id]
        
        if len(checklist) < initial_count:
            self.data['checklist'] = checklist
            self.save_data()
            return True
        
        return False
    
    def get_checklist_progress(self) -> tuple:
        """
        Calcule la progression de la checklist.
        
        Returns:
            tuple: (nombre_coches, total, pourcentage)
        """
        checklist = self.get_checklist()
        total = len(checklist)
        
        if total == 0:
            return (0, 0, 0)
        
        checked = sum(1 for item in checklist if item.get('checked', False))
        percentage = int((checked / total) * 100)
        
        return (checked, total, percentage)
    
    # ============================================
    # METHODES UTILITAIRES
    # ============================================
    
    def reset_to_defaults(self) -> None:
        """
        Reinitialise toutes les donnees aux valeurs par defaut.
        """
        self.data = DEFAULT_DATA.copy()
        self.save_data()
        print("[DataManager] Données réinitialisées aux valeurs par défaut")
    
    def export_data(self, filepath: str) -> bool:
        """
        Exporte les donnees vers un fichier JSON specifique.
        
        Args:
            filepath: Le chemin du fichier d'export
            
        Returns:
            bool: True si l'export a reussi
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[DataManager] Erreur d'export: {e}")
            return False
    
    def import_data(self, filepath: str) -> bool:
        """
        Importe les donnees depuis un fichier JSON.
        
        Args:
            filepath: Le chemin du fichier a importer
            
        Returns:
            bool: True si l'import a reussi
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.save_data()
            return True
        except Exception as e:
            print(f"[DataManager] Erreur d'import: {e}")
            return False


# Instance globale du gestionnaire (pour acces facile)
data_manager = DataManager()

