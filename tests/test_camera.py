
import unittest
from unittest.mock import Mock

from modele.camera import Camera


class TestCamera(unittest.TestCase):

    def setUp(self):
        self.camera = Camera()

        self.voiture = Mock()
        self.voiture.hauteur = 1.80
        self.voiture.longueur = 4.50
        self.voiture.immatriculation = "AB-123-CD"

    def test_capturer_hauteur(self):
        resultat = self.camera.capturerHauteur(self.voiture)

        self.assertEqual(resultat, 1.80)

    def test_capturer_longueur(self):
        resultat = self.camera.capturerLongueur(self.voiture)

        self.assertEqual(resultat, 4.50)

    def test_capturer_immatriculation(self):
        resultat = self.camera.capturerImmatr(self.voiture)

        self.assertEqual(resultat, "AB-123-CD")

    def test_immatriculation_vide(self):
        self.voiture.immatriculation = ""

        with self.assertRaises(ValueError):
            self.camera.capturerImmatr(self.voiture)

    def test_immatriculation_illisible(self):
        self.voiture.immatriculation = "   "

        with self.assertRaises(ValueError):
            self.camera.capturerImmatr(self.voiture)


if __name__ == "__main__":
    unittest.main()
