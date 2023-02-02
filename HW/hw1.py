# hw1.py
# Fahad Khan
# 1/17/23


# Question 0:
# a. My major is computer science, 2nd year, I would say I am not a beginner but learning a lot in a short amount of time.
# I also do learning of other coding languages, and I am working on projects outside of class.

# b. I would like to fully comprehend the construction and tools needed to create a search engine along with a feature.
# I would like to include this project on my resume, so I really want to expand by knowledge through this class and
# use this project to showcase part of my skills on my resume.


# Question 1:
# a. Databases use a specific query language such as SQL to retrieve data, while search engines use a simple text-based query.
#    Search engines search through a large collection of documents on the internet, while databases search a specific, limited set of data.
#    Databases typically have a structured format for storing data, such as tables with specific columns and rows, while search engines index and store unstructured text documents.

# b. A user's previous search queries and clicks can be used to infer their interests and intent.
#    Information about the user's age, location, and other demographics can be used to produce results.
#    the amount of time someone spends on a page can be used to infer the relevance of a document.


# Question 2:

# a. Loop Method
def set_difference(set_one, set_two):
    newSet = set()
    for strings in set_one:
        if strings not in set_two:
            newSet.add(strings)
    return newSet


# b. String Comprehension
def set_intersection(set_one, set_two):
    return {strings for strings in set_one if strings in set_two}


# c.
def set_one_match(set_one, set_two):
    for strings in set_one:
        if strings not in set_two:
            return False
    return True


# d.
def list_set(lst, my_set):
    newList = []
    for element in lst:
        if element in my_set:
            newList.append(element)
    return newList


# e.
def vowel_count(my_string):
    vowelSet = set("aeiouAEIOU")
    count = 0
    for char in my_string:
        if char in vowelSet:
            count += 1
    return count


# Question 3:

def get_dict_spans(text):
    word_spans = get_word_spans(text)
    dictSpan = {}
    for span in word_spans:
        word = Span.get_substring()
        dictSpan[word] = span
    return dictSpan


# Question 4:

def boolean_term_match(query: str, document: str) -> bool:
    query_terms: typing.List[str] = set(query.lower().split())
    document_terms: typing.List[str] = set(document.lower().split())
    for term in query_terms:
        if term not in document_terms:
            return False
    return True

# Question 5
# a. 2 & 3 both will match the query
# b. 1 & 2 when using string in operator to determine match


# Question 6
# test_search:
# self.assertEqual(['red and yellow', 'blue and yellow', 'predict color'],
#                          search('', ['red and yellow', 'blue and yellow', 'predict color']))
#
# self.assertEqual([], search('red', []))

# string_match:
#     def test_string_match_empty_query(self):
#         self.assertTrue(string_match('', 'red and yellow'))
#
#     def test_string_match_empty_document(self):
#         self.assertFalse(string_match('red', ''))
#
#     def test_string_match_multiword_query(self): #come back to this
#         self.assertTrue(string_match('red yellow', 'red yellow orange'))
#
#     def test_string_match_with_boolean_term_match(self):
#         self.assertEqual(False, string_match('red or yellow', 'red'), boolean_term_match('red or yellow', 'red'))

# boolean_term_match:
#     def test_boolean_term_matches(self):
#         self.assertTrue(boolean_term_match('red', 'red'))
#
#     def test_boolean_term_dont_match(self):
#         self.assertFalse(boolean_term_match('red', 'red, yellow'))
#
#     def test_boolean_term_match__match_substring(self):
#         self.assertFalse(boolean_term_match('red', 'predict color'))
#
#     def test_boolean_term_match_empty_query(self):
#         self.assertTrue(boolean_term_match('', 'red'))
#
#     def test_boolean_term_match_empty_document(self):
#         self.assertFalse(boolean_term_match('red', ''))
#
#     def test_boolean_term_match_multiword_query(self):
#         self.assertTrue(boolean_term_match('red and yellow', 'red and yellow'))
#
#     def test_boolean_term_match_with_string_match(self):
#         self.assertEqual(False, boolean_term_match('red', 'predict color'), string_match('red', 'predict color'))
