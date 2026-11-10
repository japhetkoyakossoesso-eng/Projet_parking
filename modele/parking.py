"""
Classes Parking, Place et Placement.

Partie 0 : seules les signatures et la documentation sont écrites.
Le code des méthodes sera implémenté à partir de la Partie 1.
"""


class Parking:
    """
    Le parking DreamPark (singleton : il n'en existe qu'une seule instance).

    Il est composé de ses places, repérées par leur identifiant idPlace
    (niveau + numéro, par exemple « A1 »), et des abonnements qu'il propose.
    """

    prix = 0  # attribut de classe (souligné dans le diagramme)

    def __init__(self, nbNiveaux, nbPlacesParNiveau):
        """
        Crée le parking.

        :param nbNiveaux: nombre de niveaux du parking
        :param nbPlacesParNiveau: nombre de places par niveau
        """
        raise NotImplementedError("À implémenter en Partie 1")

    @classmethod
    def _reinitialiser(cls):
        """
        Supprime l'instance unique du parking. Réservé aux tests.

        Appelée dans le tearDown() des classes de test pour que chaque test
        reparte d'un parking neuf.
        """
        raise NotImplementedError("À implémenter en Partie 1")

    @property
    def nbPlacesLibres(self):
        """
        Attribut dérivé : nombre de places libres dans tout le parking.

        :return: un entier
        """
        raise NotImplementedError("À implémenter en Partie 1")

    def rechercherPlace(self, v):
        """
        Cherche une place libre assez grande pour la voiture v.

        Une place convient si elle est libre et si sa hauteur et sa longueur
        sont supérieures ou égales à celles de la voiture.

        :param v: la voiture à garer (Voiture)
        :return: la place trouvée (Place), ou None si aucune ne convient
        """
        raise NotImplementedError("À implémenter en Partie 1")

    def nbPlacesLibresParNiveau(self, niveau):
        """
        Compte les places libres d'un niveau.

        :param niveau: la lettre du niveau, par exemple 'A'
        :return: le nombre de places libres (int)
        :raises ValueError: si le niveau n'existe pas
        """
        raise NotImplementedError("À implémenter en Partie 1")

    def addAbonnement(self, ab):
        """
        Ajoute une formule d'abonnement proposée par le parking (sans doublon).

        :param ab: l'abonnement à ajouter (Abonnement)
        """
        raise NotImplementedError("À implémenter en Partie 1")

    def historiquePassages(self):
        """
        Renvoie tous les placements, terminés ou en cours (trace de passage).

        Ajout au diagramme fourni, justifié par RF09 et RF10 (statistiques).

        :return: une liste de Placement
        """
        raise NotImplementedError("À implémenter en Partie 3")


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
        raise NotImplementedError("À implémenter en Partie 1")

    @property
    def idPlace(self):
        """
        Identifiant unique de la place : niveau + numéro, par exemple « A1 ».

        :return: une chaîne
        """
        raise NotImplementedError("À implémenter en Partie 1")

    def addPlacementP(self, p):
        """
        Associe un placement à la place, qui devient occupée.

        :param p: le placement (Placement)
        :raises PlaceOccupeeError: si la place est déjà occupée
        :raises PlaceIncompatibleError: si la voiture est trop grande pour la place
        """
        raise NotImplementedError("À implémenter en Partie 1")


class Placement:
    """
    Classe-association entre une Voiture et une Place : un passage dans le parking.

    Les placements terminés sont conservés et servent de trace pour les statistiques.
    """

    def __init__(self, voiture, place):
        """
        Crée un placement en cours, daté d'aujourd'hui.

        :param voiture: la voiture garée (Voiture)
        :param place: la place occupée (Place)
        """
        raise NotImplementedError("À implémenter en Partie 1")

    @property
    def estEnCours(self):
        """
        Attribut dérivé : vrai tant que dateFin n'est pas renseignée.

        :return: un booléen
        """
        raise NotImplementedError("À implémenter en Partie 1")

    def partirPlace(self):
        """
        Termine le placement : renseigne dateFin, libère la place et sort la voiture.

        :return: True si le placement a été terminé, False s'il l'était déjà
        """
        raise NotImplementedError("À implémenter en Partie 2")
