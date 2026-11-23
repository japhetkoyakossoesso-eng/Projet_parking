"""
Contrôleur de l'application : fait le lien entre la vue console et le modèle.
"""

from modele.parking import Parking, Place
from modele.client import Client, Abonnement
from modele.acces import Acces, MESSAGE_PLEIN, PARTENAIRE


class ControleurParking:
    """
    Crée le parking de démonstration et exécute les actions demandées par la vue.

    La vue ne connaît pas le modèle : elle passe toujours par ce contrôleur.
    """

    def __init__(self):
        """Crée un parking de 2 niveaux (A et B), ses formules et ses deux accès."""
        self.parking = Parking(nbNiveaux=2, nbPlacesParNiveau=5)
        self.__creerPlaces()
        self.abonnements = [
            Abonnement("Mensuel", 30, False),
            Abonnement("Pack garantie", 60, True),
        ]
        for ab in self.abonnements:
            self.parking.addAbonnement(ab)
        self.acces = [Acces(self.parking), Acces(self.parking)]
        self.clients = []

    def __creerPlaces(self):
        """Crée 10 places de tailles différentes, pour tester la compatibilité."""
        dimensions = [(5.00, 2.00), (5.00, 2.00), (4.50, 1.80), (4.00, 1.60), (6.00, 2.50)]
        for niveau in self.parking.niveaux():
            for numero, (longueur, hauteur) in enumerate(dimensions, start=1):
                self.parking.ajouterPlace(Place(numero, niveau, longueur, hauteur))

    # Clients
    def nouveauClient(self, nom, adresse, immat, hauteur, longueur):
        """
        Crée un client et sa voiture.

        :return: le client créé (Client)
        :raises ValueError: si les données de la voiture sont invalides
        """
        client = Client(nom, adresse)
        client.nouvelleVoiture(immat, hauteur, longueur)
        self.clients.append(client)
        return client

    def getClient(self, indice):
        """:return: le client numéro indice (à partir de 1), ou None"""
        if 1 <= indice <= len(self.clients):
            return self.clients[indice - 1]
        return None

    def statut(self, client):
        """:return: "super abonné", "abonné" ou "non abonné" (str)"""
        if client.estSuperAbonne:
            return "super abonné"
        if client.estAbonne:
            return "abonné"
        return "non abonné"

    def lieu(self, client):
        """:return: où se trouve la voiture du client, en clair (str)"""
        lieu = client.maVoiture.lieuStationnement
        if lieu is None:
            return "hors du parking"
        if lieu == PARTENAIRE:
            return "parking partenaire"
        return f"place {lieu}"

    # Abonnements
    def getAbonnement(self, indice):
        """:return: la formule numéro indice (à partir de 1), ou None"""
        if 1 <= indice <= len(self.abonnements):
            return self.abonnements[indice - 1]
        return None

    def sAbonner(self, client, abonnement):
        """Abonne le client à la formule choisie."""
        client.sAbonner(abonnement)

    # Se garer
    def estDejaGare(self, client):
        """:return: vrai si la voiture du client est déjà prise en charge (bool)"""
        return client.maVoiture.lieuStationnement is not None

    def textesBorne(self, client, numAcces):
        """
        :return: ce que la borne propose au client avant l'entrée (list de str)
        """
        borne = self.acces[numAcces - 1].maBorne
        if client.estSuperAbonne:
            return []
        if client.estAbonne:
            return [borne.proposerServices()]
        return [borne.proposerTypePaiement(),
                borne.proposerAbonnements(client, self.parking)]

    def raisonRefus(self, client):
        """
        Explique pourquoi la voiture du client ne peut pas se garer dans DreamPark.

        :return: la raison (str), ou None si une place libre lui convient
        """
        v = client.maVoiture
        if self.parking.rechercherPlace(v) is not None:
            return None
        places = self.parking.mesPlaces
        hauteurMax = max(p.hauteur for p in places)
        longueurMax = max(p.longueur for p in places)
        tropHaute = v.hauteur > hauteurMax
        tropLongue = v.longueur > longueurMax
        if tropHaute and tropLongue:
            return (f"votre voiture est trop haute ({v.hauteur:.2f} m) et trop longue "
                    f"({v.longueur:.2f} m). Nos places mesurent au plus {hauteurMax:.2f} m "
                    f"de haut et {longueurMax:.2f} m de long.")
        if tropHaute:
            return (f"votre voiture est trop haute ({v.hauteur:.2f} m). "
                    f"Nos places mesurent au plus {hauteurMax:.2f} m de haut.")
        if tropLongue:
            return (f"votre voiture est trop longue ({v.longueur:.2f} m). "
                    f"Nos places mesurent au plus {longueurMax:.2f} m de long.")
        compatibles = [p.idPlace for p in places if p.estCompatible(v)]
        if not compatibles:
            return "aucune place n'a à la fois la hauteur et la longueur de votre voiture."
        if self.parking.nbPlacesLibres == 0:
            return "le parking est complet."
        return ("les places assez grandes pour votre voiture "
                f"({', '.join(compatibles)}) sont toutes occupées.")

    def seGarer(self, client, numAcces, modePaiement="CB", choixAbonnement=None):
        """
        Lance le use case « Se garer » par l'accès numAcces (1 ou 2).

        :return: (réussi, message) : réussi est un bool, message le ticket ou l'explication
        """
        acces = self.acces[numAcces - 1]
        etaitSuperAbonne = client.estSuperAbonne
        raison = self.raisonRefus(client)
        resultat = acces.lancerProcedureEntree(client, modePaiement, choixAbonnement)
        if resultat == MESSAGE_PLEIN:
            return False, f"{resultat} : {raison}"
        if etaitSuperAbonne:
            return True, resultat
        return True, f"Ticket : {resultat}"

    # Sortir du parking
    def sortir(self, client, numAcces, ticket=None):
        """
        Fait sortir la voiture du client par l'accès numAcces.

        Un super-abonné sort sans ticket, tout comme une voiture garée au parking
        partenaire (même si le client s'est désabonné depuis). Les autres clients
        doivent présenter leur ticket.

        :return: (réussi, message)
        """
        acces = self.acces[numAcces - 1]

        if client.estSuperAbonne or client.maVoiture.lieuStationnement == PARTENAIRE:
            voiture = acces.lancerProcedureSortieSuperAbonne(client)
        else:
            if ticket is None:
                return False, "Vous devez présenter votre ticket."
            placement = self.parking.retrouverPlacement(ticket)
            if placement is not None and placement.voiture is not client.maVoiture:
                return False, "Ce ticket ne correspond pas à votre voiture."
            voiture = acces.lancerProcedureSortie(ticket)

        if voiture is None:
            return False, "Impossible de récupérer votre voiture."

        return True, "Votre voiture vous a été rendue."

    # Services
    def livraisonEnAttente(self, client):
        """:return: la livraison non effectuée du client (Livraison), ou None"""
        from modele.services import Livraison
        for service in client.mesServices:
            if isinstance(service, Livraison) and not service.estEffectue:
                return service
        return None

    def demanderService(self, client, typeService, dateLiv=None, heure=None, adresse=None):
        """
        Demande un service pour le client (réservé aux abonnés).

        :param typeService: "maintenance", "entretien" ou "livraison"
        :return: (réussi, message)
        """
        if not client.estAbonne:
            return False, "Les services sont réservés aux abonnés."
        try:
            if typeService == "maintenance":
                service = client.demanderMaintenance()
            elif typeService == "entretien":
                service = client.demanderEntretien()
            else:
                service = client.demanderLivraison(dateLiv, heure, adresse)
        except ValueError as e:
            return False, f"Demande refusée : {e}"
        if service is False:
            return False, "Les services sont réservés aux abonnés."
        return True, f"Demande de {typeService} enregistrée."

    def modifierLivraison(self, client, dateLiv, heure, adresse):
        """
        Modifie la livraison en attente du client.

        :return: (réussi, message)
        """
        livraison = self.livraisonEnAttente(client)
        if livraison is None:
            return False, "Vous n'avez aucune livraison en attente."
        try:
            livraison.modifier(dateLiv, heure, adresse)
        except ValueError as e:
            return False, f"Modification refusée : {e}"
        return True, "Livraison modifiée."

    def servicesEnAttente(self, client):
        """:return: les services demandés par le client et pas encore réalisés (list)"""
        return [s for s in client.mesServices if not s.estEffectue]

    def realiserServices(self, client):
        """
        Réalise les services en attente du client : maintenance et entretien
        (la voiture est sortie puis regarée), livraison (le voiturier livre la voiture).

        :return: un message par service (list de str)
        """
        from modele.services import Maintenance, Entretien, Livraison
        messages = []
        for service in self.servicesEnAttente(client):
            if isinstance(service, Livraison):
                service.effectuerLivraison()
                messages.append(f"Livraison faite : {service.rapport}")
            elif not service.voiture.estDansParking:
                messages.append("Maintenance ou entretien impossible : la voiture n'est pas dans le parking.")
            elif isinstance(service, Maintenance):
                service.effectuerMaintenance()
                messages.append(f"{service.rapport}, voiture regarée : {self.lieu(client)}")
            elif isinstance(service, Entretien):
                service.effectuerEntretien()
                messages.append(f"{service.rapport}, voiture regarée : {self.lieu(client)}")
        return messages

    # Affichage du parking
    def panneaux(self):
        """:return: le texte des deux panneaux (list de str)"""
        return [a.actionnerPanneau() for a in self.acces]

    def etatPlaces(self):
        """:return: une ligne par place : identifiant, dimensions, état (list de str)"""
        lignes = []
        for place in self.parking.mesPlaces:
            etat = "libre" if place.estLibre else "occupée"
            lignes.append(f"{place.idPlace:4} {place.longueur:.2f} m x {place.hauteur:.2f} m   {etat}")
        return lignes
