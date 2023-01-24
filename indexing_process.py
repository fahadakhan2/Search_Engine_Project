import json
import typing


class DocumentCollection:
    def __init__(self):
        self.docs = []

    def add_document(self, doc):
        self.docs.append(doc)


class Index:
    pass



class Document(typing.NamedTuple);
doc_id:str
text: str



class WikiSource:
    DEFAULT_PATH = r'C:\wiki_small.json'

    def read_documents(self, data_file_path: str = DEFAULT_PATH) -> DocumentCollection:
        with open(data_file_path) as fp:
            doc_records = json.load(fp)
        doc_collection = DocumentCollection()
        for record in doc_records:
            doc_collection.add_document(Document(doc_id=record['id'], text=record['init_text']))
        return doc_collection


def transform_document(document_text) -> typing.List[str]:
    return document_text.lower().split()




def transform_documents(document_collection):
    pass


def create_index(transformed_documents):
    pass


def indexing_process(document_source: WikiSource) -> (DocumentCollection, Index):
    document_collection = document_source.read_documents()
    transformed_documents = transform_documents(document_collection)
    index = create_index(transformed_documents)
    return (document_collection, index)