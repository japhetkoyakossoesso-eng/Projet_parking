# Projet DreamPark : Partie 3

## Gestion des statistiques

**Équipe :** 404 Places Not Found  
**Membres :** Japhet KOYAKOSSO ESSO (modèle), Ayachi Mohamed Ramzi (tests)  
**Formation :** L3 MIASHS, parcours Informatique et SHS  
**Université Toulouse 2 Jean-Jaurès**

---

## 1. Ce que fait cette partie

Dans cette partie on a réalisé les use cases « Consulter les statistiques » et « Éditer les statistiques » de l'administrateur.

Le système garde déjà une trace de chaque passage : depuis la Partie 1, un placement terminé n'est pas supprimé, il reste dans la liste des placements de sa place. La Partie 3 se sert de cette trace pour calculer :

- le nombre de passages, en tout ou sur une période ;
- le nombre de passages par jour ;
- la durée moyenne de stationnement ;
- le taux d'occupation du parking en ce moment ;
- l'historique d'une voiture ;
- les clients réguliers qui ne sont pas abonnés, à qui on peut proposer un abonnement ;
- l'activité du parking par service (maintenance, entretien, livraison).

L'administrateur peut afficher ces chiffres à l'écran, ou les enregistrer dans un fichier texte, une page HTML ou une image du plan du parking (SVG). Le sujet parle de documents de différents types : on a fait un format par classe, pour pouvoir en ajouter un autre sans toucher au reste.

## 2. Ce qui a été fait

| Dossier | Contenu |
|---|---|
| modele/ | 7 méthodes de statistiques dans Parking (voir section 5) |
| vue/ | Nouveau fichier edition.py : Edition et ses 3 sous-classes (texte, HTML, image) ; menu à 11 choix |
| controleur/ | statistiques() et editerStatistiques(format, chemin) |
| main.py | 2 nouvelles actions de menu |
| tests/ | test_statistiques.py, test_edition.py, compléments de test_controleur.py |

## 3. Le menu console

```
1. Nouveau client
2. Se garer
3. S'abonner
4. Reprendre ma voiture
5. Demander un service
6. Modifier une livraison
7. Réaliser les services en attente
8. Voir l'état du parking
9. Voir les clients
10. Consulter les statistiques
11. Éditer les statistiques
0. Quitter
```

Le choix 10 affiche les statistiques à l'écran. Le choix 11 demande le format (texte, page web ou plan du parking) puis le nom du fichier, sans l'extension : le programme l'ajoute lui-même. Si le fichier ne peut pas être écrit (dossier inexistant par exemple), on affiche un message au lieu de planter.

Exemple de fichier texte obtenu après deux passages de la même voiture :

```
DreamPark : statistiques

Nombre de passages : 2
Durée moyenne de stationnement : 30.0 min
Taux d'occupation : 10 %

Passages par jour :
  24/11/2026 : 2

Activité par service :
  Maintenance : 0
  Entretien : 0
  Livraison : 0

Clients réguliers à qui proposer un abonnement :
  aucun
```

Sur le plan SVG, chaque niveau est une ligne et chaque place un rectangle portant son identifiant : vert si la place est libre, rouge si elle est occupée.

Un client est considéré comme régulier à partir de 3 passages (constante SEUIL_REGULIER du contrôleur, facile à changer).

## 4. Les tests

Commande :

```
python3 -m unittest discover -s tests -v
```

Résultat : *à compléter quand les tests de Mohamed sont ajoutés* (les 134 tests des parties précédentes passent toujours).

| Fichier | Ce qui est vérifié |
|---|---|
| test_statistiques.py | Nombre de passages (parking vide, en cours et terminés, entre deux dates avec bornes incluses), passages par jour, durée moyenne (aucun placement terminé, deux placements, placement en cours ignoré), taux d'occupation (vide, plein, partiel), historique d'une voiture (ordre, voiture inconnue), clients réguliers (seuil atteint, sous le seuil, abonnés exclus, seuil invalide), activité par service |
| test_edition.py | Chaque format crée bien son fichier ; le HTML contient un tableau ; le SVG a un rectangle par place, vert ou rouge selon l'état ; editer renvoie le chemin |
| test_controleur.py | statistiques() contient toutes les clés ; un format inconnu lève ValueError |

Pour tester des durées précises, les tests créent un placement normalement puis modifient dateDebut et dateFin à la main : sinon toutes les dates valent « maintenant » et les durées sont nulles.

## 5. Modifications par rapport aux artefacts de modélisation

| Ajout | Pourquoi |
|---|---|
| Parking.nbPassages(debut, fin) | Compter la fréquentation, sur toute la vie du parking ou sur une période |
| Parking.passagesParJour() | Voir quels jours le parking est le plus utilisé (réaménagements futurs) |
| Parking.dureeMoyenneStationnement() | Ne compte que les placements terminés : un placement en cours n'a pas encore de durée. Renvoie None s'il n'y en a aucun |
| Parking.tauxOccupation() | Indicateur simple de remplissage, entre 0 et 1 |
| Parking.historiqueVoiture(immat) | La trace de passage d'une voiture précise, du plus ancien au plus récent |
| Parking.clientsReguliers(clients, seuil) | Le sujet demande de proposer des abonnements aux clients les plus réguliers : on ne garde que les non abonnés |
| Parking.activiteParService(clients) | Le sujet demande l'activité du parking selon les différents services |
| Edition, EditionTexte, EditionHTML, EditionImage (vue) | L'édition sous plusieurs formats relève de la vue. Une sous-classe par format : on redéfinit seulement contenu(stats), editer() est commune |
| ControleurParking.statistiques(), editerStatistiques() | MVC : la vue ne lit pas le modèle directement, elle reçoit un dictionnaire préparé par le contrôleur |

On n'a pas ajouté de classe Statistiques dans le modèle, comme annoncé en Partie 0 : les placements conservés sont déjà la trace de passage, et les calculs portent sur l'ensemble du parking, donc ils vont dans Parking. Le parking ne connaît pas la liste des clients (c'est le contrôleur qui la tient) : clientsReguliers et activiteParService la reçoivent donc en paramètre.

Comme dans les parties précédentes, un cas normal (aucun passage, voiture inconnue) renvoie 0, None ou une liste vide, et seule une erreur de programmation (seuil inférieur à 1, format inconnu) lève une exception.

**Limite connue :** une voiture de super-abonné garée au parking partenaire n'a pas de placement chez nous, donc elle n'apparaît pas dans les statistiques de passages. On l'a laissé ainsi car ce passage a lieu dans un autre parking.

## 6. Répartition du travail

| Membre | Travail |
|---|---|
| Japhet KOYAKOSSO ESSO | Les 7 méthodes du modèle, vue edition.py, contrôleur, menu, rapport |
| Ayachi Mohamed Ramzi | test_statistiques.py, test_edition.py, compléments de test_controleur.py |
| Les deux | Choix des noms des méthodes (Partie3_Repartition.md), mise en commun et exécution de tous les tests |

## 7. Suite

La Partie 4 sera l'interface graphique. Elle pourra réutiliser directement statistiques() et editerStatistiques() du contrôleur, et afficher le plan du parking à partir de la même liste de places que le SVG.
