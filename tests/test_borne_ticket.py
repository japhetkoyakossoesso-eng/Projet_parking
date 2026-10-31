
import unittest
from unittest.mock import Mock

from modele.borne_ticket import BorneTicket


class TestBorneTicket(unittest.TestCase):
    """Tests unitaires de la classe BorneTicket."""

    def setUp(self):
        self.borne = BorneTicket()

        self.client = Mock()
        self.client.estSuperAbonne = False

        self.client.maVoiture.immatriculation = "AB-123-CD"
        self.client.maVoiture.lieuStationnement = "A1"

        self.parking = Mock()

        abonnement_mensuel = Mock()
        abonnement_mensuel.libelle = "Mensuel"

        abonnement_garantie = Mock()
        abonnement_garantie.libelle = "Garantie"

        self.parking.mesAbonnements = [
            abonnement_mensuel,
            abonnement_garantie
                                      ]

    def test_delivrer_ticket_place_attribuee(self):
        ticket = self.borne.delivrerTicket(self.client)

        self.assertIsNotNone(ticket)
        self.assertTrue(len(ticket) > 0)

    def test_delivrer_ticket_sans_place(self):
        self.client.maVoiture.lieuStationnement = None

        ticket = self.borne.delivrerTicket(self.client)

        self.assertIsNone(ticket)

    def test_deux_clients_tickets_differents(self):
        client2 = Mock()
        client2.maVoiture.immatriculation = "CD-456-EF"
        client2.maVoiture.lieuStationnement = "A2"

        ticket1 = self.borne.delivrerTicket(self.client)
        ticket2 = self.borne.delivrerTicket(client2)

        self.assertNotEqual(ticket1, ticket2)

    def test_ticket_contient_place_et_immatriculation(self):
        ticket = self.borne.delivrerTicket(self.client)

        self.assertIn("A1", ticket)
        self.assertIn("AB-123-CD", ticket)

    def test_recuperer_infos_super_abonne(self):
        self.client.estSuperAbonne = True

        resultat = self.borne.recupererInfosCarte(self.client)

        self.assertIn("super", resultat.lower())

    def test_recuperer_infos_client_sans_carte(self):
        self.client.estSuperAbonne = False

        resultat = self.borne.recupererInfosCarte(self.client)

        self.assertEqual(resultat, "")

    def test_proposer_services(self):
        resultat = self.borne.proposerServices()

        self.assertIn("maintenance", resultat.lower())
        self.assertIn("entretien", resultat.lower())
        self.assertIn("livraison", resultat.lower())

    def test_proposer_abonnements(self):
        resultat = self.borne.proposerAbonnements(
            self.client,
            self.parking
        )

        self.assertIn("Mensuel", resultat)
        self.assertIn("Garantie", resultat)

    def test_proposer_type_paiement(self):
        resultat = self.borne.proposerTypePaiement()

        self.assertIn("CB", resultat)
        self.assertIn("espèces", resultat.lower())


if __name__ == "__main__":
    unittest.main()
