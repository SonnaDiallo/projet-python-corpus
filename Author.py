"""Module Author : représente un auteur et ses publications (TD4, partie 2)."""


class Author:
    """Un auteur, identifié par son nom (supposé unique).

    Attributs :
        name       : nom de l'auteur
        ndoc       : nombre de documents publiés
        production : dictionnaire {id du document : objet Document}
    """

    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}

    def add(self, doc_id, document):
        """Ajoute un document à la production de l'auteur."""
        if doc_id not in self.production:
            self.production[doc_id] = document
            self.ndoc += 1

    def taille_moyenne(self):
        """Taille moyenne (en caractères) des documents de l'auteur."""
        if self.ndoc == 0:
            return 0
        return sum(len(d.texte) for d in self.production.values()) / self.ndoc

    def __str__(self):
        return f"{self.name} ({self.ndoc} document(s))"

    def __repr__(self):
        return f"Author(name={self.name!r}, ndoc={self.ndoc})"
