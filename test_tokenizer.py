import typing
from unittest import TestCase

import documents
import tokenizer
import time
import indexing_process

class Test(TestCase):
    def test_tokenize__separate_words(self):
        self.assertEqual(['some', 'word'], tokenizer.tokenize('some word'))
    def test_tokenize__lower_case(self):
        self.assertEqual(['some', 'word'], tokenizer.tokenize('Some word'))

    def test_tokenize__split_periods(self):
        self.assertEqual(['some', 'word', '.'], tokenizer.tokenize('Some word.'))

    def test_tokenize__split_comma(self):
        self.assertEqual(['some', ',', 'word'], tokenizer.tokenize('Some, word'))

class TestRegularExpressionTokenizer(TestCase):
    def test_sentence_detection(self):
        #A sentence with the end of a sentence and the start of another one. Should trigger sentence boundary detection
        #Need to inquire further about prupose of sentence boundary detection
        self.assertEqual(['This is a quick sentence.', ' ', 'And', 'another'],tokenizer.RegularExpressionTokenizer().tokenize('This is a quick sentence. And another'))
    def test_web_links(self):
        #a complicated web link that should not be split
        self.assertEqual(['https://www.wikipedia.org'], tokenizer.RegularExpressionTokenizer().tokenize('https://www.wikipedia.org'))
    def test_decimal(self):
        #a decimal number that should not be split
        self.assertEqual(['10.00'], tokenizer.RegularExpressionTokenizer().tokenize('10.00'))
    def test_regular_sentence(self):
        #A regular sentence that sentence boundary detection wont work for. For non word characters
        self.assertEqual(['This', 'is', 'a', 'regular', 'sentence', 'that', 'never', 'ends'], tokenizer.RegularExpressionTokenizer().tokenize('This is a regular sentence that never ends'))
    def test_timing(self):
        testCorpusCollection = indexing_process.CovidSource().read_documents().get_all_docs()
        regulartokenizer = tokenizer.RegularExpressionTokenizer()
        start_time = time.time()
        for i in range(10):
            for doc in testCorpusCollection:
                regulartokenizer.tokenize(doc.text)
        end_time = time.time()
        print(end_time-start_time)