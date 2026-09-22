# Projet DreamPark — Partie 0

## Spécification fonctionnelle

**Équipe :** 404 Places Not Found  
**Membres :** Japhet KOYAKOSSO ESSO, Ayachi Mohamed  
**Formation :** L3 MIASHS — Parcours Informatique et SHS  
**Université :** Toulouse 2 — Jean-Jaurès

---

# 1. Présentation du projet

Le projet consiste à concevoir un système de gestion des places et des services du parking DreamPark.

Le parking est composé d'un ensemble de places et de deux accès. Chaque accès dispose :

- d'une caméra ;
- d'une borne à tickets-paiement ;
- de deux téléporteurs.

Chaque place possède un identifiant unique ainsi que des caractéristiques permettant d'identifier sa compatibilité avec les véhicules.

Lorsqu'une voiture entre dans le parking, le système lui attribue une place adaptée. Lorsqu'elle quitte le parking, la place est de nouveau disponible et le nombre de places disponibles est mis à jour.

Le parking propose également différents services, notamment l'abonnement, le pack garantie, la livraison, l'entretien et la maintenance.

---

# 2. Objectifs du système

Le système DreamPark doit permettre :

- de gérer les places de stationnement ;
- d'identifier les véhicules ;
- d'attribuer une place adaptée à chaque véhicule ;
- de gérer l'entrée et la sortie des véhicules ;
- de gérer les tickets ;
- de gérer les abonnements ;
- de gérer le pack garantie ;
- de proposer différents services aux abonnés ;
- de gérer la livraison des véhicules ;
- de conserver les informations relatives aux passages ;
- de consulter et éditer les statistiques du parking.

---

# 3. Acteurs

Les acteurs identifiés dans le système sont :

- **Client**
- **Abonné**
- **Super_Abonné**
- **Voiturier**
- **Administrateur**

## 3.1 Client

Le client utilise les services du parking.

Il peut notamment :

- entrer dans le parking ;
- garer sa voiture ;
- récupérer sa voiture ;
- souscrire à un abonnement.

## 3.2 Abonné

L'abonné est un client ayant souscrit à un abonnement.

Il peut bénéficier des services proposés par le parking, notamment :

- la maintenance ;
- l'entretien ;
- la livraison de son véhicule.

## 3.3 Super_Abonné

Le Super_Abonné correspond au client bénéficiant du pack garantie de stationnement.

Le pack permet au parking de garantir une solution de stationnement au client. Si nécessaire, le véhicule peut être garé dans un autre parking.

Le sujet précise également que l'inscription au pack garantie permet de bénéficier des services proposés aux abonnés.

## 3.4 Voiturier

Le voiturier intervient principalement dans le service de livraison.

Il peut récupérer et livrer le véhicule conformément à la demande du client.

## 3.5 Administrateur

L'administrateur intervient dans la consultation et l'exploitation des informations relatives à l'activité du parking.

Il peut notamment :

- consulter les statistiques ;
- éditer les statistiques.

---

# 4. Cas d'utilisation

Les principaux cas d'utilisation du système sont :

| Domaine | Cas d'utilisation | Acteur |
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

---

# 5. Fonctionnalité « Se garer »

## 5.1 Acteur

**Client**

## 5.2 Objectif

Permettre à un client de garer son véhicule dans une place adaptée du parking.

## 5.3 Préconditions

- Le client se présente à l'un des accès.
- Le véhicule peut être identifié par le système.
- Le parking est disponible.

## 5.4 Scénario nominal

1. Le client arrive devant l'un des accès.
2. La caméra récupère les informations du véhicule :
   - immatriculation ;
   - hauteur ;
   - longueur.
3. Le système détermine le statut du client.
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

## 5.5 Cas particulier : aucune place disponible

Lorsque le parking ne possède aucune place adaptée au véhicule :

- aucune place n'est attribuée ;
- le système informe le client qu'aucune place n'est disponible ;
- le véhicule n'est pas garé dans le parking.

