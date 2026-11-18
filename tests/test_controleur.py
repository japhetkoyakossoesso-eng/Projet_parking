"""
Tests d'intégration du contrôleur : le use case « Se garer » de bout en bout,
sans passer par le clavier.
"""

import unittest

from controleur.controleur_parking import ControleurParking
from modele.parking import Parking


class TestControleurSeGarer(unittest.TestCase):
    """Parking de démonstration : 10 places, dont 2 grandes (A5 et B5, 6.00 m x 2.50 m)."""

    def setUp(self):
        Parking._reinitialiser()
        self.ctrl = ControleurParking()

    def tearDown(self):
        Parking._reinitialiser()

    def test_non_abonne_recoit_un_ticket(self):
        client = self.ctrl.nouveauClient("Alice", "Toulouse", "AB-123-CD", 1.80, 4.50)
        reussi, message = self.ctrl.seGarer(client, 1)
        self.assertTrue(reussi)
        self.assertTrue(message.startswith("Ticket : "))
        self.assertEqual(self.ctrl.lieu(client), "place A1")
        self.assertIn("9", self.ctrl.panneaux()[0])

    def test_non_abonne_prend_un_abonnement_a_la_borne(self):
        client = self.ctrl.nouveauClient("Alice", "Toulouse", "AB-123-CD", 1.80, 4.50)
        self.ctrl.seGarer(client, 1, "espèces", self.ctrl.abonnements[0])
        self.assertEqual(self.ctrl.statut(client), "abonné")

    def test_parking_plein_pour_une_grande_voiture(self):
        for i in range(2):
            self.ctrl.seGarer(self.ctrl.nouveauClient(f"G{i}", "x", f"GG-{i}", 2.40, 5.90), 1)
        client = self.ctrl.nouveauClient("Bob", "Paris", "CD-456-EF", 2.40, 5.90)
        reussi, message = self.ctrl.seGarer(client, 2)
        self.assertFalse(reussi)
        self.assertEqual(message, "Aucune place disponible pour votre véhicule")
        self.assertEqual(self.ctrl.lieu(client), "hors du parking")

    def test_super_abonne_parking_plein_va_au_partenaire(self):
        for i in range(2):
            self.ctrl.seGarer(self.ctrl.nouveauClient(f"G{i}", "x", f"GG-{i}", 2.40, 5.90), 1)
        client = self.ctrl.nouveauClient("Sam", "Albi", "SS-111-SS", 2.40, 5.90)
        self.ctrl.sAbonner(client, self.ctrl.abonnements[1])
        reussi, _ = self.ctrl.seGarer(client, 1)
        self.assertTrue(reussi)
        self.assertEqual(self.ctrl.lieu(client), "parking partenaire")

    def test_voiture_deja_garee(self):
        client = self.ctrl.nouveauClient("Alice", "Toulouse", "AB-123-CD", 1.80, 4.50)
        self.ctrl.seGarer(client, 1)
        self.assertTrue(self.ctrl.estDejaGare(client))


if __name__ == "__main__":
    unittest.main()
