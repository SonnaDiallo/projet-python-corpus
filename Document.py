"""Module Document : représente un document du corpus (TD4, partie 1)."""

from datetime import datetime


class Document:
    """Un document textuel accompagné de ses méta-données.

    Attributs :
        titre   : titre du document
        auteur  : nom de l'auteur
        date    : date de publication (objet datetime, ou None si inconnue)
        url     : url source
        texte   : contenu textuel
        origine : source du document ("hackernews" ou "arxiv")
    """

    def __init__(self, titre="", auteur="", date=None, url="", texte="", origine=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.origine = origine

    @staticmethod
    def parse_date(valeur):
        """Convertit une chaîne ISO 8601 (ex. '2024-05-03T12:30:00Z') en datetime.

        Renvoie None si la valeur est vide ou illisible, afin de ne jamais
        faire planter le chargement du corpus à cause d'une date mal formée.
        """
        if not valeur:
            return None
        try:
            # fromisoformat n'accepte pas le 'Z' final avant Python 3.11
            return datetime.fromisoformat(str(valeur).replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            return None

    def afficher(self):
        """Affiche toutes les informations de l'instance (TD4, question 1.2)."""
        print(f"Titre   : {self.titre}")
        print(f"Auteur  : {self.auteur}")
        print(f"Date    : {self.date}")
        print(f"URL     : {self.url}")
        print(f"Origine : {self.origine}")
        print(f"Texte   : {self.texte}")

    def __str__(self):
        """Version digeste, utilisée par print(doc) : le titre seulement."""
        return self.titre

    def __repr__(self):
        return f"Document(titre={self.titre!r}, auteur={self.auteur!r}, date={self.date})"
