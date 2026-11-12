"""Programme principal (v1) : acquisition des données, construction du corpus.

Le code d'acquisition (parties 1.1 et 1.2) est adapté de la correction du TD3
fournie par l'enseignante ; il a été étendu pour récupérer aussi le titre,
l'auteur, la date et l'url de chaque document (nécessaires au TD4).
"""

import html
import json
import os
import urllib.parse
import urllib.request

import xmltodict

from Corpus import Corpus
from Document import Document

THEME = "climate"
FICHIER_CORPUS = "corpus.csv"


def charger_hackernews(theme, nb=50):
    """Interroge l'API Hacker News et renvoie une liste de Document."""
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
        {"query": theme, "tags": "story", "hitsPerPage": nb})
    with urllib.request.urlopen(url) as reponse:
        hits = json.load(reponse)["hits"]

    documents = []
    for hit in hits:
        # story_text est absent pour les liens externes : on se rabat sur le titre
        texte = hit.get("story_text") or hit.get("title") or ""
        texte = html.unescape(texte).replace("<p>", " ").strip()
        documents.append(Document(
            titre=hit.get("title") or "",
            auteur=hit.get("author") or "inconnu",
            date=Document.parse_date(hit.get("created_at")),
            url=hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            texte=texte,
            origine="hackernews"))
    return documents


def charger_arxiv(theme, nb=50):
    """Interroge l'API Arxiv et renvoie une liste de Document."""
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": "all:" + theme, "start": 0, "max_results": nb})
    with urllib.request.urlopen(url) as reponse:
        donnees = xmltodict.parse(reponse.read())

    # xmltodict renvoie un dict (et non une liste) s'il n'y a qu'un résultat,
    # et la clef 'entry' est absente s'il n'y en a aucun.
    entrees = donnees["feed"].get("entry", [])
    if isinstance(entrees, dict):
        entrees = [entrees]

    documents = []
    for entree in entrees:
        # 'author' est un dict s'il y a un seul auteur, une liste sinon.
        # On garde le premier auteur comme auteur principal.
        auteurs = entree["author"]
        if isinstance(auteurs, dict):
            auteurs = [auteurs]
        documents.append(Document(
            titre=entree["title"].replace("\n", " ").strip(),
            auteur=auteurs[0]["name"],
            date=Document.parse_date(entree.get("published")),
            url=entree["id"],
            texte=entree["summary"].replace("\n", " ").strip(),
            origine="arxiv"))
    return documents


def construire_corpus():
    """Charge le corpus depuis le disque s'il existe, sinon interroge les API."""
    corpus = Corpus(f"Corpus {THEME}")
    if os.path.exists(FICHIER_CORPUS):
        corpus.load(FICHIER_CORPUS)
        print("Corpus chargé depuis le disque.")
    else:
        for doc in charger_hackernews(THEME) + charger_arxiv(THEME):
            # TD3 3.3 : on ignore les documents de moins de 20 caractères
            if len(doc.texte) >= 20:
                corpus.add(doc)
        corpus.save(FICHIER_CORPUS)
        print("Corpus construit depuis les API et sauvegardé.")
    return corpus


def statistiques_auteur(corpus):
    """Demande un nom d'auteur et affiche ses statistiques (TD4, question 2.4)."""
    nom = input("Nom d'un auteur (laisser vide pour passer) : ").strip()
    if not nom:
        return
    auteur = corpus.get_author(nom)
    if auteur is None:
        print("Auteur inconnu.")
    else:
        print(auteur)
        print(f"Taille moyenne de ses documents : {auteur.taille_moyenne():.0f} caractères")


if __name__ == "__main__":
    corpus = construire_corpus()
    print(repr(corpus))

    print("\n--- 5 documents les plus récents ---")
    corpus.afficher_par_date(5)
    print("\n--- 5 premiers documents par titre ---")
    corpus.afficher_par_titre(5)

    print()
    statistiques_auteur(corpus)