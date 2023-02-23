import json
import typing
from collections import defaultdict, Counter

import counting
from documents import TransformedDocument


class Index:
    def add_document(self, doc: TransformedDocument):
        pass

    def search(self, query: typing.List[str]) -> typing.List[str]:
        pass

class NaiveIndex(Index):
    def __init__(self):
        self.docs = dict()

    def add_document(self, doc: TransformedDocument):
        self.docs[doc.doc_id] = set(doc.tokens)

    def search(self, query: typing.List[str]) -> typing.List[str]:
        """
        Does search using the index.
        :param query: List of query terms.
        :return: List of doc_ids for matching documents in correct order.
        """
        query_terms_set = set(query)
        matching_doc_ids = []
        for doc_id, doc_terms_set in self.docs.items():
            if query_terms_set.issubset(doc_terms_set):
                matching_doc_ids.append(doc_id)
        return matching_doc_ids


class SimpleInvertedIndex(Index):
    def __init__(self):
        self.doc_id_sets = defaultdict(set)

    def add_document(self, doc_id: int, doc: TransformedDocument):
        for token in doc.tokens:
            self.doc_id_sets[token].add(doc_id)

    def write(self, path: str):
        index_list = [{"term": term, "doc_ids": list(doc_ids)} for term, doc_ids in self.doc_id_sets.items()]
        with open(path, "w") as file:
            json.dump(index_list, file)

    @staticmethod
    def read(path: str):
        with open(path, "r") as file:
            index_list = json.load(file)
        out = SimpleInvertedIndex()
        for index in index_list:
            out.doc_id_sets[index["term"]] = set(index["doc_ids"])
        return out

    def search(self, terms: typing.List[str]) -> typing.List[int]: ##intersects the current set doc_ids with the set of document IDs associated with the term in the query
        doc_ids = set(self.doc_id_sets[terms[0]])
        for term in terms[1:]:
            doc_ids.intersection_update(self.doc_id_sets[term])
        return list(doc_ids)

class DocInfo(typing.NamedTuple):
    doc_id: str
    tf: float
    # positions: typing.List[int]

class InvertedTfIdfIndex(TfIdfIndex):
    def __init__(self):
        self.number_of_documents = 0
        self.doc_count = Counter()
        self.term_to_doc_info: typing.Dict[str: typing.List[DocInfo]] = defaultdict(list)

    def add_document(self, doc:TransformedDocument):
        self.number_of_documents += 1
        self.doc_count.update(set(doc.tokens))
        term_counts = counting.count_words(doc)
        for term, count in term_counts.items():
            self.term_to_doc_info[term].append(DocInfo(doc_id=doc.doc_id,
                                                       tf=counting.term_frequency(count, len(doc.tokens))))

        # term_frequencies = {term: counting.term_frequency(count, len(doc.tokens))
        #                     for term, count in term_counts.items()}
        # self.doc_id_to_term_frequencies[doc.doc_id] = term_frequencies


class TfIdfIndex(Index):
    def __init__(self):
        self.number_of_documents = 0
        self.doc_count = Counter()
        # dictionary mapping doc_ids to term to term_frequency dicts
        self.doc_id_to_term_frequencies: typing.Dict[str, typing.Dict[str, float]] = dict()

    def write(self, path: str):
        with open(path, 'w') as fp:
            metadata_record = {
                'doc_id': '__metadata__',
                'number_of_documents': self.number_of_documents,
                'doc_count': [{'term': term, 'doc_count': doc_count} for term, doc_count in self.doc_count.items()]
            }
            fp.write(json.dumps(metadata_record) + '\n')
            for doc_id, term_freqs in self.doc_id_to_term_frequencies.items():
                record = {
                    'doc_id': doc_id,
                    'tfs': [{'term': term, 'tf': tf} for term, tf in term_freqs]
                }
                fp.write(json.dumps(record) + '\n')


    def add_document(self, doc:TransformedDocument):
        self.number_of_documents += 1
        self.doc_count.update(set(doc.tokens))
        term_counts = counting.count_words(doc)
        term_frequencies = {term: counting.term_frequency(count, len(doc.tokens))
                            for term, count in term_counts.items()}
        self.doc_id_to_term_frequencies[doc.doc_id] = term_frequencies


    def compute_score(self, query, term_freqs):
        score = 0
        for term in query:
            if term not in term_freqs:
                return None
            tf = term_freqs[term]
            idf = counting.inverse_doc_frequency(doc_count=self.doc_count[term], collection_size=self.number_of_documents)
            score += counting.tf_idf(tf, idf)
        return score



    def search(self, query: typing.List[str]) -> typing.List[str]:
        """
        Does search using the index.
        :param query: List of query terms.
        :return: List of doc_ids for matching documents in correct order.
        """
        doc_ids_to_scores = dict()
        list_of_doc_infos = []
        matches = defaultdict(float)
        for term in query:
            doc_info_list = self.term_to_doc_info[term]
            for doc_info in doc_info_list:
                doc_ids_to_scores[doc_info.doc_id] += self.score(
                    doc_info.tf, self.doc_count[term], self.number_of_documents)


        for doc_id, term_freqs in self.doc_id_to_term_frequencies.items():
            score = self.compute_score(query, term_freqs)
            if score is not None:
                doc_ids_to_scores[doc_id] = score
        return sorted(doc_ids_to_scores.keys(), key=doc_ids_to_scores.get, reverse=True)


