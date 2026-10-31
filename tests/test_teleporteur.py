
import unittest

from modele.teleporteur import Teleporteur
from modele.parking import Parking, Place
from modele.client import Voiture


class TestTeleporteur(unittest.TestCase):
    """Tests unitaires de la classe Teleporteur."""

    def setUp(self):
        Parking._reinitialiser()

        self.parking = Parking(
            nbNiveaux=1,
            nbPlacesParNiveau=0
        )

        self.place1 = Place(
            numero=1,
            niveau="A",
            longueur=5.00,
            hauteur=2.00
        )

        self.place2 = Place(
            numero=2,
            niveau="A",
            longueur=5.00,
            hauteur=2.00
        )

        self.place3 = Place(
            numero=3,
            niveau="A",
            longueur=4.00,
            hauteur=1.60
        )

        self.parking.ajouterPlace(self.place1)
        self.parking.ajouterPlace(self.place2)
        self.parking.ajouterPlace(self.place3)

        self.teleporteur = Teleporteur()

        self.voiture = Voiture(
            immatriculation="AB-123-CD",
            hauteur=1.80,
            longueur=4.50
                              )

    def tearDown(self):
        Parking._reinitialiser()

    def test_teleporter_voiture_place_attribuee(self):
        """La voiture est reliée à la place attribuée."""

        placement = self.teleporteur.teleporterVoiture(
            self.voiture,
            self.place1
                                                      )

        self.assertIsNotNone(placement)
        self.assertIs(placement.place, self.place1)
        self.assertIs(placement.voiture, self.voiture)

    def test_teleporter_voiture_sans_place(self):
        """Une absence de place déclenche une ValueError."""

        with self.assertRaises(ValueError):
            self.teleporteur.teleporterVoiture(
                self.voiture,
                None
                                                )

    def test_super_abonne_place_disponible(self):
        """Le super-abonné obtient une place dans DreamPark."""

        self.teleporteur.teleporterVoitureSuperAbonne(
            self.voiture
                                                      )

        self.assertTrue(self.voiture.estDansParking)
        self.assertFalse(self.place1.estLibre)
        self.assertEqual(
            self.voiture.lieuStationnement,
            self.place1.idPlace
        )
        self.assertEqual(self.parking.nbPlacesLibres, 2)

    def test_super_abonne_parking_plein(self):
        """Le super-abonné est dirigé vers un parking partenaire."""

        voiture2 = Voiture("CD-456-EF", 1.80, 4.50)
        voiture3 = Voiture("GH-789-IJ", 1.80, 4.50)

        self.place1.addPlacementP(
            __import__("modele.parking", fromlist=["Placement"])
            .Placement(voiture2, self.place1)
        )

        self.place2.addPlacementP(
            __import__("modele.parking", fromlist=["Placement"])
            .Placement(voiture3, self.place2)
        )

        # A3 est trop petite pour la voiture de test.
        self.place3.addPlacementP(
            __import__("modele.parking", fromlist=["Placement"])
            .Placement(
                Voiture("KL-012-MN", 1.50, 3.50),
                self.place3
            )
        )

        self.teleporteur.teleporterVoitureSuperAbonne(
            self.voiture
        )

        self.assertEqual(
            self.voiture.lieuStationnement,
            "PARTENAIRE"
        )
        self.assertEqual(self.parking.nbPlacesLibres, 0)

    def test_super_abonne_ne_recoit_pas_refus(self):
        """Le super-abonné ne reçoit pas le message de refus."""

        voiture2 = Voiture("CD-456-EF", 1.80, 4.50)
        voiture3 = Voiture("GH-789-IJ", 1.80, 4.50)

        from modele.parking import Placement

        Placement(voiture2, self.place1)
        Placement(voiture3, self.place2)
        Placement(
            Voiture("KL-012-MN", 1.50, 3.50),
            self.place3
        )

        resultat = self.teleporteur.teleporterVoitureSuperAbonne(
            self.voiture
        )

        self.assertNotEqual(
            resultat,
            "Aucune place disponible pour votre véhicule"
        )


if __name__ == "__main__":
    unittest.main()
