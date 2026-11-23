"""
Tests d'intégration du contrôleur : le use case « Se garer » de bout en bout,
sans passer par le clavier.
"""

import unittest
from datetime import date

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
        self.assertTrue(message.startswith("Aucune place disponible pour votre véhicule"))
        self.assertEqual(self.ctrl.lieu(client), "hors du parking")

    def test_super_abonne_parking_plein_va_au_partenaire(self):
        for i in range(2):
            self.ctrl.seGarer(self.ctrl.nouveauClient(f"G{i}", "x", f"GG-{i}", 2.40, 5.90), 1)
        client = self.ctrl.nouveauClient("Sam", "Albi", "SS-111-SS", 2.40, 5.90)
        self.ctrl.sAbonner(client, self.ctrl.abonnements[1])
        reussi, _ = self.ctrl.seGarer(client, 1)
        self.assertTrue(reussi)
        self.assertEqual(self.ctrl.lieu(client), "parking partenaire")

    def test_raison_voiture_trop_haute(self):
        client = self.ctrl.nouveauClient("Faess", "x", "FF-111-FF", 3.00, 3.00)
        self.assertIn("trop haute", self.ctrl.raisonRefus(client))

    def test_raison_voiture_trop_longue(self):
        client = self.ctrl.nouveauClient("Long", "x", "LL-111-LL", 1.50, 7.00)
        self.assertIn("trop longue", self.ctrl.raisonRefus(client))

    def test_raison_places_compatibles_occupees(self):
        for i in range(2):
            self.ctrl.seGarer(self.ctrl.nouveauClient(f"G{i}", "x", f"GG-{i}", 2.40, 5.90), 1)
        client = self.ctrl.nouveauClient("Maris", "x", "MM-111-MM", 2.30, 3.00)
        raison = self.ctrl.raisonRefus(client)
        self.assertIn("A5", raison)
        self.assertIn("B5", raison)
        reussi, message = self.ctrl.seGarer(client, 1)
        self.assertFalse(reussi)
        self.assertIn(raison, message)

    def test_pas_de_raison_si_une_place_convient(self):
        client = self.ctrl.nouveauClient("Alice", "Toulouse", "AB-123-CD", 1.80, 4.50)
        self.assertIsNone(self.ctrl.raisonRefus(client))

    def test_ticket_affiche_si_pack_garantie_pris_a_la_borne(self):
        client = self.ctrl.nouveauClient("Tim", "x", "ZE-257-FG", 2.00, 4.00)
        reussi, message = self.ctrl.seGarer(client, 1, "CB", self.ctrl.abonnements[1])
        self.assertTrue(reussi)
        self.assertTrue(message.startswith("Ticket : "))

    def test_super_abonne_desabonne_recupere_voiture_au_partenaire(self):
        """Super-abonné garé au partenaire puis désabonné : il récupère sa voiture sans ticket."""
        for i in range(2):
            self.ctrl.seGarer(self.ctrl.nouveauClient(f"G{i}", "x", f"GG-{i}", 2.40, 5.90), 1)
        client = self.ctrl.nouveauClient("Sam", "Albi", "SS-111-SS", 2.40, 5.90)
        self.ctrl.sAbonner(client, self.ctrl.abonnements[1])
        self.ctrl.seGarer(client, 1)
        client.seDesabonner()
        reussi, _ = self.ctrl.sortir(client, 1)
        self.assertTrue(reussi)
        self.assertEqual(self.ctrl.lieu(client), "hors du parking")

    def test_realiser_maintenance_regare_la_voiture(self):
        """Maintenance en attente : réalisée, la voiture est regarée."""
        client = self.ctrl.nouveauClient("Alice", "Toulouse", "AB-123-CD", 1.80, 4.50)
        self.ctrl.seGarer(client, 1, "CB", self.ctrl.abonnements[0])
        self.ctrl.demanderService(client, "maintenance")
        messages = self.ctrl.realiserServices(client)
        self.assertEqual(len(messages), 1)
        self.assertEqual(self.ctrl.servicesEnAttente(client), [])
        self.assertTrue(client.maVoiture.estDansParking)

    def test_realiser_livraison_sort_la_voiture(self):
        """Livraison en attente : réalisée, la place est libérée."""
        client = self.ctrl.nouveauClient("Alice", "Toulouse", "AB-123-CD", 1.80, 4.50)
        self.ctrl.seGarer(client, 1, "CB", self.ctrl.abonnements[0])
        self.ctrl.demanderService(client, "livraison", date(2026, 12, 1), 18, "Cinéma ABC")
        self.ctrl.realiserServices(client)
        self.assertFalse(client.maVoiture.estDansParking)
        self.assertEqual(self.ctrl.servicesEnAttente(client), [])

    def test_maintenance_impossible_voiture_dehors(self):
        """Maintenance demandée mais voiture hors du parking : non réalisée."""
        client = self.ctrl.nouveauClient("Alice", "Toulouse", "AB-123-CD", 1.80, 4.50)
        self.ctrl.sAbonner(client, self.ctrl.abonnements[0])
        self.ctrl.demanderService(client, "maintenance")
        messages = self.ctrl.realiserServices(client)
        self.assertIn("impossible", messages[0])
        self.assertFalse(client.maVoiture.estDansParking)
        self.assertEqual(len(self.ctrl.servicesEnAttente(client)), 1)

    def test_voiture_deja_garee(self):
        client = self.ctrl.nouveauClient("Alice", "Toulouse", "AB-123-CD", 1.80, 4.50)
        self.ctrl.seGarer(client, 1)
        self.assertTrue(self.ctrl.estDejaGare(client))


if __name__ == "__main__":
    unittest.main()
