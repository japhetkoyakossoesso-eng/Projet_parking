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

    def seGarer(self, client, numAcces, modePaiement="CB", choixAbonnement=None):
        """
        Lance le use case « Se garer » par l'accès numAcces (1 ou 2).

        :return: (réussi, message) : réussi est un bool, message le ticket ou l'explication
        """
        acces = self.acces[numAcces - 1]
        resultat = acces.lancerProcedureEntree(client, modePaiement, choixAbonnement)
        if resultat == MESSAGE_PLEIN:
            return False, resultat
        if client.estSuperAbonne:
            return True, resultat
        return True, f"Ticket : {resultat}"

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
