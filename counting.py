import collections
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
