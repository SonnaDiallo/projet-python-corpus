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

    def __init__(self, titre="", auteur="", date=None, url="", texte="", origine="", type = "Document"):
        self.__titre = titre
        self.__auteur = auteur
        self.__date = date
        self.__url = url
        self.__texte = texte
        self.__origine = origine
        self.__type = type

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

    # Accesseurs et mutateurs
    def getTitre(self):
        return self.__titre

    def setTitre(self, titre):
        self.__titre = titre

    def getAuteur(self):
        return self.__auteur

    def setAuteur(self, auteur):
            self.__auteur = auteur

    def getDate(self):
        return self.__date

    def setDate(self, date):
            self.__date = date

    def getUrl(self):
        return self.__url

    def setUrl(self, url):
            self.__url = url

    def getTexte(self):
        return self.__texte

    def setTexte(self, texte):
            self.__texte = texte

    def getOrigine(self):
        return self.__origine

    def setOrigine(self, origine):
            self.__origine = origine

    def getType(self):
         return self.__type

    def afficher(self):
        #Affiche toutes les informations de l'instance (TD4, question 1.2).
        print(f"Titre   : {self.__titre}")
        print(f"Auteur  : {self.__auteur}")
        print(f"Date    : {self.__date}")
        print(f"URL     : {self.__url}")
        print(f"Origine : {self.__origine}")
        print(f"Type    : {self.getType()}")
        print(f"Texte   : {self.__texte}")

    def __str__(self):
       # Version digeste, utilisée par print(doc) : le titre seulement.
        return self.__titre

    def __repr__(self):
        return f"Document(titre={self.__titre!r}, auteur={self.__auteur!r}, date={self.__date})"

class HackerNewsDocument(Document):

    def __init__(self, titre="", auteur="", date=None, url="", texte="", origine=""):
        super().__init__(titre, auteur, date, url, texte, origine, "Hacker News")
        self.__nbCommentaire = 0

    # Accesseurs et mutateurs
    def getNbCommentaire(self):
        return self.__nbCommentaire

    def setNbCommentaire(self, nbCommentaire):
        self.__nbCommentaire = nbCommentaire

    def getType(self):
         return "Hacker News"

    def __str__(self):
        return f"titre: {self.getTitre()}, commentaires: {self.__nbCommentaire}"
    
class ArxivDocument(Document):

    def __init__(self, titre="", auteur="", date=None, url="", texte="", origine=""):
        super().__init__(titre, auteur, date, url, texte, origine, "Arxiv")
        self.__co_auteur = []

    # Accesseurs et mutateurs
    def getCoAuteur(self):
        return self.__co_auteur

    def setCoAuteur(self, coAuteur):
        self.__co_auteur = coAuteur

    def getType(self):
             return "Arxiv"

    # Ajouter les co-auteurs a la liste
    def ajouterCoAuteur(self, co_auteur):
        self.__co_auteur.append(co_auteur)

    # Afficher la liste
    def afficherCoAuteur(self): 
        for co_aut in self.__co_auteur:
            print(f"co-auteur: {co_aut}")
