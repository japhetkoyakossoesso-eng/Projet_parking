
import unittest
from unittest.mock import Mock

from modele.client import Voiture
from modele.exceptions import VoitureDejaGareeError


class TestVoiture(unittest.TestCase):

    def setUp(self):
        self.voiture = Voiture(
            immatriculation="AB-123-CD",
            hauteur=1.80,
            longueur=4.50
                             )

    def test_creation_voiture(self):
        """Vérifie la création d'une voiture."""
        self.assertIsInstance(self.voiture, Voiture)

    def test_immatriculation(self):
        """Vérifie l'immatriculation."""
        self.assertEqual(self.voiture.immatriculation, "AB-123-CD")

    def test_hauteur(self):
        """Vérifie la hauteur."""
        self.assertEqual(self.voiture.hauteur, 1.80)

    def test_longueur(self):
        """Vérifie la longueur."""
        self.assertEqual(self.voiture.longueur, 4.50)

    def test_immatriculation_vide(self):
        """Une immatriculation vide doit provoquer une erreur."""
        with self.assertRaises(ValueError):
            Voiture("", 1.80, 4.50)

    def test_dimensions_nulles(self):
        """Les dimensions nulles sont interdites."""
        with self.assertRaises(ValueError):
            Voiture("AB-123-CD", 0, 4.50)

        with self.assertRaises(ValueError):
            Voiture("AB-123-CD", 1.80, 0)

    def test_dimensions_negatives(self):
        """Les dimensions négatives sont interdites."""
        with self.assertRaises(ValueError):
            Voiture("AB-123-CD", -1, 4.50)

        with self.assertRaises(ValueError):
            Voiture("AB-123-CD", 1.80, -4.50)

    def test_etat_initial(self):
        """Une voiture nouvellement créée n'est pas garée."""
        self.assertFalse(self.voiture.estDansParking)
        self.assertIsNone(self.voiture.lieuStationnement)
        self.assertEqual(self.voiture.mesPlacements, [])

    def test_ajouter_placement(self):
        """L'ajout d'un placement met à jour l'état de la voiture."""
        placement = Mock()
        placement.place.idPlace = "A1"

        self.voiture.addPlacementV(placement)

        self.assertTrue(self.voiture.estDansParking)
        self.assertEqual(self.voiture.lieuStationnement, "A1")
        self.assertEqual(len(self.voiture.mesPlacements), 1)
        self.assertIs(self.voiture.mesPlacements[0], placement)

    def test_voiture_deja_garee(self):
        """Une voiture déjà garée ne peut pas recevoir un autre placement."""
        placement1 = Mock()
        placement1.place.idPlace = "A1"

        placement2 = Mock()
        placement2.place.idPlace = "A2"

        self.voiture.addPlacementV(placement1)

        with self.assertRaises(VoitureDejaGareeError):
            self.voiture.addPlacementV(placement2)

        self.assertEqual(len(self.voiture.mesPlacements), 1)
        self.assertEqual(self.voiture.lieuStationnement, "A1")


if __name__ == "__main__":
    unittest.main()
