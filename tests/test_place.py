
import unittest

from modele.client import Voiture
from modele.parking import Place


class TestPlace(unittest.TestCase):

    def setUp(self):
        self.place = Place(1, "A", 5.00, 2.00)

    def test_identifiant_place(self):
        self.assertEqual(self.place.idPlace, "A1")

    def test_place_initialement_libre(self):
        self.assertTrue(self.place.estLibre)

    def test_dimensions_exactes_acceptees(self):
        voiture = Voiture("AA-111-AA", 2.00, 5.00)

        self.assertTrue(self.place.estCompatible(voiture))

    def test_dimensions_inferieures_acceptees(self):
        voiture = Voiture("BB-222-BB", 1.50, 4.00)

        self.assertTrue(self.place.estCompatible(voiture))

    def test_hauteur_superieure_refusee(self):
        voiture = Voiture("CC-333-CC", 2.10, 4.00)

        self.assertFalse(self.place.estCompatible(voiture))

    def test_longueur_superieure_refusee(self):
        voiture = Voiture("DD-444-DD", 1.50, 5.50)

        self.assertFalse(self.place.estCompatible(voiture))

    def test_place_refuse_dimensions_nulles(self):
        with self.assertRaises(ValueError):
            Place(4, "A", 0, 2.00)

    def test_dimensions_place(self):
        self.assertEqual(self.place.longueur, 5.00)
        self.assertEqual(self.place.hauteur, 2.00)


if __name__ == "__main__":
    unittest.main()
