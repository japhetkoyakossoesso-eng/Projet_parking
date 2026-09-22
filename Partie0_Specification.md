# Projet DreamPark — Partie 0

## Spécification fonctionnelle et spécification des tests

**Équipe :** 404 Places Not Found
**Membres :** Japhet KOYAKOSSO ESSO (spécification des tests), Ayachi Mohamed (spécification fonctionnelle)
**Formation :** L3 MIASHS — Parcours Informatique et SHS
**Université :** Toulouse 2 — Jean-Jaurès

---

# 1. Présentation du projet

Le projet consiste à concevoir un système de gestion des places et des services du parking DreamPark.

Le parking est composé d'un ensemble de places et de deux accès. Chaque accès dispose :
- d'une caméra ;
- d'une borne à tickets-paiement ;
- d'un panneau d'affichage ;
- de deux téléporteurs.

Chaque place possède un identifiant unique ainsi que des caractéristiques (niveau, longueur, hauteur) permettant de déterminer sa compatibilité avec un véhicule.

Lorsqu'une voiture entre dans le parking, le système lui attribue une place adaptée. Lorsqu'elle quitte le parking, la place est libérée et le nombre de places disponibles est mis à jour.

Le parking propose également différents services : abonnement, pack garantie, livraison, entretien, maintenance.

---

# 2. Objectifs du système

Le système DreamPark doit permettre :
- de gérer les places de stationnement ;
- d'identifier les véhicules ;
- d'attribuer une place adaptée à chaque véhicule ;
- de gérer l'entrée et la sortie des véhicules ;
- de gérer les tickets ;
- de gérer les abonnements et le pack garantie ;
- de proposer différents services aux abonnés ;
- de gérer la livraison des véhicules ;
- de conserver les informations relatives aux passages ;
- de consulter et éditer les statistiques du parking.

---

# 3. Acteurs

Le cours distingue quatre catégories d'acteurs : **acteurs principaux** (utilisent les fonctions principales du système), **acteurs secondaires** (tâches administratives/maintenance), **matériel externe**, **autres systèmes**. Sur cette base, les acteurs de DreamPark se classent ainsi :

| Acteur | Catégorie | Rôle |
|---|---|---|
| Client | Principal | Utilise le service de base : se garer, récupérer son véhicule, s'abonner |
| Abonné | Principal (spécialisation de Client) | Bénéficie des services (maintenance, entretien, livraison) |
| Super_Abonné | Principal (spécialisation de Client) | Bénéficie du pack garantie de stationnement |
| Voiturier | Secondaire | Exécute les livraisons demandées |
| Administrateur | Secondaire | Consulte et édite les statistiques |

**Relations de généralisation entre acteurs** (au sens du cours : *"le sous-acteur peut faire avec le système tout ce que peut faire l'acteur parent, et d'autres choses"*) :
- `Abonné` est une sorte de `Client`.
- `Super_Abonné` est une sorte de `Client`.

---

# 4. Diagramme de cas d'utilisation

| Paquetage | Cas d'utilisation | Acteur |
|---|---|---|
| CLIENT | Se garer | Client |
| CLIENT | Reprendre la voiture | Client |
| ABONNEMENT | S'abonner | Client |
| ABONNEMENT | Se désabonner | Abonné |
| PACK_GARANTIE | S'inscrire au pack garantie | Super_Abonné |
| PACK_GARANTIE | Se désinscrire du pack garantie | Super_Abonné |
| SERVICES | Demander Maintenance | Abonné |
| SERVICES | Demander Entretien | Abonné |
| SERVICES | Demander Livraison | Abonné |
| SERVICES | Effectuer la livraison | Voiturier |
| ADMINISTRATION | Consulter les statistiques | Administrateur |
| ADMINISTRATION | Éditer les statistiques | Administrateur |

