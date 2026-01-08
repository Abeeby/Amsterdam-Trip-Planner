"""
data_manager.py - Gestionnaire de donnees pour l'application Amsterdam Trip Planner.

Ce module gere toutes les operations de lecture et d'ecriture des donnees
dans le fichier JSON. Il assure la persistance des donnees entre les sessions.

Ce module utilise des fonctions simples et une variable globale pour stocker
les donnees en memoire.
"""

import json
import os
from datetime import datetime
import copy

from config import DATA_FILE, DATA_DIR, DEFAULT_DATA

# ============================================
# VARIABLE GLOBALE POUR LES DONNEES
# ============================================

# Dictionnaire qui contient toutes les donnees en memoire
_data = {}

# ============================================
# FONCTIONS DE BASE (chargement/sauvegarde)
# ============================================

def _ensure_data_directory():
    """
    Cree le repertoire data s'il n'existe pas.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"[DataManager] Repertoire cree: {DATA_DIR}")


def load_data():
    """
    Charge les donnees depuis le fichier JSON.

    Si le fichier n'existe pas ou est corrompu, utilise les donnees
    par defaut definies dans config.py.

    Returns:
        Les donnees chargees (dictionnaire)
    """
    global _data

    _ensure_data_directory()

    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                _data = json.load(f)
            print(f"[DataManager] Donnees chargees depuis {DATA_FILE}")
        else:
            # Utiliser les donnees par defaut
            _data = copy.deepcopy(DEFAULT_DATA)
            save_data()  # Sauvegarder les donnees par defaut
            print("[DataManager] Fichier de donnees cree avec les valeurs par defaut")
    except json.JSONDecodeError as e:
        print(f"[DataManager] Erreur de lecture JSON: {e}")
        print("[DataManager] Utilisation des donnees par defaut")
        _data = copy.deepcopy(DEFAULT_DATA)
        save_data()
    except Exception as e:
        print(f"[DataManager] Erreur inattendue: {e}")
        _data = copy.deepcopy(DEFAULT_DATA)

    return _data


def save_data():
    """
    Sauvegarde les donnees dans le fichier JSON.

    Returns:
        True si la sauvegarde a reussi, False sinon
    """
    global _data

    try:
        # Ajouter un timestamp de derniere modification
        _data['last_modified'] = datetime.now().isoformat()

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(_data, f, ensure_ascii=False, indent=2)

        print(f"[DataManager] Donnees sauvegardees dans {DATA_FILE}")
        return True
    except Exception as e:
        print(f"[DataManager] Erreur de sauvegarde: {e}")
        return False


def reset_to_defaults():
    """
    Reinitialise toutes les donnees aux valeurs par defaut.
    """
    global _data
    _data = copy.deepcopy(DEFAULT_DATA)
    save_data()
    print("[DataManager] Donnees reinitialisees aux valeurs par defaut")


# ============================================
# FONCTIONS POUR LES INFORMATIONS DU VOYAGE
# ============================================

def get_voyage_info():
    """
    Recupere les informations generales du voyage.

    Returns:
        Les informations du voyage (dictionnaire)
    """
    return _data.get('voyage_info', {})


def update_voyage_info(info):
    """
    Met a jour les informations du voyage.

    Args:
        info: Les nouvelles informations (dictionnaire)
    """
    _data['voyage_info'] = info
    save_data()


# ============================================
# FONCTIONS POUR LES ACTIVITES
# ============================================

def get_activites():
    """
    Recupere la liste des activites.

    Returns:
        Liste des activites
    """
    return _data.get('activites', [])


def add_activite(activite):
    """
    Ajoute une nouvelle activite.

    Args:
        activite: Les donnees de l'activite (dictionnaire)

    Returns:
        L'ID de la nouvelle activite
    """
    activites = get_activites()

    # Generer un nouvel ID
    new_id = max([a.get('id', 0) for a in activites], default=0) + 1
    activite['id'] = new_id

    activites.append(activite)
    _data['activites'] = activites
    save_data()

    return new_id


def update_activite(activite_id, activite):
    """
    Met a jour une activite existante.

    Args:
        activite_id: L'ID de l'activite a modifier
        activite: Les nouvelles donnees (dictionnaire)

    Returns:
        True si la mise a jour a reussi
    """
    activites = get_activites()

    for i, a in enumerate(activites):
        if a.get('id') == activite_id:
            activite['id'] = activite_id
            activites[i] = activite
            _data['activites'] = activites
            save_data()
            return True

    return False


def delete_activite(activite_id):
    """
    Supprime une activite.

    Args:
        activite_id: L'ID de l'activite a supprimer

    Returns:
        True si la suppression a reussi
    """
    activites = get_activites()
    initial_count = len(activites)

    activites = [a for a in activites if a.get('id') != activite_id]

    if len(activites) < initial_count:
        _data['activites'] = activites
        save_data()
        return True

    return False


# ============================================
# FONCTIONS POUR LE BUDGET
# ============================================

def get_budget():
    """
    Recupere les informations de budget.

    Returns:
        Les donnees du budget (dictionnaire)
    """
    return _data.get('budget', {'budget_prevu': 0, 'depenses': []})


def get_depenses():
    """
    Recupere la liste des depenses.

    Returns:
        Liste des depenses
    """
    return get_budget().get('depenses', [])


def add_depense(depense):
    """
    Ajoute une nouvelle depense.

    Args:
        depense: Les donnees de la depense (dictionnaire)

    Returns:
        L'ID de la nouvelle depense
    """
    budget = get_budget()
    depenses = budget.get('depenses', [])

    # Generer un nouvel ID
    new_id = max([d.get('id', 0) for d in depenses], default=0) + 1
    depense['id'] = new_id

    depenses.append(depense)
    budget['depenses'] = depenses
    _data['budget'] = budget
    save_data()

    return new_id


def update_budget_prevu(montant):
    """
    Met a jour le budget prevu.

    Args:
        montant: Le nouveau budget prevu
    """
    budget = get_budget()
    budget['budget_prevu'] = montant
    _data['budget'] = budget
    save_data()


def delete_depense(depense_id):
    """
    Supprime une depense.

    Args:
        depense_id: L'ID de la depense a supprimer

    Returns:
        True si la suppression a reussi
    """
    budget = get_budget()
    depenses = budget.get('depenses', [])
    initial_count = len(depenses)

    depenses = [d for d in depenses if d.get('id') != depense_id]

    if len(depenses) < initial_count:
        budget['depenses'] = depenses
        _data['budget'] = budget
        save_data()
        return True

    return False


def get_total_depenses():
    """
    Calcule le total des depenses.

    Returns:
        Le total des depenses (float)
    """
    depenses = get_depenses()
    return sum(d.get('montant', 0) for d in depenses)


def get_depenses_by_category():
    """
    Calcule le total des depenses par categorie.

    Returns:
        Dictionnaire avec le total par categorie
    """
    depenses = get_depenses()
    totaux = {}

    for d in depenses:
        cat = d.get('categorie', 'Autre')
        totaux[cat] = totaux.get(cat, 0) + d.get('montant', 0)

    return totaux


# ============================================
# FONCTIONS POUR L'HOTEL
# ============================================

def get_hotel():
    """
    Recupere les informations de l'hotel.

    Returns:
        Les donnees de l'hotel (dictionnaire)
    """
    return _data.get('hotel', {})


def update_hotel(hotel):
    """
    Met a jour les informations de l'hotel.

    Args:
        hotel: Les nouvelles informations (dictionnaire)
    """
    _data['hotel'] = hotel
    save_data()


# ============================================
# FONCTIONS POUR LE TRANSPORT
# ============================================

def get_transport():
    """
    Recupere les informations de transport.

    Returns:
        Les donnees de transport (dictionnaire)
    """
    return _data.get('transport', {})


def update_transport(transport):
    """
    Met a jour les informations de transport.

    Args:
        transport: Les nouvelles informations (dictionnaire)
    """
    _data['transport'] = transport
    save_data()


# ============================================
# FONCTIONS POUR LES PARTICIPANTS
# ============================================

def get_participants():
    """
    Recupere la liste des participants.

    Returns:
        Liste des participants
    """
    return _data.get('participants', [])


def add_participant(participant):
    """
    Ajoute un nouveau participant.

    Args:
        participant: Les donnees du participant (dictionnaire)

    Returns:
        L'ID du nouveau participant
    """
    participants = get_participants()

    # Generer un nouvel ID
    new_id = max([p.get('id', 0) for p in participants], default=0) + 1
    participant['id'] = new_id

    participants.append(participant)
    _data['participants'] = participants
    save_data()

    return new_id


def update_participant(participant_id, participant):
    """
    Met a jour un participant existant.

    Args:
        participant_id: L'ID du participant a modifier
        participant: Les nouvelles donnees (dictionnaire)

    Returns:
        True si la mise a jour a reussi
    """
    participants = get_participants()

    for i, p in enumerate(participants):
        if p.get('id') == participant_id:
            participant['id'] = participant_id
            participants[i] = participant
            _data['participants'] = participants
            save_data()
            return True

    return False


def delete_participant(participant_id):
    """
    Supprime un participant.

    Args:
        participant_id: L'ID du participant a supprimer

    Returns:
        True si la suppression a reussi
    """
    participants = get_participants()
    initial_count = len(participants)

    participants = [p for p in participants if p.get('id') != participant_id]

    if len(participants) < initial_count:
        _data['participants'] = participants
        save_data()
        return True

    return False


# ============================================
# FONCTIONS POUR LA CHECKLIST
# ============================================

def get_checklist():
    """
    Recupere la checklist.

    Returns:
        Liste des items de la checklist
    """
    return _data.get('checklist', [])


def add_checklist_item(item):
    """
    Ajoute un item a la checklist.

    Args:
        item: Les donnees de l'item (dictionnaire)

    Returns:
        L'ID du nouvel item
    """
    checklist = get_checklist()

    # Generer un nouvel ID
    new_id = max([i.get('id', 0) for i in checklist], default=0) + 1
    item['id'] = new_id
    item['checked'] = item.get('checked', False)

    checklist.append(item)
    _data['checklist'] = checklist
    save_data()

    return new_id


def toggle_checklist_item(item_id):
    """
    Inverse l'etat checked d'un item.

    Args:
        item_id: L'ID de l'item

    Returns:
        Le nouvel etat de l'item (True ou False)
    """
    checklist = get_checklist()

    for item in checklist:
        if item.get('id') == item_id:
            item['checked'] = not item.get('checked', False)
            _data['checklist'] = checklist
            save_data()
            return item['checked']

    return False


def delete_checklist_item(item_id):
    """
    Supprime un item de la checklist.

    Args:
        item_id: L'ID de l'item a supprimer

    Returns:
        True si la suppression a reussi
    """
    checklist = get_checklist()
    initial_count = len(checklist)

    checklist = [i for i in checklist if i.get('id') != item_id]

    if len(checklist) < initial_count:
        _data['checklist'] = checklist
        save_data()
        return True

    return False


def get_checklist_progress():
    """
    Calcule la progression de la checklist.

    Returns:
        Tuple (nombre_coches, total, pourcentage)
    """
    checklist = get_checklist()
    total = len(checklist)

    if total == 0:
        return (0, 0, 0)

    checked = sum(1 for item in checklist if item.get('checked', False))
    percentage = int((checked / total) * 100)

    return (checked, total, percentage)


# ============================================
# INITIALISATION AU CHARGEMENT DU MODULE
# ============================================

# Charger les donnees automatiquement quand le module est importe
load_data()
