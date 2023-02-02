# Question 1:

# The difference between the two implementations of search lies in how documents are ranked and matched to the query.
# ranking.py uses term_count and boolean_term_count functions to calculate the number of matching terms between the
# query and the document and return the documents sorted in descending order of the match count. On the other hand,
# matching.py uses boolean_term_match function to match the query terms with the document terms and returns the
# documents that have a complete match of query terms.

# To produce just the best 10 results for a query in ranking.py, you can modify the search function to
# return only the first 10 documents from the sorted list of matching documents. Add the following below to search()
# return [documents[i] for i in indexes][:10]

# To produce just the best 10 results for a query in matching.py implementation, modify its search function to
# return only the first 10 elements of the list of matching documents. Add the code below inside the first if statement:
# if len(out) == 10:
#         break

# Question 2:

class DictDocumentCollection:
    def __init__(self):
        self.docs: typing.Dict[str, Document] = {}

    def add_document(self, doc: Document):
        self.docs[doc.doc_id] = doc

    def get_all_docs(self) -> typing.Dict[str, Document]:
        return self.docs

# Testcase added:
from unittest import TestCase
from typing import Dict
from documents import DictDocumentCollection, Document

class TestDictDocumentCollection(TestCase):
    def test_add_document(self):
        docs = DictDocumentCollection()
        docs.add_document(Document(doc_id='1', text='text1'))
        docs.add_document(Document(doc_id='2', text='text2'))
        self.assertEqual(docs.docs, {'1': Document(doc_id='1', text='text1'), '2': Document(doc_id='2', text='text2')})



# Question 3

    def write(self, path: str):
        json_data = {'docs': [d._asdict() for d in self.docs]}
        with open(path, 'w') as fp:
            json.dump(obj=json_data, fp=fp)

    @staticmethod
    def read(path: str) -> 'DictDocumentCollection':
        out = DictDocumentCollection()
        with open(path) as fp:
            collection_dict = json.load(fp)

        doc_records = collection_dict['docs']
        for record in doc_records:
            doc = Document(doc_id=record['doc_id'], text=record['text'])
            out.add_document(doc)
        return out

# Question 4

class LectureTranscriptsSource:
    DEFAULT_PATH = r'C:\lectures_transcripts2-8'

    def read_documents(self, data_file_path: str = DEFAULT_PATH) -> DictDocumentCollection:
        with open(data_file_path) as fp:
            doc_records = json.load(fp)
        doc_collection = DictDocumentCollection()
        for record in doc_records:
            doc_id = record['source_name'] + '_' + record['index']
            doc = Document(doc_id=doc_id, text=record['text'])
            doc_collection.add_document(doc)
        return doc_collection

