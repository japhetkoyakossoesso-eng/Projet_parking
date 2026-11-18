
import unittest

from modele.client import Voiture
from modele.parking import Parking, Place, Placement


class TestParking(unittest.TestCase):

    def setUp(self):
        Parking._reinitialiser()

        self.parking = Parking(nbNiveaux=1)

        self.place1 = Place(1, "A", 5.00, 2.00)
        self.place2 = Place(2, "A", 5.00, 2.00)
        self.place3 = Place(3, "A", 4.00, 1.60)

        self.parking.ajouterPlace(self.place1)
        self.parking.ajouterPlace(self.place2)
        self.parking.ajouterPlace(self.place3)

        self.voiture = Voiture("AB-123-CD", 1.80, 4.50)

    # TESTS DU PARKING

    def test_parking_est_un_singleton(self):
        autre_parking = Parking()
        self.assertIs(self.parking, autre_parking)

    def test_nombre_initial_de_places_libres(self):
        self.assertEqual(self.parking.nbPlacesLibres, 3)

    def test_ajout_place_avec_identifiant_duplique(self):
        place = Place(1, "A", 5.00, 2.00)

        with self.assertRaises(ValueError):
            self.parking.ajouterPlace(place)

    def test_ajout_place_dans_niveau_inexistant(self):
        place = Place(1, "B", 5.00, 2.00)

        with self.assertRaises(ValueError):
            self.parking.ajouterPlace(place)

    def test_nombre_places_libres_par_niveau(self):
        self.assertEqual(
            self.parking.nbPlacesLibresParNiveau("A"), 3
        )

    def test_niveau_inexistant(self):
        with self.assertRaises(ValueError):
            self.parking.nbPlacesLibresParNiveau("Z")

    def test_get_place_existante(self):
        self.assertIs(self.parking.getPlace("A1"), self.place1)

    def test_get_place_inexistante(self):
        self.assertIsNone(self.parking.getPlace("Z99"))

    def test_mes_places_retourne_toutes_les_places(self):
        places = self.parking.mesPlaces

        self.assertEqual(len(places), 3)
        self.assertIn(self.place1, places)
        self.assertIn(self.place2, places)
        self.assertIn(self.place3, places)

    def test_ajouter_abonnement(self):
        abonnement = object()

        self.parking.addAbonnement(abonnement)

        self.assertIn(abonnement, self.parking.mesAbonnements)

    def test_ajouter_abonnement_deja_existant(self):
        abonnement = object()

        self.parking.addAbonnement(abonnement)
        self.parking.addAbonnement(abonnement)

        self.assertEqual(len(self.parking.mesAbonnements), 1)

    # TESTS DE RECHERCHE DE PLACE

    def test_rechercher_place_compatible(self):
        place = self.parking.rechercherPlace(self.voiture)

        self.assertIsNotNone(place)
        self.assertTrue(place.estLibre)
        self.assertTrue(place.estCompatible(self.voiture))

    def test_aucune_place_compatible(self):
        grande_voiture = Voiture("FF-666-FF", 2.50, 6.00)

        self.assertIsNone(
            self.parking.rechercherPlace(grande_voiture)
        )

    def test_parking_sans_place_compatible_disponible(self):
        Placement(self.voiture, self.place1)

        autre_voiture = Voiture("KK-222-KK", 1.80, 4.50)
        Placement(autre_voiture, self.place2)

        derniere_voiture = Voiture("LL-333-LL", 1.80, 4.50)

        self.assertIsNone(
            self.parking.rechercherPlace(derniere_voiture)
        )

    def test_rechercher_place_ignore_les_places_occupees(self):
        Placement(self.voiture, self.place1)

        autre_voiture = Voiture("JJ-111-JJ", 1.80, 4.50)

        place = self.parking.rechercherPlace(autre_voiture)

        self.assertIs(place, self.place2)

    # TESTS DE L'HISTORIQUE

    def test_historique_initialement_vide(self):
        self.assertEqual(self.parking.historiquePassages(), [])

    def test_placement_termine_conserve_dans_historique(self):
        placement = Placement(self.voiture, self.place1)
        placement.partirPlace()

        historique = self.parking.historiquePassages()

        self.assertIn(placement, historique)

    def test_historique_conserve_placements_actifs_et_termines(self):
        premier = Placement(self.voiture, self.place1)
        premier.partirPlace()

        autre_voiture = Voiture("II-999-II", 1.70, 4.00)
        second = Placement(autre_voiture, self.place2)

        historique = self.parking.historiquePassages()

        self.assertIn(premier, historique)
        self.assertIn(second, historique)
        self.assertEqual(len(historique), 2)


if __name__ == "__main__":
    unittest.main()
