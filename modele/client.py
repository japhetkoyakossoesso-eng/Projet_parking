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


class Client:
    """
    Un client du parking.

    Il n'y a pas de sous-classes Abonné ou Super_Abonné : le statut est calculé
    à partir du contrat en cours (attributs dérivés estAbonne et estSuperAbonne).
    """

    def __init__(self, nom, adresse):
        """
        Crée un client sans voiture ni abonnement.

        :param nom: nom du client (str)
        :param adresse: adresse du client (str)
        """
        self.nom = nom
        self.adresse = adresse
        self.maVoiture = None
        self.mesContrats = []
        self.mesServices = []

    @property
    def contratEnCours(self):
        """:return: le contrat en cours (Contrat), ou None"""
        for contrat in self.mesContrats:
            if contrat.estEnCours:
                return contrat
        return None

    @property
    def monAbonnement(self):
        """:return: la formule du contrat en cours (Abonnement), ou None"""
        contrat = self.contratEnCours
        return contrat.abonnement if contrat else None

    @property
    def estAbonne(self):
        """Attribut dérivé : vrai si le client a un contrat en cours."""
        return self.contratEnCours is not None

    @property
    def estSuperAbonne(self):
        """Attribut dérivé : vrai si le contrat en cours porte sur un pack garantie."""
        ab = self.monAbonnement
        return ab is not None and ab.estPackGar

    @property
    def nbFrequentations(self):
        """Attribut dérivé : nombre de placements de la voiture du client."""
        if self.maVoiture is None:
            return 0
        return len(self.maVoiture.mesPlacements)

    def sAbonner(self, ab):
        """
        Abonne le client : crée un contrat entre lui et l'abonnement.

        S'il avait déjà un contrat en cours, celui-ci est rompu.

        :param ab: la formule choisie (Abonnement)
        :return: le nouveau contrat (Contrat)
        """
        if self.contratEnCours is not None:
            self.contratEnCours.rompreContrat()
        contrat = Contrat(self, ab)
        self.mesContrats.append(contrat)
        return contrat

    def nouvelleVoiture(self, imma, hautV, longV):
        """
        Associe une voiture au client.

        :param imma: immatriculation (str)
        :param hautV: hauteur en mètres (float)
        :param longV: longueur en mètres (float)
        :return: la voiture créée (Voiture)
        :raises ValueError: si une dimension est négative ou nulle
        """
        self.maVoiture = Voiture(imma, hautV, longV)
        return self.maVoiture

    def seDesabonner(self):
        """
        Rompt le contrat en cours.

        :return: True si un contrat a été rompu, False si le client n'était pas abonné
        """
        contrat = self.contratEnCours
        if contrat is None:
            return False
        return contrat.rompreContrat()

    def demanderMaintenance(self):
        """
        Demande une maintenance de la voiture (réservé aux abonnés).

        :return: le service créé (Maintenance), ou False si le client n'est pas abonné
        """
        from modele.services import Maintenance
        if not self.estAbonne:
            return False
        service = Maintenance(self.maVoiture)
        self.mesServices.append(service)
        return service

    def demanderEntretien(self):
        """
        Demande un entretien de la voiture (réservé aux abonnés).

        :return: le service créé (Entretien), ou False si le client n'est pas abonné
        """
        from modele.services import Entretien
        if not self.estAbonne:
            return False
        service = Entretien(self.maVoiture)
        self.mesServices.append(service)
        return service

    def demanderLivraison(self, dateLiv, heure, adresseLiv):
        """
        Demande la livraison de la voiture (réservé aux abonnés).

        Une nouvelle demande remplace celle qui est en attente (politique de flexibilité).

        :param dateLiv: date de livraison (date)
        :param heure: heure de livraison, de 0 à 23 (int)
        :param adresseLiv: adresse de livraison (str)
        :return: le service (Livraison), ou False si le client n'est pas abonné
        :raises ValueError: si l'heure est hors de 0..23 ou si l'adresse est vide
        """
        from modele.parking import Parking
        from modele.services import Livraison
        if not self.estAbonne:
            return False
        for service in self.mesServices:
            if isinstance(service, Livraison) and not service.estEffectue:
                service.modifier(dateLiv, heure, adresseLiv)
                return service
        livraison = Livraison(self.maVoiture, dateLiv, heure, adresseLiv,
                              Parking().voiturierDisponible())
        self.mesServices.append(livraison)
        return livraison

    def entrerParking(self, a):
        """
        Lance la procédure d'entrée par l'accès a.

        :param a: l'accès utilisé (Acces)
        :return: le ticket, ou le message « Aucune place disponible pour votre véhicule »
        """
        return a.lancerProcedureEntree(self)
