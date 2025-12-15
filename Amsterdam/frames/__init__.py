"""
Package frames - Contient tous les frames (onglets) de l'application.

Ce package regroupe les differents modules de l'interface:
- home_frame: Page d'accueil avec resume du voyage (utilise PLACE)
- activities_frame: Planificateur d'activites (utilise GRID)
- budget_frame: Gestion du budget (utilise GRID)
- hotel_frame: Informations sur l'hebergement (utilise PACK)
- transport_frame: Planning des transports (utilise GRID)
- participants_frame: Liste des participants (utilise PACK)
- checklist_frame: Checklist des affaires a emporter (utilise PACK + GRID)
"""

from frames.home_frame import HomeFrame
from frames.activities_frame import ActivitiesFrame
from frames.budget_frame import BudgetFrame
from frames.hotel_frame import HotelFrame
from frames.transport_frame import TransportFrame
from frames.participants_frame import ParticipantsFrame
from frames.checklist_frame import ChecklistFrame

__all__ = [
    'HomeFrame',
    'ActivitiesFrame',
    'BudgetFrame',
    'HotelFrame',
    'TransportFrame',
    'ParticipantsFrame',
    'ChecklistFrame'
]