**Relations entre cas d'utilisation** (vocabulaire du cours : *Extension* — « B étend A, B est une partie optionnelle de A » ; *Utilisation* — « A inclut B, B est une partie obligatoire de A ») :
- **Se désinscrire du pack garantie** \<\<extend\>\> **S'inscrire au pack garantie**
- **S'abonner** \<\<extend\>\> **Se garer** (le client peut choisir de s'abonner pendant qu'il se gare)
- **Reprendre la voiture** \<\<extend\>\> **Se garer** (au sens du diagramme fourni par l'enseignant : ce sont deux cas liés du même paquetage CLIENT)
- **Effectuer la livraison** \<\<extend\>\> **Demander Livraison**
- **Éditer les statistiques** \<\<extend\>\> **Consulter les statistiques**

---

# 5. Fonctionnalité « Se garer »

**Acteur** : Client
**Objectif** : permettre à un client de garer son véhicule dans une place adaptée du parking.

**Début du cas d'utilisation** (événement déclencheur) : le client arrive devant l'un des accès du parking.
**Fin du cas d'utilisation** (événement d'arrêt) : le ticket est délivré et le véhicule est garé — ou le client est informé qu'aucune place n'est disponible.

**Préconditions** :
- le client se présente à l'un des accès ;
- le véhicule peut être identifié par le système ;
- le parking est disponible (instance unique du singleton `Parking`).

**Scénario nominal** :
1. Le client arrive devant l'un des accès.
2. La caméra récupère les informations du véhicule : immatriculation, hauteur, longueur.
3. Le système détermine le statut du client (Super_Abonné, Abonné, Client).
4. Le parking recherche une place compatible avec le véhicule.
5. Une place disponible est attribuée au véhicule.
6. La borne effectue les opérations nécessaires concernant le ticket.
7. Le système prend en compte le paiement ou l'abonnement du client.
8. Un ticket est délivré.
9. Le téléporteur prend en charge le véhicule.
10. Le véhicule est déplacé vers la place attribuée.
11. La place devient occupée.
12. Le nombre de places disponibles est mis à jour.
13. Le panneau d'affichage est actualisé.

**Postconditions (succès)** : une place passe à l'état occupé, un `Placement` actif est créé, `Voiture.estDansParking = True`, ticket délivré, panneaux d'affichage à jour.

**Scénario alternatif — aucune place disponible** :
- aucune place n'est attribuée ;
- le système informe le client qu'aucune place n'est disponible ;
- le véhicule n'est pas garé dans le parking.

---

# 6. Fonctionnalité « Reprendre la voiture »

**Acteur** : Client
**Objectif** : permettre au client de récupérer son véhicule stationné dans le parking.

**Début** : le client se présente à un accès avec son ticket.
**Fin** : la place est libérée et le véhicule est rendu au client (ou pris en charge pour livraison/service).

**Préconditions** :
- le véhicule est présent dans le parking ;
- le client possède le ticket correspondant.

**Scénario nominal** :
1. Le client se présente à l'un des accès.
2. Il présente son ticket.
3. Le système identifie le véhicule correspondant.
4. Le téléporteur récupère le véhicule.
5. Le véhicule est ramené vers l'accès.
6. La place précédemment occupée est libérée.
7. Le système est informé que la place est disponible.
8. Le nombre de places disponibles est mis à jour.
9. Le panneau d'affichage est actualisé.
10. Le véhicule est rendu au client.

**Postconditions** : `Placement` clôturé, place libérée, compteurs et panneaux à jour, `Voiture.estDansParking = False`.

**Scénarios alternatifs** :
- **Livraison** : si le client a demandé une livraison, le système récupère le véhicule et organise sa livraison conformément à la demande, au lieu de le restituer physiquement.
- **Entretien / maintenance** : le système prend en charge le véhicule et le gare à nouveau après la réalisation du service (nouveau `Placement`, sans nouvelle interaction avec le client).

---

# 7. Fonctionnalité « S'abonner »

**Acteur** : Client
**Scénario** :
1. Le client consulte les abonnements disponibles.
2. Il sélectionne une formule.
3. Le système enregistre son abonnement.
4. Un contrat est associé à l'abonnement.
5. Le client devient abonné.
6. Il peut alors bénéficier des services associés à son abonnement.

