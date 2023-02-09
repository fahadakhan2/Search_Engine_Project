import collections
import typing

from documents import TransformedDocument, TransformedDocumentCollection


def count_words(doc: TransformedDocument) -> collections.Counter:
    return collections.Counter(doc.tokens)


def count_words_in_collection(docs: TransformedDocumentCollection) -> collections.Counter:
    totals = collections.Counter()
    for doc in docs.get_all_docs():
        totals.update(count_words(doc))
    return totals


def document_counts(docs: TransformedDocumentCollection) -> collections.Counter:
    """
    Compute number of documents each word occurs in.
    :param docs: TransformedDocumentCollection to run over
    :return: A counter mapping tokens to the number of documents each token occurs in.
    """
    num_docs = collections.Counter()
    for doc in docs.get_all_docs():
        num_docs.update(collections.Counter(set(doc.tokens)))
    return num_docs

def doc_tf_idf_scores(doc : TransformedDocument, doc_frequencies: collections.Counter) -> typing.Dict[str, float]:
    out = dict()
    term_frequencies = count_words(doc)
    for term, freq in term_frequencies:
        weight = freq / doc_frequencies[term]
        out[term] = weight
    return out


def tf_idf_scores(docs: TransformedDocumentCollection):
    doc_frequencies = document_counts(docs)
    out = list()
    for doc in docs.get_all_docs():
        out.append(doc_tf_idf_scores(doc, doc_frequencies))
    return out