---

# 6. Fonctionnalité « Reprendre la voiture »

## 6.1 Acteur

**Client**

## 6.2 Objectif

Permettre au client de récupérer son véhicule stationné dans le parking.

## 6.3 Préconditions

- Le véhicule est présent dans le parking.
- Le client possède le ticket correspondant.

## 6.4 Scénario nominal

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

## 6.5 Cas particuliers

### Livraison

Si le client a demandé une livraison, le système récupère le véhicule et organise sa livraison conformément à la demande.

### Entretien ou maintenance

Dans le cas d'une demande d'entretien ou de maintenance, le système prend en charge le véhicule et le gare à nouveau après la réalisation du service.

---

# 7. Fonctionnalité « S'abonner »

## 7.1 Acteur

**Client**

## 7.2 Objectif

Permettre à un client de souscrire à une formule d'abonnement proposée par le parking.

## 7.3 Scénario

1. Le client consulte les abonnements disponibles.
2. Il sélectionne une formule.
3. Le système enregistre son abonnement.
4. Un contrat est associé à l'abonnement.
5. Le client devient abonné.
6. Il peut alors bénéficier des services associés à son abonnement.

---

# 8. Fonctionnalité « Se désabonner »

## 8.1 Acteur

**Abonné**

## 8.2 Objectif

Permettre à un abonné de mettre fin à son abonnement.

## 8.3 Scénario

1. L'abonné demande la résiliation de son abonnement.
2. Le système identifie le contrat correspondant.
3. Le contrat est clôturé.
4. Le statut du client est mis à jour.

---

# 9. Fonctionnalité « Pack garantie »

Le parking propose un pack garantissant au client une solution de stationnement.

## 9.1 Inscription au pack garantie

Le client souscrit au pack garantie.

Le parking réserve une place pour le client.

Si aucune place n'est disponible dans le parking, le véhicule peut être stationné dans un autre parking.

Cette opération doit être transparente pour le client.

L'inscription au pack permet également de bénéficier des services proposés aux abonnés.

## 9.2 Désinscription du pack garantie

Le client peut demander la fin de son inscription au pack garantie.

Le système met alors à jour les informations correspondant à son abonnement.

---

# 10. Fonctionnalité « Demander une maintenance »

## 10.1 Acteur

**Abonné**

## 10.2 Scénario

1. L'abonné demande une maintenance.
2. Le système enregistre la demande.
3. Le véhicule est pris en charge.
4. La maintenance est réalisée.
5. Les informations relatives au service sont enregistrées.
6. Le véhicule est garé à nouveau après le service.

---

# 11. Fonctionnalité « Demander un entretien »

## 11.1 Acteur

**Abonné**

## 11.2 Scénario

1. L'abonné demande un entretien.
2. Le système enregistre la demande.
3. Le véhicule est pris en charge.
4. L'entretien est réalisé.
5. Les informations relatives au service sont enregistrées.
6. Le véhicule est garé à nouveau.

---

# 12. Fonctionnalité « Demander une livraison »

## 12.1 Acteur

**Abonné**

## 12.2 Informations nécessaires

La demande de livraison comprend notamment :

- une date ;
- une heure ;
- une adresse.

## 12.3 Scénario

1. L'abonné demande la livraison de son véhicule.
2. Le système enregistre la demande.
3. Le véhicule est récupéré.
4. Un voiturier prend en charge la livraison.
5. Le véhicule est livré à l'adresse et à l'heure demandées.

Le sujet précise également que le parking propose une politique de flexibilité permettant au client de modifier ses options de service par simple appel téléphonique.

---

# 13. Fonctionnalité « Effectuer la livraison »

## 13.1 Acteur

**Voiturier**

Le voiturier intervient pour réaliser une livraison demandée par un abonné.

Il prend en charge le véhicule et effectue la livraison conformément aux informations enregistrées dans la demande.

