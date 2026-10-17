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
        Ajoute une place au parking (ajout au diagramme : il faut bien créer les places).

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

    def historiquePassages(self):
        """
        Renvoie tous les placements, terminés ou en cours (trace de passage).

        Ajout au diagramme fourni, justifié par RF09 et RF10 (statistiques).

        :return: une liste de Placement
        """
        historique = []
        for place in self.__places.values():
            historique.extend(place.mesPlacements)
        return historique


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


