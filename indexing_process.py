import json
from documents import Document, DocumentCollection, TransformedDocument, TransformedDocumentCollection
from index import Index, NaiveIndex
from tokenizer import Tokenizer, NaiveTokenizer


class Source:
    def read_documents(self):
        pass

class WikiSource(Source):
    DEFAULT_PATH = r'C:\wiki_small.json'

    def read_documents(self, data_file_path: str = DEFAULT_PATH) -> DocumentCollection:
        with open(data_file_path) as fp:
            doc_records = json.load(fp)
        doc_collection = DocumentCollection()
        for record in doc_records:
            doc = Document(doc_id=record['id'], text=record['init_text'])
            doc_collection.add_document(doc)
        return doc_collection



class IndexCreator:
    def create_index(transformed_documents):
        index = Index()
        for doc in transformed_documents.get_all_docs():
            index.add_document(doc)
        return index


class DocumentTransformer:
    def transform_documents(self, document_collection: DocumentCollection) -> TransformedDocumentCollection:
        pass

class TokenizerOnlyDocumentTransformer(DocumentTransformer):
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def transform_documents(self, document_collection: DocumentCollection) -> TransformedDocumentCollection:
        docs = document_collection.get_all_docs()
        out = TransformedDocumentCollection()
        for d in docs:
            tokens = self.tokenizer.tokenize(d.text)
            transformed_doc = TransformedDocument(doc_id=d.doc_id, tokens=tokens)
            out.add_document(transformed_doc)
        return out


class IndexingProcess:
    def __init__(self, document_transformer: DocumentTransformer, index: Index):
        self.document_transformer = document_transformer
        self.index = index

    @staticmethod
    def create_naive_indexing_process() -> 'IndexingProcess':
        return IndexingProcess(
            document_transformer=TokenizerOnlyDocumentTransformer(NaiveTokenizer()),
            index=NaiveIndex())

    def run(self, document_source: Source) -> (DocumentCollection, Index):
        document_collection = document_source.read_documents()
        transformed_documents = self.document_transformer.transform_documents(document_collection)
        # transformed_documents.write(path='')
        for doc in transformed_documents.get_all_docs():
            self.index.add_document(doc)
        return document_collection, self.index
