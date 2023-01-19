from unittest import TestCase
from matching import *


class Test(TestCase):
    def test_search(self):
        self.assertEqual(['red and yellow'],search('red', ['red and yellow', 'blue and yellow', 'predict color']))

    def test_search_empty_query(self):
        self.assertEqual([], search('', ['red and yellow', 'blue and yellow', 'predict color']))

    def test_search_empty_collection(self):
        self.assertEqual([], search('red', []))




    def test_string_match_matches(self):
        self.assertTrue(string_match('red', 'red and yellow'))

    def test_string_match_dont_match(self):
        self.assertFalse(string_match('red', 'yellow and blue'))

    def test_string_match_match_substring(self):
        self.assertTrue(string_match('red', 'predict color'))

    def test_string_match_returns_true_but_search_does_not(self):
        self.assertTrue(string_match('color', 'predict color'))
        self.assertEqual([], search('color', ['predict color']))





    def test_boolean_term_match_matches(self):
        self.assertTrue(boolean_term_match('red', 'red and yellow'))

    def test_boolean_term_match_dont_match(self):
        self.assertFalse(boolean_term_match('red', 'yellow and blue'))

    def test_boolean_term_match_differs_from_string_match(self):
        self.assertNotEqual(string_match('red', 'predict color'), boolean_term_match('red', 'predict color'))

