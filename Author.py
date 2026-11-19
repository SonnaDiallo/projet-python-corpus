"""Module Author : représente un auteur et ses publications (TD4, partie 2)."""


class Author:
    """Un auteur, identifié par son nom (supposé unique).

    Attributs :
        name       : nom de l'auteur
        ndoc       : nombre de documents publiés
        production : dictionnaire {id du document : objet Document}
    """

    def __init__(self, name):
        self.__name = name
        self.__ndoc = 0
        self.__production = {}

     # Accesseurs et mutateurs
    
    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getNdoc(self):
        return self.__ndoc

    def getProduction(self):
        return self.__production

    def add(self, doc_id, document):
        #Ajoute un document à la production de l'auteur.
        if doc_id not in self.__production:
            self.__production[doc_id] = document
            self.__ndoc += 1

    def taille_moyenne(self):
        #Taille moyenne (en caractères) des documents de l'auteur.
        if self.__ndoc == 0:
            return 0
        return sum(len(d.texte) for d in self.__production.values()) / self.__ndoc

    def __str__(self):
        return f"{self.__name} ({self.__ndoc} document(s))"

    def __repr__(self):
        return f"Author(name={self.__name!r}, ndoc={self.__ndoc})"
