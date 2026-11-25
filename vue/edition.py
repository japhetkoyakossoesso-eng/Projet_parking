"""
Édition des statistiques sous plusieurs formats (texte, HTML, image SVG).

Ces classes font partie de la vue (MVC) : elles ne calculent rien, elles mettent
en forme le dictionnaire de statistiques fourni par le contrôleur.
"""
from html import escape


class Edition:
    """
    Classe mère des éditions : un format de document = une sous-classe.

    stats est un dictionnaire avec les clés nbPassages, passagesParJour,
    dureeMoyenne, tauxOccupation, clientsReguliers, activiteParService, places.
    """

    extension = ""

    def contenu(self, stats):
        """:return: le texte du document (str). À redéfinir dans chaque sous-classe."""
        raise NotImplementedError

    def editer(self, stats, chemin):
        """
        Écrit le document dans un fichier.

        :param stats: le dictionnaire de statistiques
        :param chemin: chemin du fichier à créer
        :return: le chemin du fichier écrit
        """
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(self.contenu(stats))
        return chemin


def _duree(stats):
    """:return: la durée moyenne lisible (str)"""
    d = stats["dureeMoyenne"]
    return "aucun passage terminé" if d is None else f"{d:.1f} min"


def _taux(stats):
    """:return: le taux d'occupation en pourcentage (str)"""
    return f"{stats['tauxOccupation'] * 100:.0f} %"


class EditionTexte(Edition):
    """Rapport en texte brut."""

    extension = ".txt"

    def contenu(self, stats):
        lignes = [
            "DreamPark : statistiques",
            "",
            f"Nombre de passages : {stats['nbPassages']}",
            f"Durée moyenne de stationnement : {_duree(stats)}",
            f"Taux d'occupation : {_taux(stats)}",
            "",
            "Passages par jour :",
        ]
        for jour, nb in stats["passagesParJour"].items():
            lignes.append(f"  {jour.strftime('%d/%m/%Y')} : {nb}")
        lignes += ["", "Activité par service :"]
        for service, nb in stats["activiteParService"].items():
            lignes.append(f"  {service} : {nb}")
        lignes += ["", "Clients réguliers à qui proposer un abonnement :"]
        lignes += [f"  {nom}" for nom in stats["clientsReguliers"]] or ["  aucun"]
        return "\n".join(lignes) + "\n"


class EditionHTML(Edition):
    """Page HTML avec des tableaux."""

    extension = ".html"

    def contenu(self, stats):
        def tableau(titre, lignes):
            corps = "".join(f"<tr><td>{escape(str(a))}</td><td>{escape(str(b))}</td></tr>"
                            for a, b in lignes)
            return f"<h2>{titre}</h2>\n<table>\n{corps}\n</table>\n"

        resume = [("Nombre de passages", stats["nbPassages"]),
                  ("Durée moyenne de stationnement", _duree(stats)),
                  ("Taux d'occupation", _taux(stats))]
        jours = [(j.strftime("%d/%m/%Y"), nb) for j, nb in stats["passagesParJour"].items()]
        clients = "".join(f"<li>{escape(nom)}</li>" for nom in stats["clientsReguliers"]) or "<li>aucun</li>"
        return ("<!DOCTYPE html>\n<html lang=\"fr\">\n<head><meta charset=\"utf-8\">"
                "<title>DreamPark : statistiques</title></head>\n<body>\n"
                "<h1>DreamPark : statistiques</h1>\n"
                + tableau("Résumé", resume)
                + tableau("Passages par jour", jours)
                + tableau("Activité par service", stats["activiteParService"].items())
                + f"<h2>Clients réguliers</h2>\n<ul>{clients}</ul>\n</body>\n</html>\n")


class EditionImage(Edition):
    """Plan du parking en image SVG : places libres en vert, occupées en rouge."""

    extension = ".svg"
    VERT = "#2e7d32"
    ROUGE = "#c62828"
    LARGEUR, HAUTEUR, MARGE = 60, 40, 10

    def contenu(self, stats):
        # une ligne par niveau (la lettre de l'idPlace), une colonne par place
        niveaux = {}
        for idPlace, estLibre in stats["places"]:
            niveaux.setdefault(idPlace[0], []).append((idPlace, estLibre))
        nbColonnes = max((len(p) for p in niveaux.values()), default=0)
        w = self.MARGE + nbColonnes * (self.LARGEUR + self.MARGE)
        h = self.MARGE + len(niveaux) * (self.HAUTEUR + self.MARGE)
        formes = []
        for ligne, places in enumerate(niveaux.values()):
            for colonne, (idPlace, estLibre) in enumerate(places):
                x = self.MARGE + colonne * (self.LARGEUR + self.MARGE)
                y = self.MARGE + ligne * (self.HAUTEUR + self.MARGE)
                couleur = self.VERT if estLibre else self.ROUGE
                formes.append(f'<rect x="{x}" y="{y}" width="{self.LARGEUR}" height="{self.HAUTEUR}" '
                              f'fill="{couleur}"/>')
                formes.append(f'<text x="{x + self.LARGEUR // 2}" y="{y + self.HAUTEUR // 2 + 5}" '
                              f'text-anchor="middle" fill="white">{escape(idPlace)}</text>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">\n'
                + "\n".join(formes) + "\n</svg>\n")
