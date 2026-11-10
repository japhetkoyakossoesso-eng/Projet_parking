"""
Classes Acces, Camera, BorneTicket, PanneauAffichage et Teleporteur.
"""

from datetime import datetime

from modele.parking import Parking, Placement

MESSAGE_PLEIN = "Aucune place disponible pour votre véhicule"
PARTENAIRE = "PARTENAIRE"


class Camera:
    """La caméra d'un accès (simulée : elle lit les valeurs de l'objet Voiture)."""

    def capturerHauteur(self, v):
        """
        :param v: la voiture filmée (Voiture)
        :return: la hauteur en mètres (float)
        """
        return v.hauteur

    def capturerLongueur(self, v):
        """
        :param v: la voiture filmée (Voiture)
        :return: la longueur en mètres (float)
        """
        return v.longueur

    def capturerImmatr(self, v):
        """
        :param v: la voiture filmée (Voiture)
        :return: l'immatriculation (str)
        :raises ValueError: si la plaque est illisible (vide ou seulement des espaces)
        """
        if not v.immatriculation or not v.immatriculation.strip():
            raise ValueError("Plaque d'immatriculation illisible")
        return v.immatriculation


class PanneauAffichage:
    """Le panneau d'affichage d'un accès."""

    def afficherNbPlacesDisponibles(self, p):
        """
        :param p: le parking (Parking)
        :return: le texte affiché, contenant le nombre de places libres (str)
        """
        n = p.nbPlacesLibres
        if n == 0:
            return "COMPLET : 0 place disponible"
        return f"{n} place(s) disponible(s)"


class BorneTicket:
    """La borne à tickets-paiement d'un accès."""

    def delivrerTicket(self, c, place=None):
        """
        Délivre un ticket au client si une place lui a été attribuée.

        Le ticket est une chaîne unique : identifiant de la place,
        immatriculation sans tirets et heure d'entrée (par exemple « A1-AB123CD-0930 »).

        :param c: le client (Client)
        :param place: la place attribuée (Place) ; ajout au diagramme pour pouvoir
            délivrer le ticket avant la téléportation, comme dans le diagramme d'activité
        :return: le ticket (str), ou None si aucune place n'est attribuée
        """
        if c.maVoiture is None:
            return None
        if place is not None:
            idPlace = place.idPlace
        elif c.maVoiture.lieuStationnement not in (None, PARTENAIRE):
            idPlace = c.maVoiture.lieuStationnement
        else:
            return None
        immat = c.maVoiture.immatriculation.replace("-", "")
        heure = datetime.now().strftime("%H%M")
        return f"{idPlace}-{immat}-{heure}"

    def proposerServices(self):
        """:return: la liste des services proposés aux abonnés (str)"""
        return "Services proposés : maintenance, entretien, livraison"

    def proposerAbonnements(self, c, p):
        """
        :param c: le client (Client)
        :param p: le parking (Parking)
        :return: la liste des formules d'abonnement du parking (str)
        """
        if not p.mesAbonnements:
            return "Aucun abonnement proposé"
        formules = ", ".join(f"{ab.libelle} ({ab.prix} €)" for ab in p.mesAbonnements)
        return f"Abonnements proposés : {formules}"

    def recupererInfosCarte(self, c):
        """
        Lit la carte d'abonnement du client.

        :param c: le client (Client)
        :return: "super abonné", "abonné", ou "" si le client n'a pas de carte
        """
        if c.estSuperAbonne:
            return "super abonné"
        if c.estAbonne:
            return "abonné"
        return ""

    def proposerTypePaiement(self):
        """:return: les modes de paiement proposés (str)"""
        return "Mode de paiement : CB ou espèces"


class Teleporteur:
    """Un téléporteur, qui conduit les voitures entre l'accès et leur place."""

    def teleporterVoiture(self, v, p):
        """
        Conduit la voiture v à la place p.

        :param v: la voiture (Voiture)
        :param p: la place attribuée (Place)
        :return: le placement créé (Placement)
        :raises ValueError: si p vaut None
        """
        if p is None:
            raise ValueError("Aucune place attribuée")
        return Placement(v, p)

    def teleporterVoitureSuperAbonne(self, v):
        """
        Prend en charge la voiture d'un super-abonné, sans ticket.

        Si DreamPark est plein, la voiture est garée dans le parking partenaire
        (lieuStationnement = « PARTENAIRE »).

        :param v: la voiture (Voiture)
        :return: un message indiquant où la voiture est garée (str)
        """
        place = Parking().rechercherPlace(v)
        if place is not None:
            Placement(v, place)
            return f"Voiture garée en {place.idPlace}"
        v.lieuStationnement = PARTENAIRE
        return "Voiture garée dans le parking partenaire"


class Acces:
    """
    Un des deux accès du parking.

    Il regroupe une caméra, une borne, un panneau et deux téléporteurs
    (TelEntree et TelSortie).
    """

    def __init__(self, parking):
        """
        Crée un accès équipé, rattaché au parking.

        :param parking: le parking (Parking)
        """
        self.monParking = parking
        self.maCamera = Camera()
        self.maBorne = BorneTicket()
        self.monPanneau = PanneauAffichage()
        self.telEntree = Teleporteur()
        self.telSortie = Teleporteur()

    def actionnerCamera(self, c):
        """
        Fait relever par la caméra les informations de la voiture du client.

        :param c: le client (Client)
        :return: la voiture avec son immatriculation et ses dimensions (Voiture)
        :raises ValueError: si le client n'a pas de voiture
        """
        v = c.maVoiture
        if v is None:
            raise ValueError("Le client n'a pas de voiture")
        self.maCamera.capturerImmatr(v)
        self.maCamera.capturerHauteur(v)
        self.maCamera.capturerLongueur(v)
        return v

    def actionnerPanneau(self):
        """
        Met à jour le panneau de l'accès.

        :return: le texte affiché (str)
        """
        return self.monPanneau.afficherNbPlacesDisponibles(self.monParking)

    def lancerProcedureEntree(self, c, modePaiement="CB", choixAbonnement=None):
        """
        Déroule le scénario « Se garer » (diagramme d'activité) pour le client c.

        :param c: le client (Client)
        :param modePaiement: "CB" ou "espèces", pour un client non abonné (ajout)
        :param choixAbonnement: formule choisie à la borne par un client non abonné,
            ou None s'il n'en prend pas (ajout)
        :return: le ticket, un message pour un super-abonné,
            ou le message « Aucune place disponible pour votre véhicule »
        """
        v = self.actionnerCamera(c)
        self.maBorne.recupererInfosCarte(c)

        # Branche super-abonné : pas de recherche de place classique, pas de ticket
        if c.estSuperAbonne:
            message = self.telEntree.teleporterVoitureSuperAbonne(v)
            self.actionnerPanneau()
            return message

        place = self.monParking.rechercherPlace(v)
        if place is None:
            return MESSAGE_PLEIN

        if c.estAbonne:
            self.maBorne.proposerServices()
        else:
            self.maBorne.proposerTypePaiement()
            self.maBorne.proposerAbonnements(c, self.monParking)
            if choixAbonnement is not None:
                c.sAbonner(choixAbonnement)

        ticket = self.maBorne.delivrerTicket(c, place)
        self.telEntree.teleporterVoiture(v, place)
        self.actionnerPanneau()
        return ticket
