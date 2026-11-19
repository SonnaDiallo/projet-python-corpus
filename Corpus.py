"""Module Corpus : gère une collection de documents et d'auteurs (TD4, partie 3)."""

from datetime import datetime

import pandas as pd

from Author import Author
from Document import Document

"""le decorateur Singleton pour garantir qu'il n'existe qu'une seule instance de corpus
permet d'utiliser toujours le même objet Corpus, plutôt que de créer plusieurs corpus différents """
def singleton(cls):
    instances = [None]

    def wrapper(*args, **kwargs):
        if instances[0] is None:
            instances[0] = cls(*args, **kwargs)

        return instances[0]

    return wrapper
@singleton
class Corpus:
    """Un corpus de documents, avec ses auteurs.

    Attributs :
        nom    : nom du corpus
        authors: dictionnaire {nom de l'auteur : objet Author}
        id2doc : dictionnaire {identifiant : objet Document}
        ndoc   : nombre de documents
        naut   : nombre d'auteurs
    """

    def __init__(self, nom):
        self.__nom = nom
        self.__authors = {}
        self.__id2doc = {}
        self.__ndoc = 0
        self.__naut = 0

    #Accesseurs
    def getNom(self):
        return self.__nom

    def getAuthors(self):
        return self.__authors

    def getId2doc(self):
        return self.__id2doc

    def getNdoc(self):
        return self.__ndoc

    def getNaut(self):
        return self.__naut

    def add(self, document):
        #Ajoute un document au corpus et met à jour l'auteur correspondant.
        doc_id = self.__ndoc  # identifiant unique généré au fur et à mesure
        self.__id2doc[doc_id] = document
        self.__ndoc += 1

        # Si l'auteur est inconnu, on crée une nouvelle instance d'Author
        if document.getAuteur() not in self.__authors:
            self.__authors[document.getAuteur()] = Author(document.getAuteur())
            self.__naut += 1
        self.__authors[document.getAuteur()].add(doc_id, document)
        return doc_id

    def get_author(self, nom):
        #Renvoie l'objet Author correspondant, ou None s'il est inconnu.
        return self.__authors.get(nom)

    def afficher_par_date(self, n=5):
        #Affiche les n documents les plus récents (documents sans date en dernier).
        docs = sorted(self.__id2doc.values(),
                      key=lambda d: d.getDate() or datetime.min,
                      reverse=True)
        for doc in docs[:n]:
            print(f"{doc.getDate()} | {doc}")

    def afficher_par_titre(self, n=5):
        #Affiche les n premiers documents par ordre alphabétique de titre.
        docs = sorted(self.__id2doc.values(), key=lambda d: d.getTitre().lower())
        for doc in docs[:n]:
            print(f"{doc.getTitre()} | {doc.getDate()}")

    def __repr__(self):
        return f"Corpus '{self.__nom}' : {self.__ndoc} documents, {self.__naut} auteurs"

    # ---------- Sauvegarde / chargement via un DataFrame ----------

    def save(self, chemin):
        #Enregistre le corpus dans un fichier CSV (séparateur tabulation).
        lignes = [{"id": i,
                   "titre": d.getTitre(),
                   "auteur": d.getAuteur(),
                   "date": d.getDate().isoformat() if d.getDate() else "",
                   "url": d.getUrl(),
                   "texte": d.getTexte(),
                   "origine": d.getOrigine()}
                  for i, d in self.__id2doc.items()]
        pd.DataFrame(lignes).to_csv(chemin, sep="\t", index=False)

    def load(self, chemin):
        #Recharge le corpus depuis un CSV créé par save (remplace le contenu actuel).
        df = pd.read_csv(chemin, sep="\t", keep_default_na=False)
        self.__authors, self.__id2doc = {}, {}
        self.__ndoc = self.__naut = 0
        for _, ligne in df.iterrows():
            self.add(Document(titre=ligne["titre"],
                              auteur=ligne["auteur"],
                              date=Document.parse_date(ligne["date"]),
                              url=ligne["url"],
                              texte=ligne["texte"],
                              origine=ligne["origine"]))

    def afficher(self):
        for document in self.__id2doc.values():
            print(f"{document.getTitre()}, source: {document.getType()}")
