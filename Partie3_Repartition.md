# Partie 3 : « Gestion des statistiques » : qui fait quoi

On continue d'alterner les rôles (P1 : Japhet modèle, P2 : Mohamed modèle) :

- **Japhet (KOYAKOSSO ESSO) : le modèle**, le contrôleur, le menu et les vues d'édition.
- **Mohamed (Ayachi Mohamed Ramzi) : les tests.**

On part d'une copie de la Partie 2. Comme prévu en Partie 0, on n'ajoute **pas de classe Statistiques** : les placements terminés (gardés par `historiquePassages()`) sont déjà la trace de passage. Les calculs vont dans `Parking`, l'édition des documents va dans la **vue** (MVC).

## 1. Les nouvelles méthodes (à respecter par les deux)

### Dans le modèle (`modele/parking.py`)

| Classe | Méthode | Ce qu'elle fait | Ce qu'elle renvoie |
|---|---|---|---|
| `Parking` | `nbPassages(debut=None, fin=None)` | Compte les placements commencés entre `debut` et `fin` (bornes incluses ; `None` = pas de limite) | un `int` |
| `Parking` | `passagesParJour()` | Regroupe les placements par jour d'entrée | un `dict` {`date`: nombre} |
| `Parking` | `dureeMoyenneStationnement()` | Moyenne des durées des placements **terminés** | des minutes (`float`), ou `None` s'il n'y en a aucun |
| `Parking` | `tauxOccupation()` | Places occupées / nombre de places | un `float` entre 0 et 1 (0 si aucune place) |
| `Parking` | `historiqueVoiture(immat)` | Les passages d'une voiture, du plus ancien au plus récent | une liste de `Placement` (vide si inconnue) |
| `Parking` | `clientsReguliers(clients, seuil)` | Les clients **non abonnés** avec `nbFrequentations >= seuil` (à qui proposer un abonnement) | une liste de `Client` |
| `Parking` | `activiteParService(clients)` | Compte les services demandés par type | `{"Maintenance": n, "Entretien": n, "Livraison": n}` |

`clients` est la liste des clients que tient le contrôleur (le parking ne connaît pas les clients). Un `seuil` < 1 lève `ValueError`.

### Dans la vue (`vue/edition.py`, nouveau)

Une classe mère `Edition` avec `editer(stats, chemin)` qui écrit un fichier et renvoie son chemin, et trois sous-classes (un format = une classe) :

| Classe | Fichier produit |
|---|---|
| `EditionTexte` | `.txt` lisible |
| `EditionHTML` | `.html` avec un tableau des chiffres |
| `EditionImage` | `.svg` : plan du parking (places libres en vert, occupées en rouge) |

`stats` est le dictionnaire renvoyé par le contrôleur (section 3). Pas de bibliothèque externe : le SVG est du texte.

### Dans le contrôleur

- `ControleurParking.statistiques()` → `dict` avec les clés `nbPassages`, `passagesParJour`, `dureeMoyenne`, `tauxOccupation`, `clientsReguliers`, `activiteParService`, `places` (liste de `(idPlace, estLibre)` pour le plan).
- `ControleurParking.editerStatistiques(format, chemin)` avec `format` dans `"texte"`, `"html"`, `"image"` → chemin du fichier ; autre format → `ValueError`.

Menu : deux nouveaux choix, « Consulter les statistiques » et « Éditer les statistiques » (on choisit le format).

Règle commune (comme en P1 et P2) : un cas normal (aucun passage, voiture inconnue) renvoie 0, `None` ou une liste vide ; une erreur de programmation lève une exception.

## 2. Travail de Mohamed : les tests

**Astuce pour les dates** : `Placement` met `datetime.now()` dans `dateDebut`. Pour avoir des durées et des jours précis, crée le placement normalement puis modifie `placement.dateDebut` / `placement.dateFin` à la main dans le test.

### a) `tests/test_statistiques.py` (contexte : parking de 3 places A1, A2, A3)

| Test | Cas | Résultat attendu |
|---|---|---|
| `test_nbPassages_parking_vide` | aucun passage | 0 |
| `test_nbPassages_compte_en_cours_et_termines` | 1 voiture sortie + 1 garée | 2 |
| `test_nbPassages_entre_deux_dates` | passages le 1er, le 5 et le 10 ; période du 1er au 5 | 2 (bornes incluses) |
| `test_passagesParJour` | 2 passages le même jour, 1 le lendemain | `{jour1: 2, jour2: 1}` |
| `test_dureeMoyenne_aucun_placement_termine` | une voiture encore garée | `None` |
| `test_dureeMoyenne_deux_placements` | durées 30 min et 90 min | `60.0` |
| `test_dureeMoyenne_ignore_en_cours` | 1 terminé (30 min) + 1 en cours | `30.0` |
| `test_tauxOccupation_vide` | aucune voiture | `0.0` |
| `test_tauxOccupation_plein` | 3 voitures | `1.0` |
| `test_tauxOccupation_partiel` | 1 voiture sur 3 | `assertAlmostEqual(…, 1/3)` |
| `test_historiqueVoiture_ordre` | entrer, sortir, entrer | 2 placements, le plus ancien d'abord |
| `test_historiqueVoiture_inconnue` | plaque jamais vue | `[]` |
| `test_clientsReguliers_seuil_atteint` | non abonné avec 2 passages, seuil 2 | il est dans la liste (valeur limite) |
| `test_clientsReguliers_sous_le_seuil` | 1 passage, seuil 2 | liste vide |
| `test_clientsReguliers_exclut_abonnes` | abonné avec 3 passages | pas dans la liste |
| `test_clientsReguliers_seuil_invalide` | seuil 0 | `ValueError` |
| `test_activiteParService` | 1 maintenance, 2 livraisons | `{"Maintenance": 1, "Entretien": 0, "Livraison": 2}` |
| `test_activiteParService_aucun_client` | liste vide | les 3 clés à 0 |

### b) `tests/test_edition.py`

Utiliser `tempfile.TemporaryDirectory()` dans `setUp` pour ne pas salir le dossier, et un petit dictionnaire `stats` écrit à la main.

| Test | Résultat attendu |
|---|---|
| `test_edition_texte_cree_fichier` | le fichier existe, contient le nombre de passages |
| `test_edition_html_contient_tableau` | le fichier contient `<table>` et le taux d'occupation |
| `test_edition_image_svg` | le fichier commence par `<svg`, un rectangle par place |
| `test_edition_image_couleurs` | place libre → vert, place occupée → rouge |
| `test_edition_renvoie_chemin` | `editer` renvoie le chemin donné |

### c) `tests/test_controleur.py` (compléter)

- `test_statistiques_cles` : `statistiques()` contient les 7 clés ;
- `test_editer_format_inconnu` : `editerStatistiques("pdf", …)` lève `ValueError`.

### d) Les règles

- un test = un seul cas, nom clair + docstring ;
- `setUp` crée le contexte, `tearDown` appelle `Parking._reinitialiser()` ;
- les tests sont écrits avant le code : ils échouent tant que Japhet n'a pas fini, c'est normal.

## 3. Travail de Japhet : le modèle

1. les 7 méthodes de `Parking` avec docstrings ;
2. `vue/edition.py` (les 3 formats) ;
3. `statistiques()` et `editerStatistiques()` dans le contrôleur, les 2 choix du menu ;
4. rapport Partie 3 (ajouts au diagramme justifiés : méthodes de `Parking`, classes `Edition`).

## 4. À la fin

`python3 -m unittest discover -s tests -v` doit afficher **OK**, avec les 134 tests de la Partie 2 toujours verts.
