import typing


class Tokenizer:
    def tokenize(self, document_text: str) -> typing.List[str]:
        pass


class NaiveTokenizer(Tokenizer):
    def tokenize(self, document_text: str) -> typing.List[str]:
        return document_text.replace('.', ' . ').replace(',', ' , ').lower().split()