**Postcondition** : `Client.estAbonne = True`, `Contrat` actif créé.

# 8. Fonctionnalité « Se désabonner »

**Acteur** : Abonné
**Scénario** :
1. L'abonné demande la résiliation de son abonnement.
2. Le système identifie le contrat correspondant.
3. Le contrat est clôturé.
4. Le statut du client est mis à jour.

# 9. Fonctionnalité « Pack garantie »

**Inscription** (Super_Abonné) : le client souscrit au pack garantie ; le parking lui réserve une place ; si aucune place n'est disponible dans le parking, le véhicule peut être stationné dans un autre parking, de façon transparente pour le client ; l'inscription donne également accès aux services réservés aux abonnés.

**Désinscription** : le client met fin à son inscription ; le système met à jour son abonnement en conséquence.

# 10. Fonctionnalité « Demander une maintenance »

**Acteur** : Abonné
1. Demande de maintenance enregistrée.
2. Véhicule pris en charge (cf. Reprendre la voiture).
3. Maintenance réalisée, informations enregistrées (rapport).
4. Véhicule garé à nouveau.

# 11. Fonctionnalité « Demander un entretien »

**Acteur** : Abonné — même déroulé que la maintenance (étapes 1 à 4), appliqué à un entretien.

# 12. Fonctionnalité « Demander une livraison »

**Acteur** : Abonné
**Informations requises** : date, heure, adresse.
1. L'abonné demande la livraison de son véhicule.
2. Le système enregistre la demande.
3. Le véhicule est récupéré.
4. Un voiturier prend en charge la livraison.
5. Le véhicule est livré à l'adresse et à l'heure demandées.

Politique de flexibilité : le client peut modifier ses options de service par simple appel téléphonique avant l'exécution.

# 13. Fonctionnalité « Effectuer la livraison »

**Acteur** : Voiturier — prend en charge le véhicule et effectue la livraison conformément aux informations enregistrées dans la demande.

# 14. Fonctionnalité « Consulter / Éditer les statistiques »

**Acteur** : Administrateur — le système conserve une trace des passages des véhicules (fréquentation, activité, usage des services). L'administrateur peut consulter cette activité et l'éditer sous différents formats : texte, HTML, image (plans), vidéo.

---

# 15. Diagramme de classes — inventaire

Notation reprise du cours (`+ public`, `# protégé`, `- privé`, `nom : Type`, `opération(arg : type) : TypeRetour`), sur la base du diagramme fourni par l'enseignant.

| Classe | Attributs (extrait) | Opérations principales |
|---|---|---|
| `Parking` *(singleton)* | `- nbPlacesParNiveau`, `- nbPlacesLibres`, `- prix`, `- nbNiveaux` | `+ rechercherPlace(v: Voiture): Place`, `+ nbPlacesLibresParNiveau(niveau: char): int`, `+ addAbonnement(ab: Abonnement)` |
| `Place` | `+ numero: int`, `+ niveau: char`, `+ longueur: float`, `+ hauteur: float`, `+ estLibre: bool` | `+ addPlacementP(p: Placement)` |
| `Voiture` | `+ immatriculation: string`, `+ hauteur: float`, `+ longueur: float`, `+ estDansParking: bool` | `+ addPlacementV(p: Placement)` |
| `Placement` | `+ dateDebut: Date`, `+ dateFin: Date`, `+ estEnCours: bool` | `+ partirPlace()` |
| `Client` | `+ nom: string`, `+ adresse: string`, `+ estAbonne: bool`, `+ estSuperAbonne: bool`, `+ nbFrequentations: int` | `+ sAbonner(ab: Abonnement)`, `+ nouvelleVoiture(imma, hautV, longV)`, `+ seDesabonner()`, `+ demanderMaintenance()`, `+ demanderEntretien()`, `+ demanderLivraison(dateL, heure, adresseL)`, `+ entrerParking(a: Acces): string` |
| `Abonnement` | `+ libelle: string`, `+ prix: float`, `+ estPackGar: bool` | `+ addContrat(contrat: Contrat)` |
| `Contrat` | `+ dateDebut: Date`, `+ dateFin: Date`, `+ estEnCours: bool` | `+ rompreContrat()` |
| `Service` *(mère de Maintenance/Entretien/Livraison)* | `+ dateDemande: Date`, `+ dateService: Date`, `+ rapport: string` | — |
| `Maintenance` | — | `+ effectuerMaintenance(v: Voiture)` |
| `Entretien` | — | `+ effectuerEntretien()` |
| `Livraison` | — | `+ effectuerLivraison()` |
| `Voiturier` | `+ numVoiturier: int` | `+ livrerVoiture(v: Voiture, date: Date, heure: int)` |
| `Acces` | — | `+ actionnerCamera(c: Client): Voiture`, `+ actionnerPanneau()`, `+ lancerProcedureEntree(c: Client): string` |
| `Camera` | — | `+ capturerHauteur(v): float`, `+ capturerLongueur(v): float`, `+ capturerImmat(v): string` |
| `BorneTicket` | — | `+ delivrerTicket(c): string`, `+ proposerServices()`, `+ proposerAbonnements(c, p)`, `+ proposerTypePaiement()` |
| `PanneauAffichage` | — | `+ afficherNbPlacesDisponibles(p: Parking): string` |
| `Teleporteur` | — | `+ teleporterVoiture(v, p): Placement`, `+ teleporterVoitureSuperAbonne(v): string` |

