from typing import List
from documents import DocumentCollection, Document
from index import Index, NaiveIndex
import tokenizer


def process_query(query: str) -> List[str]:
    return tokenizer.tokenize(query)


def format_single_result(doc: Document) -> str:
    return doc.text


class NaiveResultFormatter:
    def __init__(self, documents: DocumentCollection):
        self.documents = documents

    def format_results(self, results: List[str]) -> str:
        out = ''
        for doc_id in results:
            doc = self.documents.get(doc_id)
            out += '\n' + format_single_result(doc)
        return out


class TokenizerOnlyQueryTransformer:
    def __init__(self, tokenizer: tokenizer.Tokenizer):
        self.tokenizer = tokenizer

    def transform_query(self, query: str) -> List[str]:
        return self.tokenizer.tokenize(query)


class QueryProcess:
    def __init__(self, result_formatter: NaiveResultFormatter, index: Index,
                 query_transformer: TokenizerOnlyQueryTransformer):
        self.result_formatter = result_formatter
        self.index = index
        self.query_transformer = query_transformer

    @staticmethod
    def create_naive_query_process(documents: DocumentCollection, index: Index) -> 'QueryProcess':
        return QueryProcess(
            result_formatter=NaiveResultFormatter(documents),
            index=index,
            query_transformer=TokenizerOnlyQueryTransformer(tokenizer.NaiveTokenizer())
        )

    def run(self, query: str) -> str:
        processed_query = self.query_transformer.transform_query(query)
        results = self.index.search(processed_query)
        formatted_results = self.result_formatter.format_results(results)
        return formatted_results
