"""
Tests du use case « Reprendre la voiture » (Partie 2).

Les méthodes testées ici sont écrites par Mohamed dans le modèle :
Parking.retrouverPlacement, Teleporteur.ramenerVoiture,
Acces.lancerProcedureSortie et Acces.lancerProcedureSortieSuperAbonne
(voir Partie2_Repartition.md). Tant qu'elles n'existent pas, les classes
de test sont sautées (skipUnless) ; elles s'activent toutes seules ensuite.
"""

import unittest

from modele.parking import Parking, Place, Placement
from modele.client import Client, Voiture, Abonnement
from modele.acces import Acces, Teleporteur, PARTENAIRE

SORTIE_ECRITE = (hasattr(Parking, "retrouverPlacement")
                 and hasattr(Teleporteur, "ramenerVoiture")
                 and hasattr(Acces, "lancerProcedureSortie"))
SORTIE_SUPER_ECRITE = hasattr(Acces, "lancerProcedureSortieSuperAbonne")


class ContexteSortie(unittest.TestCase):
    """
    Contexte commun : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ;
    A3 : 1,60 m x 4,00 m), un accès, un client C non abonné dont la voiture V
    (1,80 m x 4,50 m, « AB-123-CD ») vient d'entrer : elle est en A1 et C a son ticket.
    """

    def setUp(self):
        """Crée le parking, l'accès, et fait entrer la voiture de C (ticket dans self.ticket)."""
        Parking._reinitialiser()
        self.parking = Parking(nbNiveaux=1)
        self.place1 = Place(1, "A", 5.00, 2.00)
        self.place2 = Place(2, "A", 5.00, 2.00)
        self.place3 = Place(3, "A", 4.00, 1.60)
        for place in (self.place1, self.place2, self.place3):
            self.parking.ajouterPlace(place)
        self.acces = Acces(self.parking)
        self.client = Client("Dupont", "1 rue du Taur, Toulouse")
        self.voiture = self.client.nouvelleVoiture("AB-123-CD", 1.80, 4.50)
        self.ticket = self.client.entrerParking(self.acces)

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def placementEnCours(self):
        """:return: le dernier placement de la voiture V"""
        return self.voiture.mesPlacements[-1]


@unittest.skipUnless(SORTIE_ECRITE, "Méthodes de sortie pas encore écrites dans le modèle")
class TestRetrouverPlacement(ContexteSortie):
    """Tests de Parking.retrouverPlacement(ticket)."""

    def test_retrouver_placement_ticket_valide(self):
        """Voiture garée en A1 : son ticket donne le bon placement."""
        self.assertIs(self.parking.retrouverPlacement(self.ticket), self.placementEnCours())

    def test_retrouver_placement_ticket_inconnu(self):
        """Ticket qui ne correspond à aucune voiture : None."""
        self.assertIsNone(self.parking.retrouverPlacement("Z9-XX000XX-0000"))

    def test_retrouver_placement_voiture_deja_sortie(self):
        """Ticket d'une voiture déjà partie : None."""
        self.placementEnCours().partirPlace()
        self.assertIsNone(self.parking.retrouverPlacement(self.ticket))


@unittest.skipUnless(SORTIE_ECRITE, "Méthodes de sortie pas encore écrites dans le modèle")
class TestRamenerVoiture(ContexteSortie):
    """Tests de Teleporteur.ramenerVoiture(placement)."""

    def test_ramener_voiture_libere_la_place(self):
        """La place est libérée et la voiture est hors du parking."""
        voiture = Teleporteur().ramenerVoiture(self.placementEnCours())
        self.assertIs(voiture, self.voiture)
        self.assertTrue(self.place1.estLibre)
        self.assertFalse(self.voiture.estDansParking)
        self.assertIsNone(self.voiture.lieuStationnement)