> ⚠️ **Point ouvert à trancher/justifier** : la classe `Statistiques` proposée par Ayachi dans une version antérieure n'apparaît pas dans le diagramme de classes fourni par l'enseignant. Le sujet impose de justifier toute modification des artefacts fournis (consigne « Méthode de travail »). À décider en binôme : l'ajouter et la justifier dans le rapport, ou la retirer et modéliser les statistiques comme un comportement de `Parking`/`Administrateur`. On va justifier ça plutart.

---

# 16. Règles fonctionnelles (RF)

| # | Règle |
|---|---|
| **RF01** | Le système doit pouvoir récupérer l'immatriculation, la hauteur et la longueur du véhicule à l'aide de la caméra. |
| **RF02** | Le système doit attribuer une place compatible avec les dimensions du véhicule lorsqu'une place est disponible. |
| **RF03** | Lorsqu'aucune place adaptée n'est disponible, le système ne doit pas effectuer le stationnement normal du véhicule. |
| **RF04** | L'entrée ou la sortie d'une voiture doit entraîner la mise à jour du nombre de places disponibles. |
| **RF05** | Lorsqu'une place est attribuée, le système doit permettre la délivrance d'un ticket. |
| **RF06** | Les abonnés doivent pouvoir bénéficier des services prévus par leur abonnement. |
| **RF07** | Le pack garantie doit permettre de garantir une solution de stationnement au client, éventuellement dans un autre parking. |
| **RF08** | Le système doit permettre de demander et d'effectuer la livraison d'un véhicule. |
| **RF09** | Le système doit conserver des informations permettant d'étudier la fréquentation du parking. |
| **RF10** | L'administrateur doit pouvoir consulter et éditer les statistiques. |

---

# 17. Spécification des tests unitaires par classe

Conformément au « Travail à réaliser » du sujet (identifier puis spécifier les tests unitaires de chaque classe, sans implémentation à ce stade). Pour chaque méthode : **cas nominal**, **cas limite**, **cas d'erreur**, avec traçabilité vers les RF ci-dessus.

## 17.1 `Place`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Affectation à un véhicule compatible | Nominal | Place disponible → occupée | RF02 |
| Affectation à un véhicule incompatible (hauteur/longueur) | Erreur | Refus de l'affectation | RF02 |
| Affectation sur une place déjà occupée | Erreur | Refus / exception (à définir) | RF02, RF03 |
| Libération après récupération | Nominal | Place repasse à disponible | RF04 |
| Libération d'une place déjà disponible | Limite | Comportement idempotent à définir | RF04 |

