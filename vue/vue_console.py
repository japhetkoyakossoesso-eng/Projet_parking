"""
Vue console de l'application : affiche les menus et lit ce que tape l'utilisateur.
"""


class VueConsole:
    """Tout ce qui s'affiche à l'écran ou se lit au clavier passe par cette classe."""

    def afficher(self, texte=""):
        """Affiche une ligne de texte."""
        print(texte)

    def titre(self, texte):
        """Affiche un titre encadré."""
        print()
        print("=" * 50)
        print(texte)
        print("=" * 50)

    def menuPrincipal(self):
        """
        Affiche le menu principal.

        :return: le choix de l'utilisateur (str)
        """
        self.titre("DreamPark : menu principal")
        print("1. Nouveau client")
        print("2. Se garer")
        print("3. S'abonner")
        print("4. Voir l'état du parking")
        print("5. Voir les clients")
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
