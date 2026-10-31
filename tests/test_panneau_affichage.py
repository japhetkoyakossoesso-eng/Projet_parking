
import unittest

from modele.parking import Parking, Place, Placement
from modele.client import Voiture
from modele.panneau_affichage import PanneauAffichage


class TestPanneauAffichage(unittest.TestCase):
    """Tests unitaires de la classe PanneauAffichage."""

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

        self.panneau = PanneauAffichage()

    def tearDown(self):
        Parking._reinitialiser()

    def test_afficher_parking_vide(self):
        """Le panneau indique trois places disponibles."""

        resultat = self.panneau.afficherNbPlacesDisponibles(
            self.parking
                                                           )

        self.assertIn("3", resultat)

    def test_afficher_apres_une_entree(self):
        """Le panneau indique deux places disponibles."""

        voiture = Voiture("AB-123-CD", 1.80, 4.50)
        Placement(voiture, self.place1)

        resultat = self.panneau.afficherNbPlacesDisponibles(
            self.parking
                                                           )

        self.assertIn("2", resultat)

    def test_afficher_parking_plein(self):
        """Le panneau indique zéro place disponible."""

        voiture1 = Voiture("AB-123-CD", 1.80, 4.50)
        voiture2 = Voiture("CD-456-EF", 1.80, 4.50)
        voiture3 = Voiture("GH-789-IJ", 1.50, 3.50)

        Placement(voiture1, self.place1)
        Placement(voiture2, self.place2)
        Placement(voiture3, self.place3)

        resultat = self.panneau.afficherNbPlacesDisponibles(
            self.parking
        )

        self.assertIn("0", resultat)


if __name__ == "__main__":
    unittest.main()
