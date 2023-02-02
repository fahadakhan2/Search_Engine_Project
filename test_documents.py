from unittest import TestCase
from typing import Dict
from documents import DictDocumentCollection, Document

class TestDictDocumentCollection(TestCase):
    def test_add_document(self):
        docs = DictDocumentCollection()
        docs.add_document(Document(doc_id='1', text='text1'))
        docs.add_document(Document(doc_id='2', text='text2'))
        self.assertEqual(docs.docs, {'1': Document(doc_id='1', text='text1'), '2': Document(doc_id='2', text='text2')})

    def test_get_all_docs(self):
        docs = DictDocumentCollection()
        docs.add_document(Document(doc_id='1', text='text1'))
        docs.add_document(Document(doc_id='2', text='text2'))
        all_docs = docs.get_all_docs()
        self.assertEqual(len(all_docs), 2)
        self.assertEqual(all_docs['1'].doc_id, '1')
        self.assertEqual(all_docs['1'].text, 'text1')
        self.assertEqual(all_docs['2'].doc_id, '2')
        self.assertEqual(all_docs['2'].text, 'text2')