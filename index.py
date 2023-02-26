import json
import typing
from collections import Counter, defaultdict

import counting
from documents import TransformedDocument


class Index:
    def add_document(self, doc: TransformedDocument):
        raise NotImplementedError

    def search(self, query: typing.List[str]) -> typing.List[str]:
        raise NotImplementedError

    def write(self, path: str):
        raise NotImplementedError

    @staticmethod
    def read(path: str):
        raise NotImplementedError


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


class TfIdfIndex(Index):
    def __init__(self):
        self.number_of_documents = 0
        self.doc_count = Counter()
        # dictionary mapping doc_ids to term to term_frequency dicts.
        self.doc_id_to_term_frequencies: typing.Dict[str, typing.Dict[str, float]] = dict()

    def write(self, path: str):
        with open(path, 'w') as fp:
            metadata_record = {
                'doc_id': '__metadata__',
                'number_of_documents': self.number_of_documents,
                'doc_count': [{'term': term, 'doc_count': doc_count}
                              for term, doc_count in self.doc_count.items()]
            }
            fp.write(json.dumps(metadata_record) + '\n')
            for doc_id, term_freqs in self.doc_id_to_term_frequencies.items():
                record = {
                    'doc_id': doc_id,
                    'tfs': [{'term': term, 'tf': tf} for term, tf in term_freqs.items()]
                }
                fp.write(json.dumps(record) + '\n')

    @staticmethod
    def read(path: str) -> 'TfIdfIndex':
        index = TfIdfIndex()
        with open(path) as fp:
            for line in fp:
                record = json.loads(line)
                if record['doc_id'] == '__metadata__':
                    index.number_of_documents = record['number_of_documents']
                    index.doc_count = Counter({
                        doc_count_record['term']: doc_count_record['doc_count']
                        for doc_count_record in record['doc_count']
                    })
                else:
                    index.doc_id_to_term_frequencies[record['doc_id']] = {
                        tf_record['term']: tf_record['tf']
                        for tf_record in record['tfs']
                    }
        return index

    def add_document(self, doc: TransformedDocument):
        self.number_of_documents += 1
        self.doc_count.update(set(doc.tokens))
        term_counts = counting.count_words(doc)
        term_frequencies = {term: counting.term_frequency(count, len(doc.tokens))
                            for term, count in term_counts.items()}
        self.doc_id_to_term_frequencies[doc.doc_id] = term_frequencies

    def compute_score(self, query, term_freqs):
        score = 0.0
        for term in query:
            if term not in term_freqs:
                return None
            tf = term_freqs[term]
            idf = counting.inverse_doc_frequency(
                doc_count=self.doc_count[term], collection_size=self.number_of_documents)
            score += counting.tf_idf(tf, idf)
        return score

    def search(self, query: typing.List[str]) -> typing.List[str]:
        """
        Does search using the index.
        :param query: List of query terms.
        :return: List of doc_ids for matching documents in correct order.
        """
        doc_ids_to_scores = dict()
        for doc_id, term_freqs in self.doc_id_to_term_frequencies.items():
            score = self.compute_score(query, term_freqs)
            if score is not None:
                doc_ids_to_scores[doc_id] = score
        return sorted(doc_ids_to_scores.keys(), key=doc_ids_to_scores.get, reverse=True)


class DocInfo(typing.NamedTuple):
    doc_id: str
    tf: float
    # positions: typing.List[int]


class InvertedTfIdfIndex(Index):
    def __init__(self):
        self.number_of_documents = 0
        self.doc_count = Counter()
        self.term_to_doc_info: typing.Dict[str, typing.List[DocInfo]] = defaultdict(list)

    def add_document(self, doc: TransformedDocument):
        self.number_of_documents += 1
        self.doc_count.update(set(doc.tokens))
        term_counts = counting.count_words(doc)
        for term, count in term_counts.items():
            self.term_to_doc_info[term].append(
                DocInfo(doc_id=doc.doc_id,
                        tf=counting.term_frequency(count, len(doc.tokens))))

    def search(self, query: typing.List[str]) -> typing.List[str]:
        """
        Does search using the index.
        :param query: List of query terms.
        :return: List of doc_ids for matching documents in correct order.
        """
        doc_ids_to_scores = defaultdict(float)
        matches = None
        for term in query:
            doc_info_list = self.term_to_doc_info[term]
            matches = {di.doc_id for di in doc_info_list
                       if matches is None or di.doc_id in matches}
            for doc_info in doc_info_list:
                if doc_info.doc_id not in matches:
                    continue
                idf = counting.inverse_doc_frequency(
                    doc_count=self.doc_count[term],
                    collection_size=self.number_of_documents)
                doc_ids_to_scores[doc_info.doc_id] += counting.tf_idf(doc_info.tf, idf)
        return sorted(matches, key=doc_ids_to_scores.get, reverse=True)