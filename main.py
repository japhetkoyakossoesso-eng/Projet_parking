"""
Point d'entrée de l'application DreamPark.

Partie 2 : menus « Se garer », « Reprendre la voiture » et services. »
Lancement : python3 main.py (python main.py sous Windows).
"""

from controleur.controleur_parking import ControleurParking
from vue.vue_console import VueConsole


def choisirClient(vue, ctrl):
    """
    Fait choisir un client dans la liste.

    :return: le client choisi (Client), ou None s'il n'y a aucun client
    """
    if not ctrl.clients:
        vue.afficher("Aucun client : créez-en un avec le choix 1.")
        return None
    vue.afficherListe([f"{c.nom} ({c.maVoiture.immatriculation})" for c in ctrl.clients])
    return ctrl.getClient(vue.demanderEntier("Numéro du client : ", 1, len(ctrl.clients)))


def choisirAbonnement(vue, ctrl):
    """:return: la formule choisie (Abonnement)"""
    vue.afficherListe([f"{ab.libelle} ({ab.prix} €)" for ab in ctrl.abonnements])
    return ctrl.getAbonnement(vue.demanderEntier("Numéro de la formule : ", 1, len(ctrl.abonnements)))


def nouveauClient(vue, ctrl):
    """Crée un client et sa voiture à partir des saisies."""
    vue.titre("Nouveau client")
    nom = vue.demanderTexte("Nom : ")
    adresse = vue.demanderTexte("Adresse : ")
    immat = vue.demanderTexte("Immatriculation (ex. AB-123-CD) : ").upper()
    hauteur = vue.demanderNombre("Hauteur de la voiture en mètres : ")
    longueur = vue.demanderNombre("Longueur de la voiture en mètres : ")
    try:
        client = ctrl.nouveauClient(nom, adresse, immat, hauteur, longueur)
        vue.afficher(f"Client {client.nom} créé.")
    except ValueError as e:
        vue.afficher(f"Erreur : {e}")


def seGarer(vue, ctrl):
    """Déroule le use case « Se garer » pour un client choisi."""
    vue.titre("Se garer")
    client = choisirClient(vue, ctrl)
    if client is None:
        return
    if ctrl.estDejaGare(client):
        vue.afficher(f"La voiture de {client.nom} est déjà garée ({ctrl.lieu(client)}).")
        return
    numAcces = vue.demanderEntier("Par quel accès entrez-vous (1 ou 2) ? ", 1, 2)
    vue.afficher(f"Carte lue : {ctrl.statut(client)}")

    # Pas de place pour cette voiture : on le dit tout de suite, avec la raison,
    # sans demander de payer (un super-abonné, lui, part au parking partenaire).
    raison = ctrl.raisonRefus(client)
    if raison is not None and not client.estSuperAbonne:
        vue.afficher(f"Accès refusé : {raison}")
        return

    for texte in ctrl.textesBorne(client, numAcces):
        vue.afficher(texte)

    modePaiement, choixAbonnement = "CB", None
    if not client.estAbonne:
        modePaiement = "CB" if vue.demanderEntier("Paiement : 1. CB  2. Espèces : ", 1, 2) == 1 else "espèces"
        if vue.demanderOuiNon("Voulez-vous prendre un abonnement ?"):
            choixAbonnement = choisirAbonnement(vue, ctrl)

    reussi, message = ctrl.seGarer(client, numAcces, modePaiement, choixAbonnement)
    vue.afficher(message)
    if reussi:
        vue.afficher(f"Voiture garée : {ctrl.lieu(client)}")
    for numero, texte in enumerate(ctrl.panneaux(), start=1):
        vue.afficher(f"Panneau de l'accès {numero} : {texte}")


def sAbonner(vue, ctrl):
    """Abonne un client choisi à une formule."""
    vue.titre("S'abonner")
    client = choisirClient(vue, ctrl)
    if client is None:
        return
    ctrl.sAbonner(client, choisirAbonnement(vue, ctrl))
    vue.afficher(f"{client.nom} est maintenant {ctrl.statut(client)}.")