## 17.2 `Voiture`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Association à un `Placement` | Nominal | `estDansParking = True` | — |
| Association alors que la voiture est déjà dans le parking | Erreur | Refus | RF03 |
| Sortie du parking | Nominal | `estDansParking = False` | RF04 |

## 17.3 `Placement`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Fin d'un placement en cours | Nominal | `estEnCours = False`, `dateFin` renseignée, place libérée | RF04 |
| Fin d'un placement déjà terminé | Limite | Comportement idempotent à définir | RF04 |

## 17.4 `Client`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Recherche de place pour un client non abonné | Nominal | Place compatible proposée si disponible | RF02 |
| Recherche de place, parking plein / aucune place compatible | Erreur | Indication explicite "aucune place" | RF03 |
| Accès à un service abonné par un client non abonné | Erreur | Accès refusé | RF06 |
| Accès à un service abonné par un abonné | Nominal | Service accepté | RF06 |
| Souscription d'un abonnement | Nominal | Statut client mis à jour (abonné/super-abonné) | RF06, RF07 |
| Ajout d'un nouveau véhicule | Nominal | Véhicule correctement rattaché | — |

## 17.5 `Contrat` / `Abonnement`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Souscription | Nominal | Contrat actif créé | RF06 |
| Résiliation d'un contrat actif | Nominal | `estEnCours = False`, `dateFin` renseignée | RF06 |
| Résiliation d'un contrat déjà résilié | Limite | Comportement idempotent à définir | — |
| Accès service sans contrat actif | Erreur | Accès refusé | RF06 |

## 17.6 `Service` / `Maintenance` / `Entretien` / `Livraison`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Création d'une demande de service | Nominal | `dateDemande` horodatée | — |
| Exécution (maintenance/entretien) | Nominal | Véhicule repris, service effectué, regaré, rapport renseigné | RF06 |
| Demande de livraison avec date/heure/adresse | Nominal | Livraison programmée correctement | RF08 |
| Modification des options avant exécution | Nominal | Nouvelle adresse/heure prise en compte | RF08 |
| Demande de service par un client non abonné | Erreur | Refus | RF06 |

## 17.7 `Voiturier`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Livraison suite à une demande existante | Nominal | Véhicule livré à l'adresse/heure attendues | RF08 |
| Tentative de livraison sans demande préalable | Erreur | Refus | RF08 |

## 17.8 `Camera`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Capture des infos véhicule | Nominal | Immat/hauteur/longueur cohérentes | RF01 |
| Capture avec infos incomplètes | Erreur | Comportement à définir | RF01 |

## 17.9 `BorneTicket`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Délivrance après affectation de place | Nominal | Ticket valide retourné | RF05 |
| Délivrance sans place affectée | Erreur | Aucun ticket délivré | RF03, RF05 |
| Proposition de services (abonné vs non-abonné) | Nominal | Liste différente selon statut | RF06 |
| Récupération du mode de paiement | Nominal | Valeur cohérente (CB/espèces) | — |

## 17.10 `Teleporteur`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Déplacement vers une place assignée | Nominal | `Placement` créé, bonne place associée | — |
| Déplacement pour un super-abonné (pack garanti) | Nominal | Chemin dédié, sans recherche de place classique | RF07 |
| Retour d'un véhicule à la sortie | Nominal | Place libérée | RF04 |

## 17.11 `PanneauAffichage`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Affichage du nombre de places disponibles | Nominal | Valeur = places libres à l'instant T | RF04 |
| Mise à jour après entrée/sortie | Nominal | Compteur décrémenté/incrémenté | RF04 |
| Affichage parking plein | Limite | Valeur = 0, cohérent avec RF03 | RF03, RF04 |

## 17.12 `Acces`
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Procédure d'entrée complète (test d'intégration au niveau classe) | Nominal | Séquence correcte, ticket délivré, véhicule placé | RF01, RF02, RF05 |
| Procédure d'entrée, parking plein | Erreur | Message d'absence de place, aucun ticket | RF03 |

