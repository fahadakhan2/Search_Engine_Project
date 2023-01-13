from unittest import TestCase
from matching import *


class Test(TestCase):
    def test_search(self):
        self.assertEqual(['red and yellow'],
                         search('red', ['red and yellow', 'blue and yellow', 'predict color']))

    def test_string_match__matches(self):
        self.assertTrue(string_match('red', 'red and yellow'))

    def test_string_match__dont_match(self):
        self.assertFalse(string_match('red', 'yellow and blue'))

    def test_string_match__match_substring(self):
        self.assertTrue(string_match('red', 'predict color'))

    # def test_boolean_term_match(self):
    #     self.fail()
