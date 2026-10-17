"""
Classes Parking, Place et Placement.
"""

from datetime import datetime

from modele.exceptions import PlaceOccupeeError, PlaceIncompatibleError, VoitureDejaGareeError


class Parking:
    """
    Le parking DreamPark (singleton : il n'en existe qu'une seule instance).

    Il est composé de ses places, repérées par leur identifiant idPlace
    (niveau + numéro, par exemple « A1 »), et des abonnements qu'il propose.
    """

    prix = 0  # attribut de classe qui appartient à la classe elle-même et n’est pas créé individuellement dans chaque appel à __init__.(souligné dans le diagramme)

    _instance = None  # l'instance unique du singleton

    def __new__(cls, *args, **kwargs):
        """
        Renvoie toujours la même instance : la crée au premier appel seulement.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialise = False
        return cls._instance