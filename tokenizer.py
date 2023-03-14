import typing
import re


class Tokenizer:
    def tokenize(self, document_text: str) -> typing.List[str]:
        pass


class NaiveTokenizer(Tokenizer):
    def tokenize(self, document_text: str) -> typing.List[str]:
        return document_text.replace('.', ' . ').replace(',', ' , ').lower().split()


class RegularExpressionTokenizer(Tokenizer):
    def tokenize(self, document_text: str) -> typing.List[str]:
        # regular expression patterns for sentence boundary, urls, decimals
        sentence_end_re = r'(?<=[.!?])\s+(?=[A-Z])|^ *[A-Z]+.*?[.!?](?= |\Z)'
        url_re = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        decimal_re = r'\d+\.\d+'

        # tokenize the input text using the regex patterns listed above
        regex_tokens = re.findall(sentence_end_re + '|' + url_re + '|' + decimal_re + '|[\w]+', document_text)

        # remove any string tokens that are empty and contain nothing
        tokens = list(filter(None, regex_tokens))
        return tokens
