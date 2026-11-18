"""
Exceptions propres au parking DreamPark.

Règle suivie dans tout le projet :
- un résultat normal du métier (parking plein, client non abonné...) renvoie None ou False ;
- un appel incohérent, qui ne devrait pas arriver si le reste du programme est correct,
  lève une de ces exceptions.
"""


class PlaceOccupeeError(Exception):
    """Levée quand on essaie de garer une voiture sur une place déjà occupée."""


class PlaceIncompatibleError(Exception):
    """Levée quand une voiture est plus haute ou plus longue que la place visée."""


class VoitureDejaGareeError(Exception):
    """Levée quand on essaie de garer une voiture qui est déjà dans le parking."""


class LivraisonSansDemandeError(Exception):
    """Levée quand un voiturier doit livrer une voiture pour laquelle aucune livraison n'a été demandée."""
