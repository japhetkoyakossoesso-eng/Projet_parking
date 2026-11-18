# Projet DreamPark : Partie 1

## Réalisation du use case « Se garer »

Équipe : 404 Places Not Found  
Membres : Japhet KOYAKOSSO ESSO (modèle), Ayachi Mohamed (tests)  
Formation : L3 MIASHS, parcours Informatique et SHS  
Université Toulouse 2 Jean-Jaurès

---

## 1. Ce que fait cette partie

La Partie 1 rend le use case « Se garer » utilisable. Quand un client arrive à l'un des deux accès :

1. la caméra relève l'immatriculation et les dimensions de la voiture ;
2. la borne lit la carte du client (non abonné, abonné ou super-abonné) ;
3. le parking cherche une place libre assez grande ;
4. la borne propose les services à un abonné, ou le mode de paiement et les abonnements à un non-abonné ;
5. la borne délivre un ticket, le téléporteur conduit la voiture à sa place et les panneaux se mettent à jour.

Si aucune place ne convient, le client reçoit le message « Aucune place disponible pour votre véhicule ». Un super-abonné n'est jamais refusé : quand DreamPark est plein, sa voiture est garée dans le parking partenaire.

Cette partie est construite à partir de la Partie 0 : le squelette a été repris et les méthodes ont été écrites en suivant la spécification et le diagramme d'activité « Se garer ».

## 2. Ce qui a été réalisé

| Dossier | Contenu |
|---|---|
| `modele/` | Toutes les classes du diagramme : `Parking`, `Place`, `Placement`, `Client`, `Voiture`, `Abonnement`, `Contrat`, `Acces`, `Camera`, `BorneTicket`, `PanneauAffichage`, `Teleporteur`, ainsi que les services (`Maintenance`, `Entretien`, `Livraison`, `Voiturier`) qui serviront en Partie 2 |
| `tests/` | Les tests unitaires de chaque classe du use case, les tests d'intégration de `Acces` (avec des objets simulés `Mock`) et du contrôleur |
| `vue/` | `VueConsole` : les menus et les saisies au clavier |
| `controleur/` | `ControleurParking` : crée un parking de démonstration et exécute les actions du menu |
| `main.py` | Lance le menu console |

Le programme suit le patron MVC : la vue n'utilise jamais directement le modèle, elle passe par le contrôleur. On peut donc tester le modèle seul, et remplacer la vue console par l'interface tkinter en Partie 4 sans toucher au modèle.

## 3. Le menu console

```
1. Nouveau client
2. Se garer
3. S'abonner
4. Voir l'état du parking
5. Voir les clients
0. Quitter
```

Le parking de démonstration a deux niveaux (A et B) de cinq places de tailles différentes. Seules A5 et B5 (6.00 m x 2.50 m) acceptent une voiture de 2.40 m x 5.90 m : cela permet de montrer le cas « parking plein » et le parking partenaire sans créer dix voitures.

Les saisies sont contrôlées : un nombre invalide, un choix hors du menu ou un champ vide sont redemandés, et une voiture aux dimensions négatives est refusée avec un message.

## 4. Les tests

Commande, depuis le dossier `Projet_parking` :

```bash
python3 -m unittest discover -s tests -v
```

Résultat : `Ran 112 tests`, `OK (skipped=32)`.

| Fichier | Ce qui est vérifié |
|---|---|
| `test_parking.py` | Singleton, ajout de places (doublon, niveau inexistant), places libres, recherche de place, abonnements, historique |
| `test_place.py` | Identifiant, compatibilité (valeurs limites : dimensions égales acceptées, supérieures refusées), dimensions nulles refusées |
| `test_placement.py` | Garer une voiture, place occupée ou incompatible, voiture déjà garée, libération de la place |
| `test_voiture.py` | Création, données invalides, état initial, ajout de placement |
| `test_camera.py` | Lecture des dimensions et de la plaque, plaque vide ou illisible |
| `test_borne_ticket.py` | Ticket (avec ou sans place, unique), carte, services, abonnements, paiement |
| `test_panneau_affichage.py` | Nombre de places affiché : parking vide, après une entrée, plein |
| `test_teleporteur.py` | Téléportation, absence de place, super-abonné (place libre et parking partenaire) |
| `test_acces.py` | Scénario complet avec matériel simulé : non-abonné, parking plein, super-abonné |
| `test_controleur.py` | « Se garer » de bout en bout, sans clavier |

Les 32 tests mis en pause sont ceux de `test_client.py` et `test_services.py` : ils portent sur les services et la sortie du parking, qui relèvent de la Partie 2.

## 5. Modifications par rapport aux artefacts de modélisation

Chaque ajout au diagramme de classes est justifié ci-dessous.

| Ajout | Pourquoi |
|---|---|
| `Parking.ajouterPlace()`, `getPlace()`, `mesPlaces`, `niveaux()` | Le diagramme ne dit pas comment les places arrivent dans le parking : il faut pouvoir les créer et les retrouver par leur identifiant |
| `Parking._reinitialiser()` | Garder les tests indépendants malgré le singleton |
| `Parking.mesVoituriers`, `voiturierDisponible()` | Trouver un voiturier pour une livraison |
| `Place.estCompatible()` | Ne pas écrire deux fois la vérification des dimensions |
| `Place.liberer()` | `estLibre` est privé, il faut une méthode pour libérer la place |
| `Voiture.lieuStationnement` | Savoir où est la voiture, y compris au parking partenaire (choix déjà fait en Partie 0) |
| `Voiture.mesPlacements`, `Client.mesContrats`, `Abonnement.mesContrats` | Traduction en Python des associations du diagramme |
| `Client.contratEnCours`, `Client.monAbonnement` | Calculer le statut du client à partir de ses contrats |
| Paramètre `place` de `BorneTicket.delivrerTicket` | Délivrer le ticket avant la téléportation, dans l'ordre du diagramme d'activité |
| Paramètres `modePaiement` et `choixAbonnement` de `Acces.lancerProcedureEntree` | Transmettre les réponses du client aux questions de la borne |
| `Camera.capturerImmatr` refuse une plaque faite seulement d'espaces | Une telle plaque est illisible au même titre qu'une plaque vide (cas ajouté par les tests) |
| `Service.voiture`, `Service.estEffectue`, `Livraison.modifier()`, `Voiturier.mesLivraisons` | Relier un service à sa voiture et permettre de modifier une livraison (préparation de la Partie 2) |
| Classes `VueConsole` et `ControleurParking` | Patron MVC : séparer l'affichage, le contrôle et le modèle |

## 6. Répartition du travail

| Membre | Travail |
|---|---|
| Japhet KOYAKOSSO ESSO | Écriture du modèle (`modele/`) |
| Ayachi Mohamed | Écriture des tests unitaires et d'intégration (`tests/`) |
| Les deux | Mise en commun des tests et du modèle, menu console, rapport |

## 7. Suite

La Partie 2 réalisera le use case « Reprendre la voiture » : sortie du parking, paiement, services et livraison. Les tests de `test_client.py` et `test_services.py` seront alors réactivés.
