# Nom de l'équipe :  404 Places Not Found — Système de gestion de parking DreamPark
# Membres de l'équipe : KOYAKOSSO-ESSO Japhet et Mohamed-Ramzi Ayachi


Projet Python, L3 MIASHS parcours Informatique(UT2J), implémentation du sujet "Projet de Système de
gestion de parking" à partir du diagramme UC et du diagramme de classes fournis.

## Structure du projet 

```
parking_project/
├── parking/                 # le package principal
│   ├── place.py             # Place
│   ├── voiture.py           # Voiture
│   ├── placement.py         # Placement (association Voiture <-> Place)
│   ├── contrat.py           # Contrat
│   ├── abonnement.py        # Abonnement
│   ├── services.py          # Service (abstraite), Maintenance, Entretien, Livraison
│   ├── voiturier.py         # Voiturier
│   ├── client.py            # Client
│   ├── camera.py            # Camera
│   ├── borne_ticket.py      # BorneTicket
│   ├── teleporteur.py       # Teleporteur
│   ├── panneau_affichage.py # PanneauAffichage
│   ├── acces.py             # Acces (orchestre "Se garer" et "Reprendre la voiture")
│   ├── parking.py           # Parking (singleton)
│   └── statistiques.py      # Statistiques (Partie 3)
├── tests/
│   ├── test_unites_base.py      # Place, Voiture, Placement, Abonnement, Contrat
│   └── test_parking_acces.py    # Parking (singleton), use cases, services abonnés
├── main.py                  # menu console de démonstration
├── gui.py                   # interface graphique Tkinter (Partie 4)
└── README.md
```

## Dépôts

Le projet sera déposé à la fois sur GitLab et GitHub.