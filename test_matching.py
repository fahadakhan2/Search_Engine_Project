from unittest import TestCase
from matching import *


class Test(TestCase):
    def test_search(self):
        self.assertEqual(['red and yellow'], search('red', ['red and yellow', 'blue and yellow', 'predict color']))

        self.assertEqual(['red and yellow', 'blue and yellow', 'predict color'],
                         search('', ['red and yellow', 'blue and yellow', 'predict color']))

        self.assertEqual([], search('red', []))



    def test_string_match__matches(self):
        self.assertTrue(string_match('red', 'red and yellow'))

    def test_string_match__dont_match(self):
        self.assertFalse(string_match('red', 'yellow and blue'))

    def test_string_match__match_substring(self):
        self.assertTrue(string_match('red', 'predict color'))

    def test_string_match_empty_query(self):
        self.assertTrue(string_match('', 'red and yellow'))

    def test_string_match_empty_document(self):
        self.assertFalse(string_match('red', ''))

    def test_string_match_multiword_query(self):
        self.assertTrue(string_match('red yellow', 'red yellow orange'))

    def test_string_match_with_boolean_term_match(self):
        self.assertEqual(False, string_match('red or yellow', 'red'), boolean_term_match('red or yellow', 'red'))




    def test_boolean_term_matches(self):
        self.assertTrue(boolean_term_match('red', 'red'))

    def test_boolean_term_dont_match(self):
        self.assertFalse(boolean_term_match('red', 'red, yellow'))

    def test_boolean_term_match__match_substring(self):
        self.assertFalse(boolean_term_match('red', 'predict color'))

    def test_boolean_term_match_empty_query(self):
        self.assertTrue(boolean_term_match('', 'red'))

    def test_boolean_term_match_empty_document(self):
        self.assertFalse(boolean_term_match('red', ''))

    def test_boolean_term_match_multiword_query(self):
        self.assertTrue(boolean_term_match('red and yellow', 'red and yellow'))

    def test_boolean_term_match_with_string_match(self):
        self.assertEqual(False, boolean_term_match('red', 'predict color'), string_match('red', 'predict color'))

