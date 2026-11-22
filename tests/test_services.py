"""
Tests des classes Maintenance, Entretien, Livraison et Voiturier (spécification §8.7 et §8.8).

Partie 2 : tests écrits à partir des docstrings de la Partie 0.
"""

import unittest
from datetime import date

from modele.parking import Parking, Place, Placement
from modele.client import Client, Abonnement
from modele.services import Maintenance, Entretien, Livraison, Voiturier
from modele.exceptions import LivraisonSansDemandeError


class ContexteServices(unittest.TestCase):
    """
    Contexte commun : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ;
    A3 : 1,60 m x 4,00 m), client C abonné « Mensuel » dont la voiture V
    (1,80 m x 4,50 m, « AB-123-CD ») est garée en A1.
    """

    def setUp(self):
        """Crée le parking, ses trois places, le client abonné et gare sa voiture en A1."""
        Parking._reinitialiser()
        self.parking = Parking(nbNiveaux=1)
        self.place1 = Place(1, "A", 5.00, 2.00)
        self.place2 = Place(2, "A", 5.00, 2.00)
        self.place3 = Place(3, "A", 4.00, 1.60)
        for place in (self.place1, self.place2, self.place3):
            self.parking.ajouterPlace(place)
        self.client = Client("Dupont", "1 rue du Taur, Toulouse")
        self.voiture = self.client.nouvelleVoiture("AB-123-CD", 1.80, 4.50)
        self.client.sAbonner(Abonnement("Mensuel", 30, False))
        self.placement = Placement(self.voiture, self.place1)

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()


class TestMaintenance(ContexteServices):
    """Tests de la classe Maintenance."""

    def test_creation_date_demande(self):
        """dateDemande vaut aujourd'hui. (RF09)"""
        maintenance = Maintenance(self.voiture)
        self.assertEqual(maintenance.dateDemande.date(), date.today())
        self.assertFalse(maintenance.estEffectue)

    def test_effectuerMaintenance(self):
        """dateService et rapport renseignés, voiture regarée (nouveau placement). (RF06)"""
        maintenance = self.client.demanderMaintenance()
        maintenance.effectuerMaintenance()
        self.assertIsNotNone(maintenance.dateService)
        self.assertIn("Maintenance", maintenance.rapport)
        self.assertTrue(self.voiture.estDansParking)
        self.assertFalse(self.placement.estEnCours)
        self.assertEqual(len(self.voiture.mesPlacements), 2)


class TestEntretien(ContexteServices):
    """Tests de la classe Entretien."""

    def test_effectuerEntretien(self):
        """dateService et rapport renseignés, voiture regarée. (RF06)"""
        entretien = self.client.demanderEntretien()
        entretien.effectuerEntretien()
        self.assertIsNotNone(entretien.dateService)
        self.assertIn("Entretien", entretien.rapport)
        self.assertTrue(self.voiture.estDansParking)
        self.assertEqual(len(self.voiture.mesPlacements), 2)


class TestLivraison(ContexteServices):
    """Tests de la classe Livraison."""

    def test_effectuerLivraison(self):
        """Le voiturier est appelé, la place est libérée, la voiture est hors du parking. (RF08)"""
        livraison = self.client.demanderLivraison(date(2026, 12, 1), 18, "Cinéma ABC")
        livraison.effectuerLivraison()
        self.assertFalse(self.voiture.estDansParking)
        self.assertTrue(self.place1.estLibre)
        self.assertTrue(livraison.estEffectue)


class TestVoiturier(ContexteServices):
    """Tests de la classe Voiturier."""

    def test_livrerVoiture_avec_demande(self):
        """Une demande existe : livraison effectuée à la bonne date et heure. (RF08)"""
        voiturier = Voiturier(7)
        jour = date(2026, 12, 1)
        livraison = Livraison(self.voiture, jour, 18, "Cinéma ABC", voiturier)
        voiturier.livrerVoiture(self.voiture, jour, 18)
        self.assertEqual(livraison.dateLivraison, jour)
        self.assertEqual(livraison.heure, 18)
        self.assertIn(f"le {jour} à 18h", livraison.rapport)
        self.assertIn("voiturier 7", livraison.rapport)

    def test_livrerVoiture_sans_demande(self):
        """Aucune demande : lève LivraisonSansDemandeError. (RF08)"""
        with self.assertRaises(LivraisonSansDemandeError):
            Voiturier(7).livrerVoiture(self.voiture, date(2026, 12, 1), 18)


if __name__ == '__main__':
    unittest.main()
