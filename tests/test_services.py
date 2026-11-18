"""
Tests des classes Maintenance, Entretien, Livraison et Voiturier (spécification §8.7 et §8.8).

Partie 0 : chaque test est spécifié par son docstring (cas testé,
résultat attendu, assertion prévue). Le code des tests sera écrit en Partie 1,
d'ici là les classes sont marquées @unittest.skip.
"""

import unittest

from modele.parking import Parking
from modele.client import Client, Voiture
from modele.services import Maintenance, Entretien, Livraison, Voiturier
from modele.exceptions import LivraisonSansDemandeError


@unittest.skip("Partie 0 : spécification seulement")
class TestMaintenance(unittest.TestCase):
    """
    Tests de la classe Maintenance.

    Contexte : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ; A3 : 1,60 m x 4,00 m),
    voiture V de 1,80 m x 4,50 m (« AB-123-CD »), client C non abonné,
    formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def test_creation_date_demande(self):
        """
        dateDemande vaut aujourd'hui. (RF09)

        Assertion prévue : assertEqual
        """

    def test_effectuerMaintenance(self):
        """
        dateService et rapport renseignés, voiture regarée (nouveau placement). (RF06)

        Assertion prévue : assertIsNotNone, assertTrue(v.estDansParking)
        """


@unittest.skip("Partie 0 : spécification seulement")
class TestEntretien(unittest.TestCase):
    """
    Tests de la classe Entretien.

    Contexte : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ; A3 : 1,60 m x 4,00 m),
    voiture V de 1,80 m x 4,50 m (« AB-123-CD »), client C non abonné,
    formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def test_effectuerEntretien(self):
        """
        dateService et rapport renseignés, voiture regarée. (RF06)

        Assertion prévue : assertIsNotNone, assertTrue(v.estDansParking)
        """


@unittest.skip("Partie 0 : spécification seulement")
class TestLivraison(unittest.TestCase):
    """
    Tests de la classe Livraison.

    Contexte : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ; A3 : 1,60 m x 4,00 m),
    voiture V de 1,80 m x 4,50 m (« AB-123-CD »), client C non abonné,
    formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def test_effectuerLivraison(self):
        """
        Le voiturier est appelé, la place est libérée, la voiture est hors du parking. (RF08)

        Assertion prévue : assertFalse(v.estDansParking)
        """


@unittest.skip("Partie 0 : spécification seulement")
class TestVoiturier(unittest.TestCase):
    """
    Tests de la classe Voiturier.

    Contexte : niveau A de trois places (A1, A2 : 2,00 m x 5,00 m ; A3 : 1,60 m x 4,00 m),
    voiture V de 1,80 m x 4,50 m (« AB-123-CD »), client C non abonné,
    formules « Mensuel » et « Garantie » (pack garantie).
    """

    def setUp(self):
        """Crée le parking, ses trois places, la voiture V, le client C et les deux formules."""

    def tearDown(self):
        """Réinitialise le singleton Parking pour que les tests restent indépendants."""
        Parking._reinitialiser()

    def test_livrerVoiture_avec_demande(self):
        """
        Une demande existe : livraison effectuée à la bonne date et heure. (RF08)

        Assertion prévue : assertEqual
        """

    def test_livrerVoiture_sans_demande(self):
        """
        Aucune demande : lève LivraisonSansDemandeError. (RF08)

        Assertion prévue : assertRaises(LivraisonSansDemandeError)
        """


if __name__ == '__main__':
    unittest.main()
