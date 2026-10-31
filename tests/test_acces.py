
import unittest
from unittest.mock import Mock

from modele.acces import Acces
from modele.parking import Parking, Place
from modele.client import Voiture


class TestAcces(unittest.TestCase):
    """
    Tests d'intégration de la classe Acces.

    Le contexte comporte un parking de trois places :
    A1 et A2 : 2.00 m de haut et 5.00 m de long.
    A3 : 1.60 m de haut et 4.00 m de long.

    La voiture de test mesure 1.80 m x 4.50 m.
    """

    def setUp(self):
        Parking._reinitialiser()

        self.parking = Parking(
            nbNiveaux=1,
            nbPlacesParNiveau=0
        )

        self.place1 = Place(1, "A", 5.00, 2.00)
        self.place2 = Place(2, "A", 5.00, 2.00)
        self.place3 = Place(3, "A", 4.00, 1.60)

        self.parking.ajouterPlace(self.place1)
        self.parking.ajouterPlace(self.place2)
        self.parking.ajouterPlace(self.place3)

        # Création des composants simulés
        self.camera = Mock()
        self.borne = Mock()
        self.panneau = Mock()
        self.teleporteur_entree = Mock()
        self.teleporteur_sortie = Mock()

        # Configuration de la caméra
        self.camera.capturerHauteur.return_value = 1.80
        self.camera.capturerLongueur.return_value = 4.50
        self.camera.capturerImmatr.return_value = "AB-123-CD"

        # Configuration de la borne
        self.borne.delivrerTicket.return_value = "A1-AB123CD-0930"
        self.borne.recupererInfosCarte.return_value = ""

        # Création de l'accès sans imposer un constructeur
        # qui n'est pas précisé dans le diagramme.
        self.acces = Acces.__new__(Acces)

        # Composants associés à l'accès
        self.acces.camera = self.camera
        self.acces.borneTicket = self.borne
        self.acces.panneauAffichage = self.panneau
        self.acces.TelEntree = self.teleporteur_entree
        self.acces.TelSortie = self.teleporteur_sortie

        # Parking associé à l'accès
        self.acces.parking = self.parking

        self.client = Mock()
        self.client.maVoiture = Voiture(
            "AB-123-CD",
            1.80,
            4.50
        )
        self.client.estAbonne = False
        self.client.estSuperAbonne = False

    def tearDown(self):
        Parking._reinitialiser()

    def test_actionner_camera(self):
        """La caméra récupère les informations de la voiture."""

        voiture = self.acces.actionnerCamera(self.client)

        self.assertIsNotNone(voiture)
        self.assertEqual(voiture.immatriculation, "AB-123-CD")
        self.assertEqual(voiture.hauteur, 1.80)
        self.assertEqual(voiture.longueur, 4.50)

        self.camera.capturerHauteur.assert_called_once()
        self.camera.capturerLongueur.assert_called_once()
        self.camera.capturerImmatr.assert_called_once()

    def test_actionner_panneau(self):
        """Le panneau affiche le nombre de places disponibles."""

        self.panneau.afficherNbPlacesDisponibles.return_value = "3"

        resultat = self.acces.actionnerPanneau()

        self.assertEqual(resultat, "3")
        self.panneau.afficherNbPlacesDisponibles.assert_called_once_with(
            self.parking
        )

    def test_entree_client_non_abonne(self):
        """
        Un client non abonné obtient un ticket
        et sa voiture est garée.
        """

        resultat = self.acces.lancerProcedureEntree(self.client)

        self.assertTrue(self.teleporteur_entree.teleporterVoiture.called)
        self.assertTrue(self.borne.delivrerTicket.called)

        self.assertIsNotNone(resultat)

    def test_entree_parking_plein(self):
        """
        Si aucune place ne convient, aucun ticket
        n'est délivré et la voiture n'entre pas.
        """

        self.place1 = Place(1, "A", 1.00, 1.00)
        self.place2 = Place(2, "A", 1.00, 1.00)
        self.place3 = Place(3, "A", 1.00, 1.00)

        # Remplacement des places du parking
        self.parking = Parking._reinitialiser()
        self.parking = Parking(
            nbNiveaux=1,
            nbPlacesParNiveau=0
        )

        self.parking.ajouterPlace(self.place1)
        self.parking.ajouterPlace(self.place2)
        self.parking.ajouterPlace(self.place3)

        self.acces.parking = self.parking

        resultat = self.acces.lancerProcedureEntree(self.client)

        self.assertEqual(
            resultat,
            "Aucune place disponible pour votre véhicule"
        )

        self.borne.delivrerTicket.assert_not_called()
        self.teleporteur_entree.teleporterVoiture.assert_not_called()

    def test_entree_super_abonne_place_disponible(self):
        """
        Le super-abonné entre sans recevoir de ticket.
        """

        self.client.estSuperAbonne = True
        self.borne.recupererInfosCarte.return_value = "super"

        resultat = self.acces.lancerProcedureEntree(self.client)

        self.assertTrue(
            self.teleporteur_entree.teleporterVoitureSuperAbonne.called
        )

        self.borne.delivrerTicket.assert_not_called()

    def test_entree_super_abonne_parking_plein(self):
        """
        Un super-abonné obtient une solution de stationnement
        même lorsque DreamPark est plein.
        """

        self.client.estSuperAbonne = True
        self.borne.recupererInfosCarte.return_value = "super"

        self.place1 = Place(1, "A", 1.00, 1.00)
        self.place2 = Place(2, "A", 1.00, 1.00)
        self.place3 = Place(3, "A", 1.00, 1.00)

        Parking._reinitialiser()
        self.parking = Parking(
            nbNiveaux=1,
            nbPlacesParNiveau=0
        )

        self.parking.ajouterPlace(self.place1)
        self.parking.ajouterPlace(self.place2)
        self.parking.ajouterPlace(self.place3)

        self.acces.parking = self.parking

        resultat = self.acces.lancerProcedureEntree(self.client)

        self.assertTrue(
            self.teleporteur_entree.teleporterVoitureSuperAbonne.called
        )

        self.borne.delivrerTicket.assert_not_called()

        self.assertNotEqual(
            resultat,
            "Aucune place disponible pour votre véhicule"
        )


if __name__ == "__main__":
    unittest.main()