---

# 14. Gestion des places

Le système doit gérer l'ensemble des places du parking.

Chaque place possède notamment :

- un identifiant unique ;
- un numéro ;
- un niveau ;
- une longueur ;
- une hauteur ;
- un état indiquant si elle est libre ou occupée.

Lorsqu'un véhicule entre :

- une place compatible est recherchée ;
- la place est attribuée ;
- elle devient occupée.

Lorsqu'un véhicule sort :

- la place est libérée ;
- elle redevient disponible.

---

# 15. Gestion des véhicules

Le système doit conserver les informations nécessaires à l'identification des véhicules.

Une voiture possède notamment :

- une immatriculation ;
- une hauteur ;
- une longueur ;
- un état indiquant si elle se trouve dans le parking.

Une voiture peut être associée à un placement correspondant à son stationnement.

---

# 16. Gestion des accès

Le parking possède deux accès.

Chaque accès comprend :

- une caméra ;
- une borne à tickets-paiement ;
- un panneau d'affichage ;
- deux téléporteurs.

L'accès permet notamment de gérer l'entrée et la sortie des véhicules.

---

# 17. Gestion des tickets et du paiement

Lorsqu'une place est attribuée à un véhicule, la borne délivre un ticket.

Le ticket permet notamment d'actionner le système nécessaire à la récupération ou au stationnement du véhicule.

Lors de l'entrée, le système peut également déterminer :

- si le client possède un abonnement ;
- si une carte d'abonnement est nécessaire ;
- le mode de paiement utilisé.

Le sujet prévoit notamment le paiement en espèces ou par carte bancaire.

---

# 18. Gestion des panneaux d'affichage

Un panneau est situé au niveau de chacun des accès.

Il indique le nombre de places disponibles.

Lorsqu'une voiture entre :

**nombre de places disponibles → diminution**

Lorsqu'une voiture sort :

**nombre de places disponibles → augmentation**

Les panneaux doivent être actualisés en conséquence.

---

# 19. Gestion des statistiques

Le système conserve une trace des passages des véhicules.

Ces informations permettent notamment d'étudier :

- la fréquentation du parking ;
- l'activité du parking ;
- l'utilisation des différents services.

L'administrateur peut consulter ces statistiques et éditer l'activité du parking.

Le sujet indique que les statistiques peuvent être présentées sous différentes formes, notamment :

- documents texte ;
- HTML ;
- images pour les plans ;
- vidéo.

---

# 20. Règles fonctionnelles principales

Les principales règles fonctionnelles du système sont les suivantes :

### RF01 — Identification du véhicule

Le système doit pouvoir récupérer l'immatriculation, la hauteur et la longueur du véhicule à l'aide de la caméra.

### RF02 — Attribution d'une place

Le système doit attribuer une place compatible avec les dimensions du véhicule lorsqu'une place est disponible.

### RF03 — Parking complet

Lorsqu'aucune place adaptée n'est disponible, le système ne doit pas effectuer le stationnement normal du véhicule.

### RF04 — Mise à jour des places

L'entrée ou la sortie d'une voiture doit entraîner la mise à jour du nombre de places disponibles.

### RF05 — Ticket

Lorsqu'une place est attribuée, le système doit permettre la délivrance d'un ticket.

### RF06 — Services abonnés

Les abonnés doivent pouvoir bénéficier des services prévus par leur abonnement.

### RF07 — Pack garantie

Le pack garantie doit permettre de garantir une solution de stationnement au client, éventuellement dans un autre parking.

### RF08 — Livraison

Le système doit permettre de demander et d'effectuer la livraison d'un véhicule.

### RF09 — Statistiques

Le système doit conserver des informations permettant d'étudier la fréquentation du parking.

### RF10 — Administration

L'administrateur doit pouvoir consulter et éditer les statistiques.

---

# 21. Limites de cette spécification

Cette partie décrit le **