def reprendreVoiture(vue, ctrl):
    """Déroule le use case « Reprendre la voiture » pour un client choisi."""
    vue.titre("Reprendre ma voiture")
    client = choisirClient(vue, ctrl)
    if client is None:
        return
    if not client.maVoiture.estDansParking and ctrl.lieu(client) != "parking partenaire":
        vue.afficher(f"La voiture de {client.nom} n'est pas garée.")
        return
    numAcces = vue.demanderEntier("Par quel accès sortez-vous (1 ou 2) ? ", 1, 2)
    ticket = None
    if not client.estSuperAbonne:
        ticket = vue.demanderTexte("Votre ticket (ex. A1-AB123CD-0930) : ")
    reussi, message = ctrl.sortir(client, numAcces, ticket)
    vue.afficher(message)
    for numero, texte in enumerate(ctrl.panneaux(), start=1):
        vue.afficher(f"Panneau de l'accès {numero} : {texte}")


def demanderService(vue, ctrl):
    """Fait demander un service (maintenance, entretien, livraison) à un client."""
    vue.titre("Demander un service")
    client = choisirClient(vue, ctrl)
    if client is None:
        return
    vue.afficherListe(["Maintenance", "Entretien", "Livraison"])
    choix = vue.demanderEntier("Service : ", 1, 3)
    if choix == 3:
        dateLiv = vue.demanderDate("Date de livraison")
        heure = vue.demanderEntier("Heure de livraison (0-23) : ", 0, 23)
        adresse = vue.demanderTexte("Adresse de livraison : ")
        reussi, message = ctrl.demanderService(client, "livraison", dateLiv, heure, adresse)
    else:
        typeService = ["maintenance", "entretien"][choix - 1]
        reussi, message = ctrl.demanderService(client, typeService)
    vue.afficher(message)


def modifierLivraison(vue, ctrl):
    """Modifie la livraison en attente d'un client."""
    vue.titre("Modifier une livraison")
    client = choisirClient(vue, ctrl)
    if client is None:
        return
    dateLiv = vue.demanderDate("Nouvelle date")
    heure = vue.demanderEntier("Nouvelle heure (0-23) : ", 0, 23)
    adresse = vue.demanderTexte("Nouvelle adresse : ")
    reussi, message = ctrl.modifierLivraison(client, dateLiv, heure, adresse)
    vue.afficher(message)

def etatParking(vue, ctrl):
    """Affiche les panneaux et l'état de chaque place."""
    vue.titre("État du parking")
    vue.afficher(f"Panneau : {ctrl.panneaux()[0]}")
    vue.afficher()
    for ligne in ctrl.etatPlaces():
        vue.afficher(ligne)


def voirClients(vue, ctrl):
    """Affiche les clients, leur statut et où est leur voiture."""
    vue.titre("Clients")
    if not ctrl.clients:
        vue.afficher("Aucun client.")
        return
    vue.afficherListe([f"{c.nom} : {c.maVoiture.immatriculation}, {ctrl.statut(c)}, {ctrl.lieu(c)}"
                       for c in ctrl.clients])


def main():
    """Lance l'application DreamPark."""
    vue = VueConsole()
    ctrl = ControleurParking()
    actions = {  "1": nouveauClient,"2": seGarer, 
                 "3": sAbonner,"4": reprendreVoiture, 
                 "5": demanderService,"6": modifierLivraison, 
                 "7": etatParking,"8": voirClients
               }
    while True:
        try:
            choix = vue.menuPrincipal()
        except (EOFError, KeyboardInterrupt):
            choix = "0"
        if choix == "0":
            vue.afficher("Au revoir !")
            break
        if choix in actions:
            try:
                actions[choix](vue, ctrl)
            except (EOFError, KeyboardInterrupt):
                vue.afficher("\nAction annulée.")
        else:
            vue.afficher("Choix inconnu.")


if __name__ == '__main__':
    main()
