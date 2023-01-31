import json
import typing

from documents import Document, DocumentCollection, TransformedDocument, TransformedDocumentCollection
from index import Index


# class DictDocumentCollection:
#     def __init__(self):
#         self.docs: typing.Dict[Document] = {}
#
#     def add_document(self, doc: Document):
#         pass


class WikiSource:
    DEFAULT_PATH = r'C:\Users\Alex\Documents\DePaul\datasets\wiki_small\wiki_small.json'

    def read_documents(self, data_file_path: str = DEFAULT_PATH) -> DocumentCollection:
        with open(data_file_path) as fp:
            doc_records = json.load(fp)
        doc_collection = DocumentCollection()
        for record in doc_records:
            doc = Document(doc_id=record['id'], text=record['init_text'])
            doc_collection.add_document(doc)
        return doc_collection


def tokenize(document_text: str) -> typing.List[str]:
    return document_text.lower().split()


def transform_documents(document_collection: DocumentCollection) -> TransformedDocumentCollection:
    docs = document_collection.get_all_docs()
    out = TransformedDocumentCollection()
    for d in docs:
        tokens = tokenize(d.text)
        transformed_doc = TransformedDocument(doc_id=d.doc_id, tokens=tokens)
        out.add_document(transformed_doc)
    return out


def create_index(transformed_documents):
    index = Index()
    for doc in transformed_documents.get_all_docs():
        index.add_document(doc)
    return index



def indexing_process(document_source: WikiSource) -> (DocumentCollection, Index):
    document_collection = document_source.read_documents()
    transformed_documents = transform_documents(document_collection)
    # transformed_documents.write(path='')
    index = create_index(transformed_documents)
    return document_collection, index
