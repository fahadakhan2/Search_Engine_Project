from unittest import TestCase
from query_process import *
from tokenizer import Tokenizer
from documents import *


class FakeTokenizer(Tokenizer):
    def tokenize(self, text):
        return text.lower().split()


class TestTokenizerOnlyQueryTransformer(TestCase):
    def test_transform_query(self):
        fake_tokenizer = FakeTokenizer()
        transformer = TokenizerOnlyQueryTransformer(tokenizer=fake_tokenizer)
        query = "This is a sample query."
        expected_output = ['this', 'is', 'a', 'sample', 'query.']
        self.assertEqual(transformer.transform_query(query), expected_output)


class TestNaiveResultFormatter(TestCase):
    def setUp(self):
        # setup sample documents
        self.documents = DocumentCollection([Document("doc1", "This is document one."),
                                             Document("doc2", "This is document two."),
                                             Document("doc3", "This is document three.")])
        self.result_formatter = NaiveResultFormatter(self.documents)

    def test_format_results(self):
        # test with sample results
        results = ["doc1", "doc3"]
        expected_output = "\n" + format_single_result(self.documents.get("doc1")) + "\n" + format_single_result(
            self.documents.get("doc3"))
        self.assertEqual(self.result_formatter.format_results(results), expected_output)

