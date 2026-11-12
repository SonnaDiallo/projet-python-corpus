"""Module Corpus : gère une collection de documents et d'auteurs (TD4, partie 3)."""

from datetime import datetime

import pandas as pd

from Author import Author
from Document import Document


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
        self.nom = nom
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, document):
        """Ajoute un document au corpus et met à jour l'auteur correspondant."""
        doc_id = self.ndoc  # identifiant unique généré au fur et à mesure
        self.id2doc[doc_id] = document
        self.ndoc += 1

        # Si l'auteur est inconnu, on crée une nouvelle instance d'Author
        if document.auteur not in self.authors:
            self.authors[document.auteur] = Author(document.auteur)
            self.naut += 1
        self.authors[document.auteur].add(doc_id, document)
        return doc_id

    def get_author(self, nom):
        """Renvoie l'objet Author correspondant, ou None s'il est inconnu."""
        return self.authors.get(nom)

    def afficher_par_date(self, n=5):
        """Affiche les n documents les plus récents (documents sans date en dernier)."""
        docs = sorted(self.id2doc.values(),
                      key=lambda d: d.date or datetime.min,
                      reverse=True)
        for doc in docs[:n]:
            print(f"{doc.date} | {doc}")

    def afficher_par_titre(self, n=5):
        """Affiche les n premiers documents par ordre alphabétique de titre."""
        docs = sorted(self.id2doc.values(), key=lambda d: d.titre.lower())
        for doc in docs[:n]:
            print(f"{doc.titre} | {doc.date}")

    def __repr__(self):
        return f"Corpus '{self.nom}' : {self.ndoc} documents, {self.naut} auteurs"

    # ---------- Sauvegarde / chargement via un DataFrame ----------

    def save(self, chemin):
        """Enregistre le corpus dans un fichier CSV (séparateur tabulation)."""
        lignes = [{"id": i,
                   "titre": d.titre,
                   "auteur": d.auteur,
                   "date": d.date.isoformat() if d.date else "",
                   "url": d.url,
                   "texte": d.texte,
                   "origine": d.origine}
                  for i, d in self.id2doc.items()]
        pd.DataFrame(lignes).to_csv(chemin, sep="\t", index=False)

    def load(self, chemin):
        """Recharge le corpus depuis un CSV créé par save (remplace le contenu actuel)."""
        df = pd.read_csv(chemin, sep="\t", keep_default_na=False)
        self.authors, self.id2doc = {}, {}
        self.ndoc = self.naut = 0
        for _, ligne in df.iterrows():
            self.add(Document(titre=ligne["titre"],
                              auteur=ligne["auteur"],
                              date=Document.parse_date(ligne["date"]),
                              url=ligne["url"],
                              texte=ligne["texte"],
                              origine=ligne["origine"]))
