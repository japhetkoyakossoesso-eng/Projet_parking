"""
Tests des classes Client, Voiture, Abonnement et Contrat (spécification §8.3, §8.5 et §8.6).

Partie 2 : tests écrits à partir des docstrings de la Partie 0.
"""

import unittest
from datetime import date

from modele.parking import Parking, Place, Placement
from modele.client import Client, Voiture, Abonnement, Contrat
from modele.services import Maintenance, Entretien, Livraison
from modele.acces import Acces, MESSAGE_PLEIN
from modele.exceptions import VoitureDejaGareeError


class ContexteParking(unittest.TestCase):
    """
    Contexte commun : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ;
    A3 : 1,60 m x 4,00 m), voiture V de 1,80 m x 4,50 m (« AB-123-CD »),
    client C non abonné, formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""
        Parking._reinitialiser()
        self.parking = Parking(nbNiveaux=1)
        self.place1 = Place(1, "A", 5.00, 2.00)
        self.place2 = Place(2, "A", 5.00, 2.00)
        self.place3 = Place(3, "A", 4.00, 1.60)
        for place in (self.place1, self.place2, self.place3):
            self.parking.ajouterPlace(place)
        self.client = Client("Dupont", "1 rue du Taur, Toulouse")
        self.voiture = self.client.nouvelleVoiture("AB-123-CD", 1.80, 4.50)
        self.mensuel = Abonnement("Mensuel", 30, False)
        self.garantie = Abonnement("Garantie", 60, True)
        self.parking.addAbonnement(self.mensuel)
        self.parking.addAbonnement(self.garantie)

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()


class TestVoiture(ContexteParking):
    """Tests de la classe Voiture."""

    def test_addPlacementV_voiture_hors_parking(self):
        """La voiture entre : estDansParking devient vrai. (RF04)"""
        Placement(self.voiture, self.place1)
        self.assertTrue(self.voiture.estDansParking)

    def test_addPlacementV_voiture_deja_garee(self):
        """Voiture déjà garée : lève VoitureDejaGareeError. (RF03)"""
        placement = Placement(self.voiture, self.place1)
        with self.assertRaises(VoitureDejaGareeError):
            self.voiture.addPlacementV(placement)

    def test_constructeur_immatriculation_vide(self):
        """Une immatriculation vide lève ValueError. (RF01)"""
        with self.assertRaises(ValueError):
            Voiture("", 1.80, 4.50)


class TestClient(ContexteParking):
    """Tests de la classe Client."""

    def test_nouvelleVoiture_valide(self):
        """maVoiture a la bonne immatriculation."""
        self.assertEqual(self.client.maVoiture.immatriculation, "AB-123-CD")

    def test_nouvelleVoiture_longueur_negative(self):
        """Une longueur négative lève ValueError."""
        with self.assertRaises(ValueError):
            self.client.nouvelleVoiture("EF-456-GH", 1.80, -4.50)

    def test_sAbonner_mensuel(self):
        """Formule « Mensuel » : estAbonne vrai, estSuperAbonne faux. (RF12)"""
        self.client.sAbonner(self.mensuel)
        self.assertTrue(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)

    def test_sAbonner_garantie(self):
        """Formule « Garantie » : estAbonne et estSuperAbonne vrais. (RF07)"""
        self.client.sAbonner(self.garantie)
        self.assertTrue(self.client.estAbonne)
        self.assertTrue(self.client.estSuperAbonne)

    def test_sAbonner_deja_abonne(self):
        """Nouvelle formule : l'ancien contrat est rompu, un seul contrat en cours. (RF12)"""
        ancien = self.client.sAbonner(self.mensuel)
        self.client.sAbonner(self.garantie)
        nbContratsEnCours = sum(1 for c in self.client.mesContrats if c.estEnCours)
        self.assertEqual(nbContratsEnCours, 1)
        self.assertFalse(ancien.estEnCours)

    def test_seDesabonner_client_abonne(self):
        """Après seDesabonner(), estAbonne est faux. (RF12)"""
        self.client.sAbonner(self.mensuel)
        self.client.seDesabonner()
        self.assertFalse(self.client.estAbonne)

    def test_seDesabonner_client_non_abonne(self):
        """Client non abonné : renvoie False. (RF12)"""
        self.assertFalse(self.client.seDesabonner())

    def test_demanderMaintenance_abonne(self):
        """Client abonné : une Maintenance est ajoutée à mesServices. (RF06)"""
        self.client.sAbonner(self.mensuel)
        service = self.client.demanderMaintenance()
        self.assertIsInstance(service, Maintenance)
        self.assertIn(service, self.client.mesServices)

    def test_demanderMaintenance_non_abonne(self):
        """Client non abonné : renvoie False, aucun service ajouté. (RF06)"""
        self.assertFalse(self.client.demanderMaintenance())
        self.assertEqual(len(self.client.mesServices), 0)

    def test_demanderEntretien_abonne(self):
        """Client abonné : un Entretien est ajouté à mesServices. (RF06)"""
        self.client.sAbonner(self.mensuel)
        service = self.client.demanderEntretien()
        self.assertIsInstance(service, Entretien)
        self.assertIn(service, self.client.mesServices)

    def test_demanderEntretien_non_abonne(self):
        """Client non abonné : renvoie False. (RF06)"""
        self.assertFalse(self.client.demanderEntretien())

    def test_demanderLivraison_abonne(self):
        """Livraison enregistrée avec date, heure et adresse. (RF08)"""
        self.client.sAbonner(self.mensuel)
        jour = date(2026, 12, 1)
        livraison = self.client.demanderLivraison(jour, 18, "Cinéma ABC, Toulouse")
        self.assertIsInstance(livraison, Livraison)
        self.assertEqual(livraison.dateLivraison, jour)
        self.assertEqual(livraison.heure, 18)
        self.assertEqual(livraison.adresse, "Cinéma ABC, Toulouse")

    def test_demanderLivraison_remplace_demande(self):
        """Une deuxième demande avant exécution remplace l'adresse. (RF13)"""
        self.client.sAbonner(self.mensuel)
        jour = date(2026, 12, 1)
        premiere = self.client.demanderLivraison(jour, 18, "Cinéma ABC, Toulouse")
        nouvelleAdr = "Gare Matabiau, Toulouse"
        livraison = self.client.demanderLivraison(jour, 20, nouvelleAdr)
        self.assertIs(livraison, premiere)
        self.assertEqual(livraison.adresse, nouvelleAdr)
        self.assertEqual(livraison.heure, 20)
        self.assertEqual(len(self.client.mesServices), 1)

    def test_demanderLivraison_heures_limites_valides(self):
        """Heure 0 puis 23 : livraison enregistrée. (RF08, valeurs limites)"""
        self.client.sAbonner(self.mensuel)
        jour = date(2026, 12, 1)
        self.assertEqual(self.client.demanderLivraison(jour, 0, "Capitole").heure, 0)
        self.assertEqual(self.client.demanderLivraison(jour, 23, "Capitole").heure, 23)

    def test_demanderLivraison_heures_hors_bornes(self):
        """Heure -1 puis 24 : lève ValueError. (RF08, valeurs limites)"""
        self.client.sAbonner(self.mensuel)
        jour = date(2026, 12, 1)
        with self.assertRaises(ValueError):
            self.client.demanderLivraison(jour, -1, "Capitole")
        with self.assertRaises(ValueError):
            self.client.demanderLivraison(jour, 24, "Capitole")

    def test_demanderLivraison_adresse_vide(self):
        """Adresse vide : lève ValueError. (RF08)"""
        self.client.sAbonner(self.mensuel)
        with self.assertRaises(ValueError):
            self.client.demanderLivraison(date(2026, 12, 1), 18, "")

    def test_entrerParking_place_disponible(self):
        """Place disponible : renvoie un ticket. (RF05)"""
        ticket = self.client.entrerParking(Acces(self.parking))
        self.assertIsNotNone(ticket)
        self.assertTrue(ticket.startswith("A1-AB123CD-"))

    def test_entrerParking_parking_plein(self):
        """Parking plein : renvoie « Aucune place disponible pour votre véhicule ». (RF03)"""
        Placement(Voiture("XX-111-XX", 1.80, 4.50), self.place1)
        Placement(Voiture("YY-222-YY", 1.80, 4.50), self.place2)
        resultat = self.client.entrerParking(Acces(self.parking))
        self.assertEqual(resultat, MESSAGE_PLEIN)
        self.assertFalse(self.voiture.estDansParking)

    def test_nbFrequentations(self):
        """Deux entrées et deux sorties : nbFrequentations vaut 2. (RF09)"""
        Placement(self.voiture, self.place1).partirPlace()
        Placement(self.voiture, self.place2).partirPlace()
        self.assertEqual(self.client.nbFrequentations, 2)