## 17.13 `Parking` *(singleton)*
| Cas testé | Type | Résultat attendu | RF |
|---|---|---|---|
| Instanciation multiple | Nominal | Une seule instance (test du patron singleton) | — |
| Recherche de place compatible | Nominal | Place trouvée si elle existe | RF02 |
| Recherche de place, aucune compatible | Erreur | Indication "aucune place" | RF03 |
| Comptage de places libres par niveau | Nominal | Valeur exacte | — |
| Mise à jour globale après entrée/sortie | Nominal | Compteur cohérent avec la somme des places | RF04 |

### Synthèse de couverture

| RF | Classes testées |
|---|---|
| RF01 | `Camera`, `Acces` |
| RF02 | `Place`, `Client`, `Parking`, `Acces` |
| RF03 | `Place`, `Client`, `Parking`, `BorneTicket`, `Acces`, `PanneauAffichage` |
| RF04 | `Place`, `Voiture`, `Placement`, `Teleporteur`, `PanneauAffichage`, `Parking` |
| RF05 | `BorneTicket`, `Acces` |
| RF06 | `Client`, `Contrat`/`Abonnement`, `Service` |
| RF07 | `Client`, `Teleporteur` |
| RF08 | `Service`/`Livraison`, `Voiturier` |
| RF09 | non couvert explicitement — dépend de la résolution du point ouvert sur la classe `Statistiques` (§15) |
| RF10 | non couvert explicitement — idem, dépend de la classe portant les statistiques |

---

# 18. Choix de conception retenus

Points soulevés à la relecture de la Partie 0, tranchés en binôme avant d'attaquer la Partie 1. Le principe directeur retenu : **rester au plus près du modèle fourni par l'enseignant** plutôt que d'ajouter des éléments qui devraient ensuite être justifiés — conformément à la consigne « Méthode de travail » du sujet (*"toute modification apportée aux artefacts issus de la modélisation proposés est à justifier"*).

### 18.1 Retour de `rechercherPlace` quand le parking est plein

**Décision : retourner `None`.**
Le sujet précise lui-même : *"Si le parking est plein, une valeur particulière est retournée."* Un parking plein est un état métier normal (pas une erreur de programmation) — l'exception Python reste réservée aux violations de contrat internes. `None` est la valeur idiomatique en Python pour "pas de résultat".

### 18.2 Héritage `Client → Abonné → Super_Abonné`

**Décision : ne pas créer de sous-classes ; une seule classe `Client`, statut géré par `estAbonne` et `estSuperAbonne`.**
Le diagramme de classes fourni ne définit qu'une seule classe `CLIENT` avec ces deux booléens. La hiérarchie Client/Abonné/Super_Abonné n'existe que côté acteurs UML (diagramme de cas d'utilisation), pas côté classes. Créer trois classes distinctes reviendrait à modifier le modèle fourni sans nécessité — on reste donc fidèle au diagramme donné.

### 18.3 Classe `Statistiques`

**Décision : la retirer.** Les statistiques sont modélisées comme un comportement porté par `Parking` (conservation de la trace de passage) et consulté/édité via l'acteur `Administrateur`, conformément au modèle fourni. Cela évite d'introduire une classe absente du diagramme de l'énoncé et la justification qu'elle exigerait.

### 18.4 Format de persistance des données

**Décision : reporté à la Partie 3.** La consigne du sujet classe explicitement ce point en 3.2 ("Gestion de la persistance"), pas en Partie 0 — pas de blocage à ce stade.

### 18.5 Politique de gestion des erreurs

**Décision : une règle unique appliquée à toutes les classes.**
- **Résultat métier attendu** (parking plein, pas d'abonnement actif, contrat déjà résilié) → valeur de retour spéciale (`None`, `False`).
- **Violation d'un contrat / état incohérent** (téléporteur actionné sans demande de livraison, place déjà occupée réaffectée) → exception Python personnalisée.

### 18.6 Rôle du `Voiturier` dans « Se garer »

**Décision : rien à modifier.** L'énoncé porte l'annotation *"Nous n'avons pas fait la classe Voiturier pour l'UC garer la voiture"* — c'est un choix assumé par l'enseignant dans le modèle fourni, pas un oubli à corriger.