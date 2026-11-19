from Document import Document, HackerNewsDocument, ArxivDocument


class DocumentGenerator:

    @staticmethod
    def factory(type_document, titre="", auteur="", date=None,
                url="", texte="", origine=""):

        if type_document == "document":
            return Document(titre, auteur, date, url, texte, origine)

        elif type_document == "hackernews":
            return HackerNewsDocument(titre, auteur, date, url, texte, origine)

        elif type_document == "arxiv":
            return ArxivDocument(titre, auteur, date, url, texte, origine)

        else:
            raise ValueError("Type de document non reconnu")