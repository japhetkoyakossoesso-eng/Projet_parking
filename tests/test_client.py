"""
Tests des classes Client, Voiture, Abonnement et Contrat (spécification §8.3, §8.5 et §8.6).

Partie 0 : chaque test est spécifié par son docstring (cas testé,
résultat attendu, assertion prévue). Le code des tests sera écrit en Partie 1,
d'ici là les classes sont marquées @unittest.skip.
"""

import unittest

from modele.parking import Parking
from modele.client import Client, Voiture, Abonnement, Contrat
from modele.services import Maintenance, Entretien, Livraison
from modele.exceptions import VoitureDejaGareeError


@unittest.skip("Partie 0 : spécification seulement")
class TestVoiture(unittest.TestCase):
    """
    Tests de la classe Voiture.

    Contexte : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ; A3 : 1,60 m x 4,00 m),
    voiture V de 1,80 m x 4,50 m (« AB-123-CD »), client C non abonné,
    formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def test_addPlacementV_voiture_hors_parking(self):
        """
        La voiture entre : estDansParking devient vrai. (RF04)

        Assertion prévue : assertTrue
        """

    def test_addPlacementV_voiture_deja_garee(self):
        """
        Voiture déjà garée : lève VoitureDejaGareeError. (RF03)

        Assertion prévue : assertRaises(VoitureDejaGareeError)
        """

    def test_constructeur_immatriculation_vide(self):
        """
        Une immatriculation vide lève ValueError. (RF01)

        Assertion prévue : assertRaises(ValueError)
        """


@unittest.skip("Partie 0 : spécification seulement")
class TestClient(unittest.TestCase):
    """
    Tests de la classe Client.

    Contexte : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ; A3 : 1,60 m x 4,00 m),
    voiture V de 1,80 m x 4,50 m (« AB-123-CD »), client C non abonné,
    formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def test_nouvelleVoiture_valide(self):
        """
        maVoiture a la bonne immatriculation.

        Assertion prévue : assertEqual
        """

    def test_nouvelleVoiture_longueur_negative(self):
        """
        Une longueur négative lève ValueError.

        Assertion prévue : assertRaises(ValueError)
        """

    def test_sAbonner_mensuel(self):
        """
        Formule « Mensuel » : estAbonne vrai, estSuperAbonne faux. (RF12)

        Assertion prévue : assertTrue, assertFalse
        """

    def test_sAbonner_garantie(self):
        """
        Formule « Garantie » : estAbonne et estSuperAbonne vrais. (RF07)

        Assertion prévue : assertTrue x2
        """

    def test_sAbonner_deja_abonne(self):
        """
        Nouvelle formule : l'ancien contrat est rompu, un seul contrat en cours. (RF12)

        Assertion prévue : assertEqual(nbContratsEnCours, 1)
        """

    def test_seDesabonner_client_abonne(self):
        """
        Après seDesabonner(), estAbonne est faux. (RF12)

        Assertion prévue : assertFalse
        """

    def test_seDesabonner_client_non_abonne(self):
        """
        Client non abonné : renvoie False. (RF12)

        Assertion prévue : assertFalse
        """

    def test_demanderMaintenance_abonne(self):
        """
        Client abonné : une Maintenance est ajoutée à mesServices. (RF06)

        Assertion prévue : assertIsInstance(..., Maintenance)
        """

    def test_demanderMaintenance_non_abonne(self):
        """
        Client non abonné : renvoie False, aucun service ajouté. (RF06)

        Assertion prévue : assertFalse, assertEqual(len(mesServices), 0)
        """

    def test_demanderEntretien_abonne(self):
        """
        Client abonné : un Entretien est ajouté à mesServices. (RF06)

        Assertion prévue : assertIsInstance(..., Entretien)
        """

    def test_demanderEntretien_non_abonne(self):
        """
        Client non abonné : renvoie False. (RF06)

        Assertion prévue : assertFalse
        """

    def test_demanderLivraison_abonne(self):
        """
        Livraison enregistrée avec date, heure et adresse. (RF08)

        Assertion prévue : assertEqual x3
        """

    def test_demanderLivraison_remplace_demande(self):
        """
        Une deuxième demande avant exécution remplace l'adresse. (RF13)

        Assertion prévue : assertEqual(livraison.adresse, nouvelleAdr)
        """

    def test_demanderLivraison_heures_limites_valides(self):
        """
        Heure 0 puis 23 : livraison enregistrée. (RF08, valeurs limites)

        Assertion prévue : assertEqual
        """

    def test_demanderLivraison_heures_hors_bornes(self):
        """
        Heure -1 puis 24 : lève ValueError. (RF08, valeurs limites)

        Assertion prévue : assertRaises(ValueError)
        """

    def test_demanderLivraison_adresse_vide(self):
        """
        Adresse vide : lève ValueError. (RF08)

        Assertion prévue : assertRaises(ValueError)
        """

    def test_entrerParking_place_disponible(self):
        """
        Place disponible : renvoie un ticket. (RF05)

        Assertion prévue : assertIsNotNone
        """

    def test_entrerParking_parking_plein(self):
        """
        Parking plein : renvoie « Aucune place disponible pour votre véhicule ». (RF03)

        Assertion prévue : assertEqual
        """

    def test_nbFrequentations(self):
        """
        Deux entrées et deux sorties : nbFrequentations vaut 2. (RF09)

        Assertion prévue : assertEqual
        """


@unittest.skip("Partie 0 : spécification seulement")
class TestAbonnement(unittest.TestCase):
    """
    Tests de la classe Abonnement.

    Contexte : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ; A3 : 1,60 m x 4,00 m),
    voiture V de 1,80 m x 4,50 m (« AB-123-CD »), client C non abonné,
    formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def test_addContrat(self):
        """
        Le contrat est rattaché à l'abonnement. (RF12)

        Assertion prévue : assertIn
        """


@unittest.skip("Partie 0 : spécification seulement")
class TestContrat(unittest.TestCase):
    """
    Tests de la classe Contrat.

    Contexte : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ; A3 : 1,60 m x 4,00 m),
    voiture V de 1,80 m x 4,50 m (« AB-123-CD »), client C non abonné,
    formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def test_creation(self):
        """
        dateDebut vaut aujourd'hui et le contrat est en cours. (RF12)

        Assertion prévue : assertEqual, assertTrue
        """

    def test_rompreContrat_en_cours(self):
        """
        dateFin renseignée, estEnCours faux. (RF12)

        Assertion prévue : assertFalse
        """

    def test_rompreContrat_deja_rompu(self):
        """
        Contrat déjà rompu : aucun effet, renvoie False.

        Assertion prévue : assertFalse
        """


if __name__ == '__main__':
    unittest.main()
