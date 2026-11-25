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

    prix = 0  # attribut de classe

    _instance = None  # l'instance unique du singleton

    def __new__(cls, *args, **kwargs):
        """
        Renvoie toujours la même instance : la crée au premier appel seulement.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialise = False
        return cls._instance

    def __init__(self, nbNiveaux=1, nbPlacesParNiveau=0):
        """
        Crée le parking. Les appels suivants à Parking() ne changent rien.

        :param nbNiveaux: nombre de niveaux du parking (A, B, C...)
        :param nbPlacesParNiveau: nombre de places prévues par niveau
        """
        if self._initialise:
            return
        self.nbNiveaux = nbNiveaux                    # + public
        self.__nbPlacesParNiveau = nbPlacesParNiveau  # - privé
        self.__places = {}                            # idPlace -> Place
        self.mesAbonnements = []
        self.mesVoituriers = []
        self._initialise = True

    @classmethod
    def _reinitialiser(cls):
        """
        Supprime l'instance unique du parking. Réservé aux tests.

        Appelée dans le tearDown() des classes de test pour que chaque test
        reparte d'un parking neuf.
        """
        cls._instance = None

    def niveaux(self):
        """
        :return: la liste des lettres de niveau, par exemple ['A', 'B']
        """
        return [chr(ord('A') + i) for i in range(self.nbNiveaux)]

    def ajouterPlace(self, place):
        """
        Ajoute une place au parking.

        :param place: la place à ajouter (Place)
        :raises ValueError: si une place avec le même idPlace existe déjà,
            ou si son niveau n'existe pas dans le parking
        """
        if place.idPlace in self.__places:
            raise ValueError(f"La place {place.idPlace} existe déjà")
        if place.niveau not in self.niveaux():
            raise ValueError(f"Le niveau {place.niveau} n'existe pas")
        self.__places[place.idPlace] = place

    def getPlace(self, idPlace):
        """
        :param idPlace: identifiant de la place, par exemple "A1"
        :return: la place (Place), ou None si elle n'existe pas
        """
        return self.__places.get(idPlace)

    @property
    def mesPlaces(self):
        """:return: la liste de toutes les places du parking"""
        return list(self.__places.values())

    @property
    def nbPlacesLibres(self):
        """
        Attribut dérivé : nombre de places libres dans tout le parking.

        :return: un entier
        """
        return sum(1 for place in self.__places.values() if place.estLibre)

    def rechercherPlace(self, v):
        """
        Cherche une place libre assez grande pour la voiture v.

        Une place convient si elle est libre et si sa hauteur et sa longueur
        sont supérieures ou égales à celles de la voiture.

        :param v: la voiture à garer (Voiture)
        :return: la place trouvée (Place), ou None si aucune ne convient
        """
        for place in self.__places.values():
            if place.estLibre and place.estCompatible(v):
                return place
        return None

    def nbPlacesLibresParNiveau(self, niveau):
        """
        Compte les places libres d'un niveau.

        :param niveau: la lettre du niveau, par exemple 'A'
        :return: le nombre de places libres (int)
        :raises ValueError: si le niveau n'existe pas
        """
        if niveau not in self.niveaux():
            raise ValueError(f"Le niveau {niveau} n'existe pas")
        return sum(1 for place in self.__places.values()
                   if place.niveau == niveau and place.estLibre)

    def addAbonnement(self, ab):
        """
        Ajoute une formule d'abonnement proposée par le parking (sans doublon).

        :param ab: l'abonnement à ajouter (Abonnement)
        """
        if ab not in self.mesAbonnements:
            self.mesAbonnements.append(ab)

    def voiturierDisponible(self):
        """
        Renvoie un voiturier pour une livraison (en crée un s'il n'y en a aucun).

        :return: un Voiturier
        """
        if not self.mesVoituriers:
            from modele.services import Voiturier
            self.mesVoituriers.append(Voiturier(1))
        return self.mesVoituriers[0]

    def historiquePassages(self):
        """
        Renvoie tous les placements, terminés ou en cours. Sert pour les statistiques.

        :return: une liste de Placement
        """
        historique = []
        for place in self.__places.values():
            historique.extend(place.mesPlacements)
        return historique

    def retrouverPlacement(self, ticket):
        """
        Retrouve un placement actif à partir d'un ticket.

        :param ticket: ticket au format A1-AB123CD-0930
        :return: le Placement correspondant, ou None
        """
        if not isinstance(ticket, str):
            return None

        parties = ticket.split("-")

        if len(parties) != 3:
            return None

        idPlace, immatriculation, heure = parties

        place = self.getPlace(idPlace)

        if place is None:
            return None

        for placement in place.mesPlacements:
            if (
                placement.estEnCours
                and placement.voiture.immatriculation.replace("-", "") == immatriculation
            ):
                return placement

        return None

    # Statistiques (Partie 3) : tout est calculé à partir de historiquePassages()

    def nbPassages(self, debut=None, fin=None):
        """
        Compte les passages (placements) commencés entre debut et fin, bornes incluses.

        :param debut: date ou datetime de début, None pour ne pas limiter
        :param fin: date ou datetime de fin, None pour ne pas limiter
        :return: le nombre de passages (int)
        """
        return len([p for p in self.historiquePassages() if _dansPeriode(p.dateDebut, debut, fin)])

    def passagesParJour(self):
        """
        Regroupe les passages selon le jour d'entrée.

        :return: un dictionnaire {date: nombre de passages}, trié par date
        """
        parJour = {}
        for p in sorted(self.historiquePassages(), key=lambda p: p.dateDebut):
            jour = p.dateDebut.date()
            parJour[jour] = parJour.get(jour, 0) + 1
        return parJour

    def dureeMoyenneStationnement(self):
        """
        Durée moyenne des passages terminés. Les placements en cours sont ignorés.

        :return: la durée moyenne en minutes (float), ou None s'il n'y a aucun passage terminé
        """
        durees = [(p.dateFin - p.dateDebut).total_seconds() / 60
                  for p in self.historiquePassages() if not p.estEnCours]
        if not durees:
            return None
        return sum(durees) / len(durees)

    def tauxOccupation(self):
        """
        Part des places occupées en ce moment.

        :return: un float entre 0 et 1 (0 si le parking n'a aucune place)
        """
        places = self.mesPlaces
        if not places:
            return 0.0
        return (len(places) - self.nbPlacesLibres) / len(places)

    def historiqueVoiture(self, immat):
        """
        Les passages d'une voiture, du plus ancien au plus récent.

        :param immat: immatriculation de la voiture (str)
        :return: une liste de Placement, vide si la voiture n'est jamais venue
        """
        passages = [p for p in self.historiquePassages() if p.voiture.immatriculation == immat]
        return sorted(passages, key=lambda p: p.dateDebut)

    def clientsReguliers(self, clients, seuil):
        """
        Les clients non abonnés venus au moins seuil fois : on peut leur proposer un abonnement.

        :param clients: les clients à examiner (list de Client)
        :param seuil: nombre minimal de passages (int, au moins 1)
        :return: une liste de Client
        :raises ValueError: si seuil est inférieur à 1
        """
        if seuil < 1:
            raise ValueError("Le seuil doit être au moins 1")
        return [c for c in clients if not c.estAbonne and c.nbFrequentations >= seuil]

    def activiteParService(self, clients):
        """
        Compte les services demandés par les clients, par type de service.

        :param clients: les clients à examiner (list de Client)
        :return: {"Maintenance": n, "Entretien": n, "Livraison": n}
        """
        activite = {"Maintenance": 0, "Entretien": 0, "Livraison": 0}
        for c in clients:
            for service in c.mesServices:
                nom = type(service).__name__
                if nom in activite:
                    activite[nom] += 1
        return activite


def _dansPeriode(moment, debut, fin):
    """
    Vrai si moment (datetime) est entre debut et fin, bornes incluses.
    Une borne de type date couvre toute la journée.
    """
    jour = moment.date()
    if debut is not None:
        if isinstance(debut, datetime):
            if moment < debut:
                return False
        elif jour < debut:
            return False
    if fin is not None:
        if isinstance(fin, datetime):
            if moment > fin:
                return False
        elif jour > fin:
            return False
    return True


class Place:
    """Une place du parking, identifiée par son niveau et son numéro."""

    def __init__(self, numero, niveau, longueur, hauteur):
        """
        Crée une place libre.

        :param numero: numéro de la place dans son niveau (int)
        :param niveau: lettre du niveau (str d'un caractère)
        :param longueur: longueur de la place en mètres (float)
        :param hauteur: hauteur de la place en mètres (float)
        :raises ValueError: si une dimension est négative ou nulle
        """
        if longueur <= 0 or hauteur <= 0:
            raise ValueError("Les dimensions d'une place doivent être positives")
        self.numero = numero        # + public
        self.__niveau = niveau      # - privé
        self.__longueur = longueur
        self.__hauteur = hauteur
        self.__estLibre = True
        self.mesPlacements = []     # tous les placements passés et en cours

    @property
    def niveau(self):
        return self.__niveau

    @property
    def longueur(self):
        return self.__longueur

    @property
    def hauteur(self):
        return self.__hauteur

    @property
    def estLibre(self):
        return self.__estLibre

    @property
    def idPlace(self):
        """
        Identifiant unique de la place : niveau + numéro, par exemple « A1 ».

        :return: une chaîne
        """
        return f"{self.__niveau}{self.numero}"

    def estCompatible(self, v):
        """
        Vérifie que la voiture v tient dans la place (dimensions égales acceptées).

        :param v: la voiture (Voiture)
        :return: True si la voiture tient, False sinon
        """
        return v.hauteur <= self.__hauteur and v.longueur <= self.__longueur

    def addPlacementP(self, p):
        """
        Associe un placement à la place, qui devient occupée.

        :param p: le placement (Placement)
        :raises PlaceOccupeeError: si la place est déjà occupée
        :raises PlaceIncompatibleError: si la voiture est trop grande pour la place
        """
        if not self.__estLibre:
            raise PlaceOccupeeError(f"La place {self.idPlace} est déjà occupée")
        if not self.estCompatible(p.voiture):
            raise PlaceIncompatibleError(f"La voiture ne tient pas dans la place {self.idPlace}")
        self.mesPlacements.append(p)
        self.__estLibre = False

    def liberer(self):
        """Rend la place libre. Appelée par Placement.partirPlace()."""
        self.__estLibre = True


class Placement:
    """
    Classe-association entre une Voiture et une Place : un passage dans le parking.

    Les placements terminés sont conservés et servent de trace pour les statistiques.
    """

    def __init__(self, voiture, place):
        """
        Crée un placement en cours, daté de maintenant, et gare la voiture.

        :param voiture: la voiture garée (Voiture)
        :param place: la place occupée (Place)
        :raises VoitureDejaGareeError: si la voiture est déjà dans le parking
        :raises PlaceOccupeeError: si la place est déjà occupée
        :raises PlaceIncompatibleError: si la voiture est trop grande pour la place
        """
        if voiture.estDansParking:
            raise VoitureDejaGareeError(f"La voiture {voiture.immatriculation} est déjà garée")
        self.voiture = voiture
        self.place = place
        self.dateDebut = datetime.now()
        self.dateFin = None
        place.addPlacementP(self)    # vérifie la place en premier
        voiture.addPlacementV(self)  # puis la voiture entre dans le parking

    @property
    def estEnCours(self):
        """
        Attribut dérivé : vrai tant que dateFin n'est pas renseignée.

        :return: un booléen
        """
        return self.dateFin is None

    def partirPlace(self):
        """
        Termine le placement : renseigne dateFin, libère la place et sort la voiture.

        :return: True si le placement a été terminé, False s'il l'était déjà
        """
        if not self.estEnCours:
            return False
        self.dateFin = datetime.now()
        self.place.liberer()
        self.voiture.estDansParking = False
        self.voiture.lieuStationnement = None
        return True