@unittest.skipUnless(SORTIE_ECRITE, "Méthodes de sortie pas encore écrites dans le modèle")
class TestLancerProcedureSortie(ContexteSortie):
    """Tests de Acces.lancerProcedureSortie(ticket)."""

    def test_sortie_avec_ticket_valide(self):
        """Ticket valide : la voiture est rendue et une place se libère. (RF04)"""
        avant = self.parking.nbPlacesLibres
        self.assertIs(self.acces.lancerProcedureSortie(self.ticket), self.voiture)
        self.assertEqual(self.parking.nbPlacesLibres, avant + 1)

    def test_sortie_met_a_jour_le_panneau(self):
        """Après la sortie, le panneau affiche une place de plus. (RF04)"""
        self.assertIn("2", self.acces.actionnerPanneau())
        self.acces.lancerProcedureSortie(self.ticket)
        self.assertIn("3", self.acces.actionnerPanneau())

    def test_sortie_ticket_invalide(self):
        """Ticket inventé : None, aucune place libérée."""
        avant = self.parking.nbPlacesLibres
        self.assertIsNone(self.acces.lancerProcedureSortie("A2-ZZ999ZZ-1200"))
        self.assertEqual(self.parking.nbPlacesLibres, avant)
        self.assertTrue(self.voiture.estDansParking)

    def test_sortie_deux_fois_meme_ticket(self):
        """Même ticket utilisé 2 fois : la voiture la 1re fois, None la 2e."""
        self.assertIs(self.acces.lancerProcedureSortie(self.ticket), self.voiture)
        self.assertIsNone(self.acces.lancerProcedureSortie(self.ticket))

    def test_sortie_conserve_historique(self):
        """Le placement terminé reste dans l'historique et n'est plus en cours. (RF09)"""
        placement = self.placementEnCours()
        self.acces.lancerProcedureSortie(self.ticket)
        self.assertIn(placement, self.parking.historiquePassages())
        self.assertFalse(placement.estEnCours)

    def test_nbFrequentations_apres_deux_passages(self):
        """Entrer, sortir, entrer, sortir : nbFrequentations vaut 2. (RF09)"""
        self.acces.lancerProcedureSortie(self.ticket)
        ticket2 = self.client.entrerParking(self.acces)
        self.acces.lancerProcedureSortie(ticket2)
        self.assertEqual(self.client.nbFrequentations, 2)


@unittest.skipUnless(SORTIE_SUPER_ECRITE, "Sortie du super-abonné pas encore écrite dans le modèle")
class TestSortieSuperAbonne(ContexteSortie):
    """Tests de Acces.lancerProcedureSortieSuperAbonne(client)."""

    def setUp(self):
        """Contexte commun, plus un super-abonné S dont la voiture (1,80 m x 4,50 m) est dehors."""
        super().setUp()
        self.superAbonne = Client("Martin", "2 allée Jean Jaurès, Toulouse")
        self.voitureS = self.superAbonne.nouvelleVoiture("SS-777-SS", 1.80, 4.50)
        self.superAbonne.sAbonner(Abonnement("Garantie", 60, True))

    def test_super_abonne_sortie_parking_partenaire(self):
        """Super-abonné garé au partenaire : voiture rendue, lieuStationnement repasse à None."""
        Placement(Voiture("XX-111-XX", 1.80, 4.50), self.place2)
        self.superAbonne.entrerParking(self.acces)
        self.assertEqual(self.voitureS.lieuStationnement, PARTENAIRE)
        self.assertIs(self.acces.lancerProcedureSortieSuperAbonne(self.superAbonne), self.voitureS)
        self.assertIsNone(self.voitureS.lieuStationnement)

    def test_super_abonne_sortie_place_dreampark(self):
        """Super-abonné garé en A2 : voiture rendue, A2 libre."""
        self.superAbonne.entrerParking(self.acces)
        self.assertEqual(self.voitureS.lieuStationnement, "A2")
        self.assertIs(self.acces.lancerProcedureSortieSuperAbonne(self.superAbonne), self.voitureS)
        self.assertTrue(self.place2.estLibre)
        self.assertFalse(self.voitureS.estDansParking)

    def test_super_abonne_pas_gare(self):
        """Super-abonné dont la voiture est dehors : None."""
        self.assertIsNone(self.acces.lancerProcedureSortieSuperAbonne(self.superAbonne))


if __name__ == '__main__':
    unittest.main()
