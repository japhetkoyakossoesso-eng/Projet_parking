"""
Classes Service, Maintenance, Entretien, Livraison et Voiturier.
"""

from datetime import datetime

from modele.parking import Parking, Placement
from modele.exceptions import LivraisonSansDemandeError


def _placementEnCours(v):
    """:return: le placement en cours de la voiture v, ou None"""
    for p in v.mesPlacements:
        if p.estEnCours:
            return p
    return None


class Service:
    """Classe mère des services proposés aux abonnés."""

    def __init__(self, voiture):
        """
        Crée une demande de service, avec dateDemande à maintenant.

        :param voiture: la voiture concernée (Voiture)
        """
        self.voiture = voiture
        self.dateDemande = datetime.now()
        self.dateService = None
        self.rapport = ""

    @property
    def estEffectue(self):
        """Vrai quand le service a été réalisé."""
        return self.dateService is not None

    def _sortirEtRegarer(self, v, nomService):
        """
        Sort la voiture de sa place, réalise le service, puis la regare.

        :param v: la voiture (Voiture)
        :param nomService: "maintenance" ou "entretien", pour le rapport
        """
        placement = _placementEnCours(v)
        if placement is not None:
            placement.partirPlace()
        self.dateService = datetime.now()
        self.rapport = f"{nomService.capitalize()} effectué(e) le {self.dateService:%d/%m/%Y à %H:%M}"
        place = Parking().rechercherPlace(v)
        if place is not None:
            Placement(v, place)


class Maintenance(Service):
    """Une maintenance du véhicule."""

    def effectuerMaintenance(self, v=None):
        """
        Réalise la maintenance : sort la voiture, renseigne dateService et rapport,
        puis la regare (nouveau placement).

        :param v: la voiture concernée (Voiture) ; par défaut, celle de la demande
        """
        self._sortirEtRegarer(v or self.voiture, "maintenance")


class Entretien(Service):
    """Un entretien du véhicule."""

    def effectuerEntretien(self):
        """Réalise l'entretien, avec le même déroulement que la maintenance."""
        self._sortirEtRegarer(self.voiture, "entretien")


class Livraison(Service):
    """Une livraison du véhicule à une adresse et une heure données."""

    def __init__(self, voiture, dateLiv, heure, adresseLiv, voiturier):
        """
        Crée une demande de livraison et la confie au voiturier.

        :param voiture: la voiture à livrer (Voiture)
        :param dateLiv: date de livraison (date)
        :param heure: heure de livraison, de 0 à 23 (int)
        :param adresseLiv: adresse de livraison (str)
        :param voiturier: le voiturier chargé de la livraison (Voiturier)
        :raises ValueError: si l'heure est hors de 0..23 ou si l'adresse est vide
        """
        super().__init__(voiture)
        self.voiturier = voiturier
        self.modifier(dateLiv, heure, adresseLiv)
        voiturier.mesLivraisons.append(self)

    def modifier(self, dateLiv, heure, adresseLiv):
        """
        Change la date, l'heure ou l'adresse (politique de flexibilité).

        :raises ValueError: si l'heure est hors de 0..23 ou si l'adresse est vide
        """
        if not 0 <= heure <= 23:
            raise ValueError("L'heure de livraison doit être comprise entre 0 et 23")
        if not adresseLiv:
            raise ValueError("L'adresse de livraison ne peut pas être vide")
        self.dateLivraison = dateLiv
        self.heure = heure
        self.adresse = adresseLiv

    def effectuerLivraison(self):
        """Sort la voiture du parking et la confie au voiturier."""
        self.voiturier.livrerVoiture(self.voiture, self.dateLivraison, self.heure)


class Voiturier:
    """Un voiturier qui livre les voitures des abonnés."""

    def __init__(self, numVoiturier):
        """
        Crée un voiturier.

        :param numVoiturier: numéro du voiturier (int)
        """
        self.__numVoiturier = numVoiturier
        self.mesLivraisons = []

    @property
    def numVoiturier(self):
        return self.__numVoiturier

    def livrerVoiture(self, v, date, heure):
        """
        Livre la voiture v à la date et à l'heure prévues.

        :param v: la voiture (Voiture)
        :param date: date de livraison (date)
        :param heure: heure de livraison, de 0 à 23 (int)
        :raises LivraisonSansDemandeError: si aucune livraison n'a été demandée pour v
        """
        livraison = None
        for l in self.mesLivraisons:
            if l.voiture is v and not l.estEffectue:
                livraison = l
                break
        if livraison is None:
            raise LivraisonSansDemandeError(
                f"Aucune livraison demandée pour la voiture {v.immatriculation}")
        placement = _placementEnCours(v)
        if placement is not None:
            placement.partirPlace()
        livraison.dateService = datetime.now()
        livraison.rapport = (f"Livrée par le voiturier {self.__numVoiturier} "
                             f"le {date} à {heure}h, {livraison.adresse}")
