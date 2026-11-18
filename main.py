"""
Point d'entrée de l'application DreamPark.

Partie 1 : menu console pour le use case « Se garer ».
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
    for texte in ctrl.panneaux():
        vue.afficher(f"Panneau : {texte}")


def sAbonner(vue, ctrl):
    """Abonne un client choisi à une formule."""
    vue.titre("S'abonner")
    client = choisirClient(vue, ctrl)
    if client is None:
        return
    ctrl.sAbonner(client, choisirAbonnement(vue, ctrl))
    vue.afficher(f"{client.nom} est maintenant {ctrl.statut(client)}.")


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
    actions = {"1": nouveauClient, "2": seGarer, "3": sAbonner,
               "4": etatParking, "5": voirClients}
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
