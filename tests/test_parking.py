
import unittest

from modele.client import Voiture
from modele.exceptions import (
    PlaceOccupeeError,
    PlaceIncompatibleError,
    VoitureDejaGareeError,
)
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

    def test_parking_est_un_singleton(self):
        autre_parking = Parking()
        self.assertIs(self.parking, autre_parking)

    def test_nombre_initial_de_places_libres(self):
        self.assertEqual(self.parking.nbPlacesLibres, 3)

    def test_ajout_place_avec_identifiant_duplique(self):
        place_dupliquee = Place(1, "A", 5.00, 2.00)

        with self.assertRaises(ValueError):
            self.parking.ajouterPlace(place_dupliquee)

    def test_ajout_place_dans_niveau_inexistant(self):
        place = Place(1, "B", 5.00, 2.00)

        with self.assertRaises(ValueError):
            self.parking.ajouterPlace(place)

    def test_nombre_places_libres_par_niveau(self):
        self.assertEqual(
            self.parking.nbPlacesLibresParNiveau("A"),
            3,
        )

    def test_niveau_inexistant(self):
        with self.assertRaises(ValueError):
            self.parking.nbPlacesLibresParNiveau("Z")

    def test_identifiant_place(self):
        self.assertEqual(self.place1.idPlace, "A1")

    def test_place_initialement_libre(self):
        self.assertTrue(self.place1.estLibre)

    def test_dimensions_exactes_acceptees(self):
        voiture = Voiture("AA-111-AA", 2.00, 5.00)

        self.assertTrue(self.place1.estCompatible(voiture))

    def test_dimensions_inferieures_acceptees(self):
        voiture = Voiture("BB-222-BB", 1.50, 4.00)

        self.assertTrue(self.place1.estCompatible(voiture))

    def test_hauteur_superieure_refusee(self):
        voiture = Voiture("CC-333-CC", 2.10, 4.00)

        self.assertFalse(self.place1.estCompatible(voiture))

    def test_longueur_superieure_refusee(self):
        voiture = Voiture("DD-444-DD", 1.50, 5.50)

        self.assertFalse(self.place1.estCompatible(voiture))

    def test_place_refuse_des_dimensions_nulles(self):
        with self.assertRaises(ValueError):
            Place(4, "A", 0, 2.00)

    def test_voiture_refuse_une_immatriculation_vide(self):
        with self.assertRaises(ValueError):
            Voiture("", 1.80, 4.50)

    def test_voiture_refuse_des_dimensions_nulles(self):
        with self.assertRaises(ValueError):
            Voiture("EE-555-EE", 0, 4.50)

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

    def test_place_incompatible_refuse_le_placement(self):
        grande_voiture = Voiture("GG-777-GG", 2.50, 6.00)

        with self.assertRaises(PlaceIncompatibleError):
            Placement(grande_voiture, self.place1)

    def test_place_occupee_refuse_un_second_placement(self):
        Placement(self.voiture, self.place1)
        autre_voiture = Voiture("HH-888-HH", 1.70, 4.00)

        with self.assertRaises(PlaceOccupeeError):
            Placement(autre_voiture, self.place1)

    def test_voiture_deja_garee_ne_peut_pas_etre_garee_deux_fois(self):
        Placement(self.voiture, self.place1)

        with self.assertRaises(VoitureDejaGareeError):
            Placement(self.voiture, self.place2)

    def test_placement_initialement_en_cours(self):
        placement = Placement(self.voiture, self.place1)

        self.assertTrue(placement.estEnCours)
        self.assertIsNone(placement.dateFin)

    def test_voiture_garee_conserve_le_lieu_stationnement(self):
        Placement(self.voiture, self.place1)

        self.assertTrue(self.voiture.estDansParking)
        self.assertEqual(
            self.voiture.lieuStationnement,
            self.place1.idPlace,
        )

    def test_nombre_places_libres_apres_entree(self):
        Placement(self.voiture, self.place1)

        self.assertEqual(self.parking.nbPlacesLibres, 2)

    def test_place_occupee_non_attribuee(self):
        Placement(self.voiture, self.place1)

        self.assertFalse(self.place1.estLibre)
        self.assertEqual(self.parking.nbPlacesLibres, 2)

    def test_place_liberee_redevient_disponible(self):
        placement = Placement(self.voiture, self.place1)

        self.assertTrue(placement.partirPlace())
        self.assertTrue(self.place1.estLibre)

    def test_nombre_places_libres_apres_sortie(self):
        placement = Placement(self.voiture, self.place1)
        placement.partirPlace()

        self.assertEqual(self.parking.nbPlacesLibres, 3)

    def test_voiture_sortie_redevient_disponible(self):
        placement = Placement(self.voiture, self.place1)
        placement.partirPlace()

        self.assertFalse(self.voiture.estDansParking)
        self.assertIsNone(self.voiture.lieuStationnement)

    def test_placement_ne_peut_pas_etre_termine_deux_fois(self):
        placement = Placement(self.voiture, self.place1)

        self.assertTrue(placement.partirPlace())
        self.assertFalse(placement.partirPlace())

    def test_historique_initialement_vide(self):
        self.assertEqual(self.parking.historiquePassages(), [])

    def test_placement_termine_conserve_dans_historique(self):
        placement = Placement(self.voiture, self.place1)
        placement.partirPlace()

        historique = self.parking.historiquePassages()

        self.assertIn(placement, historique)

    def test_historique_conserve_les_placements_actifs_et_termines(self):
        premier_placement = Placement(self.voiture, self.place1)
        premier_placement.partirPlace()

        autre_voiture = Voiture("II-999-II", 1.70, 4.00)
        second_placement = Placement(autre_voiture, self.place2)

        historique = self.parking.historiquePassages()

        self.assertIn(premier_placement, historique)
        self.assertIn(second_placement, historique)
        self.assertEqual(len(historique), 2)


if __name__ == "__main__":
    unittest.main()
