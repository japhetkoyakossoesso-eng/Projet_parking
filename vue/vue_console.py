"""
Vue console de l'application : affiche les menus et lit ce que tape l'utilisateur.
"""
from datetime import datetime

class VueConsole:
    """Tout ce qui s'affiche à l'écran ou se lit au clavier passe par cette classe."""

    def afficher(self, texte=""):
        """Affiche une ligne de texte."""
        print(texte)

    def titre(self, texte):
        """Affiche un titre, précédé d'une ligne vide."""
        print()
        print(texte)

    
    def menuPrincipal(self):
       
        self.titre("DreamPark : menu principal")
        print("Où souhaitez-vous aller ?")
        print("1. Nouveau client")
        print("2. Se garer")
        print("3. S'abonner")
        print("4. Reprendre ma voiture")
        print("5. Demander un service")
        print("6. Modifier une livraison")
        print("7. Voir l'état du parking")
        print("8. Voir les clients")
        print("0. Quitter")
        return input("Votre choix : ").strip()


    def demanderTexte(self, question):
        """:return: le texte saisi, non vide (str)"""
        while True:
            reponse = input(question).strip()
            if reponse:
                return reponse
            print("Ce champ ne peut pas être vide.")

    def demanderNombre(self, question):
        """:return: le nombre saisi (float) ; redemande tant que la saisie est invalide"""
        while True:
            reponse = input(question).strip().replace(",", ".")
            try:
                return float(reponse)
            except ValueError:
                print("Veuillez entrer un nombre (par exemple 1.80).")

    def demanderEntier(self, question, mini, maxi):
        """:return: un entier entre mini et maxi (int)"""
        while True:
            reponse = input(question).strip()
            if reponse.isdigit() and mini <= int(reponse) <= maxi:
                return int(reponse)
            print(f"Veuillez entrer un nombre entre {mini} et {maxi}.")

    def demanderOuiNon(self, question):
        """:return: True pour oui, False pour non"""
        while True:
            reponse = input(question + " (o/n) : ").strip().lower()
            if reponse in ("o", "oui"):
                return True
            if reponse in ("n", "non"):
                return False
            print("Répondez par o ou n.")

    def afficherListe(self, lignes):
        """Affiche une liste numérotée à partir de 1."""
        for i, ligne in enumerate(lignes, start=1):
            print(f"  {i}. {ligne}")

    def demanderDate(self, question):
        """:return: la date saisie au format jj/mm/aaaa (date)"""
        while True:
            reponse = input(question + " (jj/mm/aaaa) : ").strip()
            try:
                return datetime.strptime(reponse, "%d/%m/%Y").date()
            except ValueError:
                print("Date invalide, exemple : 25/12/2026.")
