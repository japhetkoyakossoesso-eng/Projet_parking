
import unittest

from modele.client import Voiture
from modele.exceptions import (
    PlaceOccupeeError,
    PlaceIncompatibleError,
    VoitureDejaGareeError,
)
from modele.parking import Parking, Place, Placement


class TestPlacement(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
