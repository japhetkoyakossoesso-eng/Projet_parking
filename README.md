# Projet_parking : DreamPark

Système de gestion du parking automatisé DreamPark, réalisé en Python dans le cadre de la L3 MIASHS (parcours Informatique et SHS) à l'Université Toulouse 2 Jean-Jaurès.

Équipe 404 Places Not Found : Japhet KOYAKOSSO ESSO, Ayachi Mohamed.

---

## 1. Ce qu'il faut installer

### Obligatoire

| Outil | Version | Pourquoi |
|---|---|---|
| Python | 3.10 ou plus | Le langage du projet |
| Git | toute version récente | Récupérer le dépôt et changer de branche |

Le projet n'utilise que la bibliothèque standard de Python, donc il n'y a aucun paquet à installer avec `pip` pour le faire tourner. Les modules utilisés sont déjà fournis avec Python :

| Module | Utilisation dans le projet |
|---|---|
| `unittest` | Les tests unitaires (dossier `tests/`) |
| `pydoc` | La génération de la documentation à partir des docstrings |
| `datetime` | Les dates des placements, contrats et services |
| `json` ou `sqlite3` | La persistance des données (choix fait lors de l'implémentation) |
| `tkinter` | L'interface graphique (Partie 4) |

### Installer Python et Git

Windows :
1. Télécharger Python sur https://www.python.org/downloads/ et cocher « Add Python to PATH » pendant l'installation. Tkinter est inclus.
2. Télécharger Git sur https://git-scm.com/download/win.

macOS :
```bash
brew install python git
```
Si `brew` n'est pas installé, Python est aussi disponible sur https://www.python.org/downloads/. Tkinter est inclus.

Linux (Ubuntu, Debian) :
```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk git
```
Sous Linux, `python3-tk` est nécessaire pour l'interface graphique, car tkinter n'est pas toujours installé avec Python.

Pour vérifier que tout est en place :
```bash
python3 --version
git --version
python3 -c "import tkinter; print('tkinter OK')"
```
Sous Windows, remplacez `python3` par `python` dans toutes les commandes de ce fichier.

### Facultatif mais pratique

| Outil | Installation | À quoi il sert |
|---|---|---|
| Un éditeur : VS Code (avec l'extension Python) ou PyCharm Community | Sites officiels | Écrire le code, lancer les tests en un clic |
| `coverage` | `pip install coverage` | Mesurer quelle part du code les tests exécutent |
| `pylint` ou `flake8` | `pip install pylint` | Relire le code automatiquement (nommage, style, erreurs fréquentes) |

Ces outils ne sont pas nécessaires pour lancer le projet.

---

## 2. Récupérer le projet

Le dépôt est hébergé sur le GitLab de l'université (https://mi-git.univ-tlse2.fr/).

```bash
git clone <adresse-du-depot> Projet_parking
cd Projet_parking
```

Chaque partie du projet est livrée sur sa propre branche :

| Branche | Contenu |
|---|---|
| `partie0` | Spécification fonctionnelle et spécification des tests |
| `partie1` | Use case « Se garer » |
| `partie2` | Use case « Reprendre la voiture » |
| `partie3` | Gestion des statistiques |
| `partie4` | Interface graphique |

Pour passer sur une branche :
```bash
git checkout partie1
```

---

## 3. Environnement virtuel (conseillé)

Un environnement virtuel isole les outils facultatifs (`coverage`, `pylint`) du reste de votre ordinateur.

```bash
python3 -m venv .venv
```

Pour l'activer :
- Linux ou macOS : `source .venv/bin/activate`
- Windows : `.venv\Scripts\activate`

Puis, si vous voulez les outils facultatifs :
```bash
pip install coverage pylint
```

Pour le désactiver : `deactivate`. Le dossier `.venv/` ne doit pas être envoyé sur git (il est dans le `.gitignore`).

---

## 4. Lancer le projet

Depuis le dossier `Projet_parking` :

```bash
python3 main.py
```

Le menu console (Partie 1) permet de :
1. créer un client et sa voiture ;
2. se garer par l'accès 1 ou 2 (ticket, paiement, abonnement proposé à la borne) ;
3. s'abonner (formule « Mensuel » ou « Pack garantie ») ;
4. voir l'état du parking (panneau et places) ;
5. voir les clients, leur statut et où est leur voiture.

Le parking de démonstration a 2 niveaux (A et B) de 5 places de tailles différentes. Les places A5 et B5 sont les seules assez grandes pour une voiture de 2.40 m x 5.90 m : c'est pratique pour tester le parking plein et le parking partenaire.

---

## 5. Lancer les tests

Tous les tests :
```bash
python3 -m unittest discover tests -v
```

Un seul fichier de tests :
```bash
python3 -m unittest tests.test_parking -v
```

Un seul test :
```bash
python3 -m unittest tests.test_parking.TestParking.test_parking_est_un_singleton
```

Mesurer la couverture des tests (si `coverage` est installé) :
```bash
coverage run -m unittest discover tests
coverage report -m
```

Sur la branche `partie1`, la commande affiche « OK (skipped=32) » : les tests du use case « Se garer » passent, et les 32 tests de `test_client.py` et `test_services.py` restent en pause (`@unittest.skip`) pour la Partie 2.

Pensez à relancer tous les tests avant chaque commit, pour vérifier qu'une modification n'a rien cassé.

---

## 6. Générer la documentation

La documentation est générée à partir des docstrings avec pydoc, sans rien installer.

Afficher la documentation d'un module dans le terminal :
```bash
python3 -m pydoc modele.parking
```

Créer une page HTML (le fichier `modele.parking.html` apparaît dans le dossier courant) :
```bash
python3 -m pydoc -w modele.parking
```

Parcourir toute la documentation dans le navigateur :
```bash
python3 -m pydoc -b
```

---

## 7. Organisation du dépôt

```
Projet_parking/
├── main.py                # point d'entrée de l'application
├── README.md
├── docs/
│   ├── Partie0_Specification.md
│   └── Partie1_Rapport.md
├── modele/                # classes métier
│   ├── __init__.py
│   ├── parking.py         # Parking, Place, Placement
│   ├── client.py          # Client, Voiture, Abonnement, Contrat
│   ├── services.py        # Service, Maintenance, Entretien, Livraison, Voiturier
│   ├── acces.py           # Acces, Camera, BorneTicket, PanneauAffichage, Teleporteur
│   └── exceptions.py      # PlaceOccupeeError, PlaceIncompatibleError...
├── vue/                   # affichage console puis interface tkinter
│   ├── __init__.py
│   └── vue_console.py     # VueConsole : menus et saisies au clavier
├── controleur/            # lien entre la vue et le modèle
│   ├── __init__.py
│   └── controleur_parking.py  # ControleurParking : parking de démonstration, actions du menu
├── persistance/           # sauvegarde et chargement des données
│   └── __init__.py
└── tests/                 # tests unittest
    ├── __init__.py
    ├── test_parking.py            # TestParking
    ├── test_place.py              # TestPlace
    ├── test_placement.py          # TestPlacement
    ├── test_voiture.py            # TestVoiture
    ├── test_camera.py             # TestCamera
    ├── test_borne_ticket.py       # TestBorneTicket
    ├── test_panneau_affichage.py  # TestPanneauAffichage
    ├── test_teleporteur.py        # TestTeleporteur
    ├── test_acces.py              # TestAcces (intégration, avec Mock)
    ├── test_controleur.py         # « Se garer » de bout en bout
    ├── test_client.py             # en pause, Partie 2
    └── test_services.py           # en pause, Partie 2
```

Les fichiers `__init__.py` ne contiennent qu'une docstring. Ils permettent d'importer les classes d'un dossier à l'autre, par exemple `from modele.parking import Parking` dans les tests.

L'application suit le patron MVC : le modèle ne connaît ni la vue ni le contrôleur, ce qui permet de le tester seul.

---

## 8. Problèmes fréquents

| Problème | Solution |
|---|---|
| `python3` n'est pas reconnu sous Windows | Utiliser `python`, ou réinstaller Python en cochant « Add Python to PATH » |
| `ModuleNotFoundError: No module named 'modele'` | Lancer la commande depuis le dossier `Projet_parking`, et vérifier que chaque dossier contient un fichier `__init__.py` |
| `No module named 'tkinter'` sous Linux | `sudo apt install python3-tk` |
| `pip` refuse d'installer (« externally managed environment ») | Créer et activer l'environnement virtuel de la section 3, puis relancer `pip install` |
