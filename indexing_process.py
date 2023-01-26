import json
import typing


class DocumentCollection:
    def __init__(self):
        self.docs: typing.List[Document] = []

    def add_document(self, doc: Document):
        self.docs.append(doc)

    def get_all_docs(self) -> typing.List[Document]:
        return self.docs



class TransformedDocument(typing.NamedTuple):
    doc_id: str
    tokens: typing.List[str]


class TransformedDocumentCollection:
    def __init__(self):
        self.docs: typingList[TransformedDocument] = []

    def add_document(self, doc: TransformedDocument):
        self.docs.append(doc)

    def write(self, path: str):
        json_data = {'docs': [td._asdict() for td in self.docs]}
        with open(path, 'w') as fp:
            json.dump(obj=json_data, fp=fp)


    @staticmethod
    def read(path:str) -> 'TransformedDocumentCollection':
        out = TransformedDocumentCollection()
        with open(path) as fp:
            collection_dict = json.load(fp)

        doc_records = collection_dict['docs']
        for record in doc_records:
            doc = TransformedDocument(doc_id=record['doc_id'], tokens=record['tokens'])
            out.add_document(doc)
        return out





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
            doc = Document(doc_id=record['id'], text=record['init_text'])
            doc_collection.add_document(doc)
        return doc_collection


def tokenize(document_text: str) -> typing.List[str]:
    return document_text.lower().split()




def transform_documents(document_collection):
    docs = document_collection.get_all_docs()
    out = TransformedDocumentCollection()
    for d in docs:
        tokens = tokenize(d.text)
        transformed_doc = TransformedDocument(doc_id=d.doc_id, tokens=tokens)
        out.add_document(transformed_doc)
    return out





def create_index(transformed_documents):
    pass


def indexing_process(document_source: WikiSource) -> (DocumentCollection, Index):
    document_collection = document_source.read_documents()
    transformed_documents = transform_documents(document_collection)
    # transformed_documents.write(path ='')
    index = create_index(transformed_documents)
    return (document_collection, index)