class TestAbonnement(ContexteParking):
    """Tests de la classe Abonnement."""

    def test_addContrat(self):
        """Le contrat est rattaché à l'abonnement. (RF12)"""
        contrat = self.client.sAbonner(self.mensuel)
        self.assertIn(contrat, self.mensuel.mesContrats)


class TestContrat(ContexteParking):
    """Tests de la classe Contrat."""

    def test_creation(self):
        """dateDebut vaut aujourd'hui et le contrat est en cours. (RF12)"""
        contrat = Contrat(self.client, self.mensuel)
        self.assertEqual(contrat.dateDebut.date(), date.today())
        self.assertTrue(contrat.estEnCours)

    def test_rompreContrat_en_cours(self):
        """dateFin renseignée, estEnCours faux. (RF12)"""
        contrat = Contrat(self.client, self.mensuel)
        self.assertTrue(contrat.rompreContrat())
        self.assertIsNotNone(contrat.dateFin)
        self.assertFalse(contrat.estEnCours)

    def test_rompreContrat_deja_rompu(self):
        """Contrat déjà rompu : aucun effet, renvoie False."""
        contrat = Contrat(self.client, self.mensuel)
        contrat.rompreContrat()
        dateFin = contrat.dateFin
        self.assertFalse(contrat.rompreContrat())
        self.assertEqual(contrat.dateFin, dateFin)


if __name__ == '__main__':
    unittest.main()
