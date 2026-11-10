"""
Classes Client, Voiture, Abonnement et Contrat.
"""

from datetime import datetime

from modele.exceptions import VoitureDejaGareeError


class Voiture:
    """La voiture d'un client."""

    def __init__(self, immatriculation, hauteur, longueur):
        """
        Crée une voiture hors du parking.

        :param immatriculation: plaque d'immatriculation (str non vide)
        :param hauteur: hauteur en mètres (float)
        :param longueur: longueur en mètres (float)
        :raises ValueError: si l'immatriculation est vide ou si une dimension est négative ou nulle
        """
        if not immatriculation:
            raise ValueError("L'immatriculation ne peut pas être vide")
        if hauteur <= 0 or longueur <= 0:
            raise ValueError("Les dimensions d'une voiture doivent être positives")
        self.__immatriculation = immatriculation  # - privé
        self.__hauteur = hauteur
        self.__longueur = longueur
        self.estDansParking = False               # + public
        self.lieuStationnement = None             # ajout : "A1", "PARTENAIRE" ou None
        self.mesPlacements = []

    @property
    def immatriculation(self):
        return self.__immatriculation

    @property
    def hauteur(self):
        return self.__hauteur

    @property
    def longueur(self):
        return self.__longueur

    def addPlacementV(self, p):
        """
        Associe un placement à la voiture, qui entre dans le parking.

        :param p: le placement (Placement)
        :raises VoitureDejaGareeError: si la voiture est déjà dans le parking
        """
        if self.estDansParking:
            raise VoitureDejaGareeError(f"La voiture {self.__immatriculation} est déjà garée")
        self.mesPlacements.append(p)
        self.estDansParking = True
        self.lieuStationnement = p.place.idPlace


class Abonnement:
    """Une formule d'abonnement proposée par le parking."""

    def __init__(self, libelle, prix, estPackGar):
        """
        Crée une formule d'abonnement.

        :param libelle: nom de la formule (str)
        :param prix: prix (float)
        :param estPackGar: vrai si la formule est un pack garantie (bool)
        """
        self.libelle = libelle
        self.prix = prix
        self.estPackGar = estPackGar
        self.mesContrats = []

    def addContrat(self, contrat):
        """
        Rattache un contrat à cette formule.

        :param contrat: le contrat (Contrat)
        """
        if contrat not in self.mesContrats:
            self.mesContrats.append(contrat)


class Contrat:
    """Classe-association entre un Client et un Abonnement."""

    def __init__(self, client, abonnement):
        """
        Crée un contrat en cours, daté de maintenant.

        :param client: le client (Client)
        :param abonnement: la formule (Abonnement)
        """
        self.client = client
        self.abonnement = abonnement
        self.dateDebut = datetime.now()
        self.dateFin = None
        abonnement.addContrat(self)

    @property
    def estEnCours(self):
        """Attribut dérivé : vrai tant que dateFin n'est pas renseignée."""
        return self.dateFin is None

    def rompreContrat(self):
        """
        Rompt le contrat en renseignant dateFin.

        :return: True si le contrat a été rompu, False s'il l'était déjà
        """
        if not self.estEnCours:
            return False
        self.dateFin = datetime.now()
        return True
